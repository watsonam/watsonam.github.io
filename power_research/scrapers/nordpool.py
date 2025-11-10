import pandas as pd
import re
from datetime import datetime, timedelta
from typing import Optional
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
    options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
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
                if 10 < price_value < 500:
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
    return df


def scrape_nordpool_volumes(delivery_date: Optional[str] = None, area: str = 'UK') -> Optional[pd.DataFrame]:
    if delivery_date is None:
        delivery_date = datetime.now().strftime('%Y-%m-%d')
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
    return df


def save_data(df: pd.DataFrame, delivery_date: str) -> str:
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"nordpool_{delivery_date}_{timestamp}.csv"
    df.to_csv(filename, index=False)
    return filename