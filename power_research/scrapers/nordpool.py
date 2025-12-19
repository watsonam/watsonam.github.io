import pandas as pd
import re
import os
import pickle
from datetime import datetime, timedelta
from typing import Optional
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


def setup_driver() -> webdriver.Chrome:
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')

    import platform
    if platform.system() == "Darwin":
        options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    elif os.path.exists("/usr/bin/google-chrome"):
        options.binary_location = "/usr/bin/google-chrome"

    return webdriver.Chrome(options=options)


def is_valid_hourly_period(time_period: str) -> bool:
    try:
        start_str, end_str = time_period.split(' - ')
        start_hour, start_min = map(int, start_str.split(':'))
        end_hour, end_min = map(int, end_str.split(':'))
        if start_min != 0 or end_min != 0:
            return False
        expected_end_hour = (start_hour + 1) % 24
        return end_hour == expected_end_hour
    except (ValueError, IndexError):
        return False


def extract_price_data(page_text: str) -> list[dict[str, str | float]]:
    data = []
    lines = page_text.split('\n')
    for line in lines:
        line = line.strip()
        if not line:
            continue
        time_match = re.search(r'(\d{2}:\d{2}\s*-\s*\d{2}:\d{2})', line)
        if time_match:
            time_period = time_match.group(1)
            if not is_valid_hourly_period(time_period):
                continue
            price_matches = re.findall(r'(\d+[.,]\d+)', line)
            for price_text in price_matches:
                price_text = price_text.replace(',', '.')
                price_value = float(price_text)
                if 0 <= price_value < 1000:
                    data.append({
                        'period': time_period,
                        'price': price_value
                    })
                    break
    return data


def extract_volume_data(page_text: str) -> list[dict[str, str | float]]:
    data = []
    lines = page_text.split('\n')
    for line in lines:
        line = line.strip()
        if not line:
            continue
        time_match = re.search(r'(\d{2}:\d{2}\s*-\s*\d{2}:\d{2})', line)
        if time_match:
            time_period = time_match.group(1)
            if not is_valid_hourly_period(time_period):
                continue
            volume_matches = re.findall(r'(\d+\s?\d*[.,]\d+)', line)
            if len(volume_matches) >= 2:
                buy_volume_text = volume_matches[0].replace(' ', '').replace(',', '.')
                sell_volume_text = volume_matches[1].replace(' ', '').replace(',', '.')
                try:
                    buy_volume = float(buy_volume_text)
                    sell_volume = float(sell_volume_text)
                    if buy_volume > 100 and sell_volume > 100:
                        data.append({
                            'period': time_period,
                            'buy_volume': buy_volume,
                            'sell_volume': sell_volume
                        })
                except ValueError:
                    continue
    return data


def scrape_nordpool(delivery_date: Optional[str] = None, currency: str = 'GBP', area: str = 'UK') -> Optional[pd.DataFrame]:
    if delivery_date is None:
        delivery_date = datetime.now().strftime('%Y-%m-%d')

    cache_dir = 'cache'
    os.makedirs(cache_dir, exist_ok=True)
    cache_file = f'{cache_dir}/nordpool_prices_{delivery_date}_{currency}_{area}.pkl'

    if os.path.exists(cache_file):
        print(f"Loading prices from cache: {delivery_date}")
        return pickle.load(open(cache_file, 'rb'))

    request_date = datetime.strptime(delivery_date, '%Y-%m-%d')
    today = datetime.now()
    two_months_ago = today - timedelta(days=60)
    if request_date > today:
        print(f"Error: Future date {delivery_date} - Nord Pool only has historical data")
        return None
    if request_date < two_months_ago:
        print(f"Error: Date {delivery_date} too old - Nord Pool only keeps ~2 months of data")
        return None

    print(f"Fetching fresh data for {delivery_date}")
    url = f"https://data.nordpoolgroup.com/auction/n2ex/prices?deliveryDate={delivery_date}&currency={currency}&aggregation=DeliveryPeriod&deliveryAreas={area}"
    driver = setup_driver()
    driver.get(url)
    wait = WebDriverWait(driver, 10)
    try:
        def data_grid_loaded(driver):
            body_text = driver.find_element(By.TAG_NAME, "body").text
            return ("00:00 - 01:00" in body_text and "23:00 - 00:00" in body_text and
                    "Data grid with 24 rows" in body_text)
        wait.until(data_grid_loaded)
    except TimeoutException:
        print("Warning: Data grid did not load within timeout, proceeding anyway")
    page_text = driver.find_element(By.TAG_NAME, "body").text
    data = extract_price_data(page_text)
    driver.quit()
    if not data:
        return None
    df = pd.DataFrame(data)
    df = df.drop_duplicates().reset_index(drop=True)
    if len(df) != 24:
        print(f"Error: Expected exactly 24 hourly periods, but found {len(df)} rows")
        print(f"Data should contain 24 hours from 23:00-00:00 through 22:00-23:00")
        return None

    pickle.dump(df, open(cache_file, 'wb'))
    print(f"Cached prices: {cache_file}")
    return df


def scrape_nordpool_volumes(delivery_date: Optional[str] = None, area: str = 'UK') -> Optional[pd.DataFrame]:
    if delivery_date is None:
        delivery_date = datetime.now().strftime('%Y-%m-%d')

    cache_dir = 'cache'
    os.makedirs(cache_dir, exist_ok=True)
    cache_file = f'{cache_dir}/nordpool_volumes_{delivery_date}_{area}.pkl'

    if os.path.exists(cache_file):
        print(f"Loading volumes from cache: {delivery_date}")
        return pickle.load(open(cache_file, 'rb'))

    request_date = datetime.strptime(delivery_date, '%Y-%m-%d')
    today = datetime.now()
    two_months_ago = today - timedelta(days=60)
    if request_date > today:
        print(f"Error: Future date {delivery_date} - Nord Pool only has historical data")
        return None
    if request_date < two_months_ago:
        print(f"Error: Date {delivery_date} too old - Nord Pool only keeps ~2 months of data")
        return None

    print(f"Fetching volume data for {delivery_date}")
    url = f"https://data.nordpoolgroup.com/auction/n2ex/volumes?deliveryDate={delivery_date}&deliveryAreas={area}"
    driver = setup_driver()
    driver.get(url)
    wait = WebDriverWait(driver, 10)
    try:
        def data_grid_loaded(driver):
            body_text = driver.find_element(By.TAG_NAME, "body").text
            return ("00:00 - 01:00" in body_text and "23:00 - 00:00" in body_text and
                    "Data grid with 24 rows" in body_text)
        wait.until(data_grid_loaded)
    except TimeoutException:
        print("Warning: Data grid did not load within timeout, proceeding anyway")
    page_text = driver.find_element(By.TAG_NAME, "body").text
    data = extract_volume_data(page_text)
    driver.quit()
    if not data:
        return None
    df = pd.DataFrame(data)
    df = df.drop_duplicates().reset_index(drop=True)
    if len(df) != 24:
        print(f"Error: Expected exactly 24 hourly periods, but found {len(df)} rows")
        print(f"Data should contain 24 hours from 23:00-00:00 through 22:00-23:00")
        return None

    pickle.dump(df, open(cache_file, 'wb'))
    print(f"Cached volumes: {cache_file}")
    return df


def save_data(df: pd.DataFrame, delivery_date: str) -> str:
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"nordpool_{delivery_date}_{timestamp}.csv"
    df.to_csv(filename, index=False)
    return filename


def save_nordpool_history(days_back: int = 90, data_dir: str = "power_research/data/nordpool") -> int:
    base_path = Path(data_dir)
    prices_dir = base_path / "prices"
    volumes_dir = base_path / "volumes"
    prices_dir.mkdir(parents=True, exist_ok=True)
    volumes_dir.mkdir(parents=True, exist_ok=True)

    end_date = datetime.now()
    start_date = end_date - timedelta(days=days_back)
    current_date = start_date
    success_count = 0

    print(f"Saving Nord Pool data from {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")

    while current_date <= end_date:
        date_str = current_date.strftime('%Y-%m-%d')
        prices_file = prices_dir / f"{date_str}_prices.csv"
        volumes_file = volumes_dir / f"{date_str}_volumes.csv"

        if prices_file.exists() and volumes_file.exists():
            print(f"Skipping {date_str}")
            current_date += timedelta(days=1)
            continue

        print(f"Processing {date_str}")

        if not prices_file.exists():
            prices_df = scrape_nordpool(date_str)
            if prices_df is not None and len(prices_df) == 24:
                prices_df.to_csv(prices_file, index=False)
                print(f"Saved prices for {date_str}")

        if not volumes_file.exists():
            volumes_df = scrape_nordpool_volumes(date_str)
            if volumes_df is not None and len(volumes_df) == 24:
                volumes_df.to_csv(volumes_file, index=False)
                print(f"Saved volumes for {date_str}")
                success_count += 1

        current_date += timedelta(days=1)

    print(f"Completed: {success_count} days processed")
    return success_count


if __name__ == "__main__":
    save_nordpool_history(days_back=14)