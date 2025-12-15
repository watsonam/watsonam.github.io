import pandas as pd
import os
import pickle
from datetime import datetime, timedelta
from typing import Optional
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import re


def setup_driver() -> webdriver.Chrome:
    """Setup Chrome driver with anti-detection settings."""
    options = Options()
    # Don't use headless - EPEX SPOT blocks headless browsers
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    return webdriver.Chrome(options=options)


def extract_table_data(driver: webdriver.Chrome) -> list[dict]:
    """Extract 30-minute period data from the EPEX SPOT table."""
    data = []

    try:
        # Wait for table to be present
        time.sleep(15)  # Allow time for dynamic content to load

        # Extract time periods from page text
        page_text = driver.find_element(By.TAG_NAME, "body").text
        periods = re.findall(r'(\d{2}:\d{2}\s*-\s*\d{2}:\d{2})', page_text)
        print(f"Found {len(periods)} time periods in page")

        tables = driver.find_elements(By.TAG_NAME, "table")

        if not tables:
            print("No table found on page")
            return []

        table = tables[0]
        rows = table.find_elements(By.TAG_NAME, "tr")

        print(f"Found {len(rows)} total rows in table")

        period_index = 0

        for i, row in enumerate(rows):
            # Get all cells (both th and td)
            all_cells = row.find_elements(By.XPATH, ".//th | .//td")

            if len(all_cells) < 7:
                continue

            # Get all cell texts
            cell_texts = [cell.text.strip() for cell in all_cells]

            # Skip header rows
            if cell_texts[0] in ['Low', ''] or 'MWh' in cell_texts[0]:
                continue

            # Skip rows with all dashes or empty
            if all(c == '-' or c == '' for c in cell_texts[:7]):
                continue

            # Skip hour group rows (like "00 - 01")
            if re.match(r'^\d{2}\s*-\s*\d{2}$', cell_texts[0]):
                continue

            try:
                # Helper function to parse numeric values
                def parse_float(s):
                    if not s or s == '-':
                        return None
                    # Remove commas and convert to float
                    return float(s.replace(',', ''))

                # Parse all columns (first column is Low price, not period)
                low = parse_float(cell_texts[0])
                high = parse_float(cell_texts[1])
                last = parse_float(cell_texts[2])
                weight_avg = parse_float(cell_texts[3])
                buy_volume = parse_float(cell_texts[4])
                sell_volume = parse_float(cell_texts[5])
                volume = parse_float(cell_texts[6])
                rpd = parse_float(cell_texts[7]) if len(cell_texts) > 7 else None
                rpd_hh = parse_float(cell_texts[8]) if len(cell_texts) > 8 else None

                # Match with period from extracted list
                period = periods[period_index] if period_index < len(periods) else None

                if period is None:
                    continue

                row_data = {
                    'period': period,
                    'low_price': low,
                    'high_price': high,
                    'last_price': last,
                    'weight_avg_price': weight_avg,
                    'buy_volume': buy_volume,
                    'sell_volume': sell_volume,
                    'volume': volume
                }

                # Add RPD columns if available
                if rpd is not None:
                    row_data['rpd'] = rpd
                if rpd_hh is not None:
                    row_data['rpd_hh'] = rpd_hh

                data.append(row_data)
                period_index += 1

                if len(data) <= 5:
                    print(f"Row {i}: {period} -> Low: {low}, Avg: {weight_avg}, Vol: {volume}")

            except (ValueError, IndexError) as e:
                print(f"Error parsing row {i}: {e}")
                continue

        print(f"Extracted {len(data)} data rows")

    except Exception as e:
        print(f"Error extracting table data: {e}")
        import traceback
        traceback.print_exc()

    return data


def extract_auction_data(driver: webdriver.Chrome) -> tuple[dict, list[dict]]:
    """Extract intraday auction data from the EPEX SPOT table.

    Returns:
        Tuple of (summary_data, period_data) where:
        - summary_data contains baseload and peakload prices
        - period_data is a list of dicts with period, buy_volume, sell_volume, volume, price
    """
    summary_data = {}
    period_data = []

    try:
        time.sleep(15)  # Allow time for dynamic content to load

        # Extract time periods from page text
        page_text = driver.find_element(By.TAG_NAME, "body").text
        periods = re.findall(r'(\d{2}:\d{2}\s*-\s*\d{2}:\d{2})', page_text)
        print(f"Found {len(periods)} time periods in page")

        tables = driver.find_elements(By.TAG_NAME, "table")

        if not tables:
            print("No table found on page")
            return summary_data, period_data

        table = tables[0]
        rows = table.find_elements(By.TAG_NAME, "tr")

        print(f"Found {len(rows)} total rows in table")

        period_index = 0

        for i, row in enumerate(rows):
            cells = row.find_elements(By.XPATH, ".//th | .//td")

            if len(cells) < 2:
                continue

            cell_texts = [cell.text.strip() for cell in cells]

            # Check for Baseload/Peakload summary rows
            if len(cell_texts) >= 2:
                if cell_texts[0] == 'Baseload':
                    try:
                        summary_data['baseload_price'] = float(cell_texts[1].replace(',', ''))
                        print(f"Baseload price: {summary_data['baseload_price']}")
                        continue
                    except ValueError:
                        pass

                if cell_texts[0] == 'Peakload':
                    try:
                        summary_data['peakload_price'] = float(cell_texts[1].replace(',', ''))
                        print(f"Peakload price: {summary_data['peakload_price']}")
                        continue
                    except ValueError:
                        pass

            # Skip header rows
            if any(keyword in str(cell_texts) for keyword in ['Index', 'Buy Volume', 'MWh']):
                continue

            # Try to parse as data row (4 numeric values: buy, sell, volume, price)
            if len(cell_texts) >= 4:
                try:
                    buy_volume = float(cell_texts[0].replace(',', ''))
                    sell_volume = float(cell_texts[1].replace(',', ''))
                    volume = float(cell_texts[2].replace(',', ''))
                    price = float(cell_texts[3].replace(',', ''))

                    # Match with period from extracted list
                    period = periods[period_index] if period_index < len(periods) else None

                    if period:
                        row_data = {
                            'period': period,
                            'buy_volume': buy_volume,
                            'sell_volume': sell_volume,
                            'volume': volume,
                            'price': price
                        }

                        period_data.append(row_data)
                        period_index += 1

                        if len(period_data) <= 5:
                            print(f"Row {i}: {period} -> Buy: {buy_volume}, Sell: {sell_volume}, Price: {price}")

                except (ValueError, IndexError):
                    continue

        print(f"Extracted {len(period_data)} data rows")

    except Exception as e:
        print(f"Error extracting auction data: {e}")
        import traceback
        traceback.print_exc()

    return summary_data, period_data


def scrape_epexspot(delivery_date: Optional[str] = None,
                    market_area: str = 'GB',
                    product: str = '30') -> Optional[pd.DataFrame]:
    """
    Scrape EPEX SPOT intraday continuous market data for GB.

    Args:
        delivery_date: Date in format 'YYYY-MM-DD'. If None, uses today.
        market_area: Market area code (default: 'GB')
        product: Product type - '30' for 30-minute, '60' for hourly (default: '30')

    Returns:
        DataFrame with period, prices, and volumes
    """
    if delivery_date is None:
        delivery_date = datetime.now().strftime('%Y-%m-%d')

    # Setup cache
    cache_dir = 'cache'
    os.makedirs(cache_dir, exist_ok=True)
    cache_file = f'{cache_dir}/epexspot_{market_area}_{delivery_date}_p{product}.pkl'

    if os.path.exists(cache_file):
        print(f"Loading EPEX SPOT data from cache: {delivery_date}")
        return pickle.load(open(cache_file, 'rb'))

    # Validate date
    request_date = datetime.strptime(delivery_date, '%Y-%m-%d')
    today = datetime.now()

    if request_date > today:
        print(f"Error: Future date {delivery_date} - EPEX SPOT only has historical data")
        return None

    # EPEX SPOT typically keeps several months of data
    six_months_ago = today - timedelta(days=180)
    if request_date < six_months_ago:
        print(f"Warning: Date {delivery_date} may be too old - EPEX SPOT typically keeps ~6 months of data")

    print(f"Fetching EPEX SPOT data for {delivery_date}")

    # Build URL
    url = (f"https://www.epexspot.com/en/market-results"
           f"?market_area={market_area}"
           f"&auction="
           f"&trading_date="
           f"&delivery_date={delivery_date}"
           f"&underlying_year="
           f"&modality=Continuous"
           f"&sub_modality="
           f"&technology="
           f"&data_mode=table"
           f"&period="
           f"&production_period="
           f"&product={product}")

    driver = setup_driver()

    try:
        driver.get(url)

        # Extract table data
        data = extract_table_data(driver)

        if not data:
            print(f"No data found for {delivery_date}")
            return None

        df = pd.DataFrame(data)

        # Validate expected number of periods
        expected_periods = 48 if product == '30' else 24
        if len(df) != expected_periods:
            print(f"Warning: Expected {expected_periods} periods, but found {len(df)} rows")

        # Cache the data
        pickle.dump(df, open(cache_file, 'wb'))
        print(f"Cached EPEX SPOT data: {cache_file}")

        return df

    except Exception as e:
        print(f"Error scraping EPEX SPOT: {e}")
        import traceback
        traceback.print_exc()
        return None

    finally:
        driver.quit()


def scrape_epexspot_auction(delivery_date: Optional[str] = None,
                            market_area: str = 'GB',
                            auction: str = 'GB-IDA1',
                            product: str = '30') -> Optional[pd.DataFrame]:
    """
    Scrape EPEX SPOT intraday auction market data for GB.

    Args:
        delivery_date: Delivery date in format 'YYYY-MM-DD'. If None, uses today.
        market_area: Market area code (default: 'GB')
        auction: Auction type (default: 'GB-IDA1', 'GB-IDA2', 'GB-IDA3')
        product: Product type - '30' for 30-minute, '60' for hourly (default: '30')

    Returns:
        DataFrame with period, volumes, and prices. Baseload and peakload prices stored as attributes.
    """
    if delivery_date is None:
        delivery_date = datetime.now().strftime('%Y-%m-%d')

    # Setup cache
    cache_dir = 'cache'
    os.makedirs(cache_dir, exist_ok=True)
    cache_file = f'{cache_dir}/epexspot_auction_{auction}_{delivery_date}_p{product}.pkl'

    if os.path.exists(cache_file):
        print(f"Loading EPEX SPOT auction data from cache: {delivery_date}")
        return pickle.load(open(cache_file, 'rb'))

    # Validate date
    request_date = datetime.strptime(delivery_date, '%Y-%m-%d')
    today = datetime.now()

    if request_date > today:
        print(f"Error: Future date {delivery_date} - EPEX SPOT only has historical data")
        return None

    # EPEX SPOT typically keeps several months of data
    six_months_ago = today - timedelta(days=180)
    if request_date < six_months_ago:
        print(f"Warning: Date {delivery_date} may be too old - EPEX SPOT typically keeps ~6 months of data")

    print(f"Fetching EPEX SPOT auction data for {auction} on {delivery_date}")

    # Build URL - only delivery_date is needed for auction data
    url = (f"https://www.epexspot.com/en/market-results"
           f"?market_area={market_area}"
           f"&auction={auction}"
           f"&trading_date="
           f"&delivery_date={delivery_date}"
           f"&underlying_year="
           f"&modality=Auction"
           f"&sub_modality=Intraday"
           f"&technology="
           f"&data_mode=table"
           f"&period="
           f"&production_period="
           f"&product={product}")

    driver = setup_driver()

    try:
        driver.get(url)

        # Extract auction data
        summary_data, period_data = extract_auction_data(driver)

        if not period_data:
            print(f"No data found for {auction} on {delivery_date}")
            return None

        df = pd.DataFrame(period_data)

        # Add summary data as DataFrame attributes
        if 'baseload_price' in summary_data:
            df.attrs['baseload_price'] = summary_data['baseload_price']
        if 'peakload_price' in summary_data:
            df.attrs['peakload_price'] = summary_data['peakload_price']

        # Validate expected number of periods based on auction type
        # GB-IDA1: 48 periods (00:00-24:00)
        # GB-IDA2: 24 periods (12:00-24:00)
        # GB-IDA3: 24 periods (12:00-24:00)
        if auction == 'GB-IDA1':
            expected_periods = 48 if product == '30' else 24
        elif auction in ['GB-IDA2', 'GB-IDA3']:
            expected_periods = 24 if product == '30' else 12
        else:
            # Default assumption for unknown auction types
            expected_periods = 48 if product == '30' else 24

        if len(df) != expected_periods:
            print(f"Warning: Expected {expected_periods} periods for {auction}, but found {len(df)} rows")

        # Cache the data
        pickle.dump(df, open(cache_file, 'wb'))
        print(f"Cached EPEX SPOT auction data: {cache_file}")

        return df

    except Exception as e:
        print(f"Error scraping EPEX SPOT auction: {e}")
        import traceback
        traceback.print_exc()
        return None

    finally:
        driver.quit()


def save_epexspot_history(days_back: int = 90,
                          data_dir: str = "power_research/data/epexspot",
                          market_area: str = "GB",
                          product: str = "30") -> int:
    """
    Download historical EPEX SPOT data and save to CSV files.

    Args:
        days_back: Number of days to go back from today
        data_dir: Directory to save the data
        market_area: Market area code (default: 'GB')
        product: Product type - '30' for 30-minute (default: '30')

    Returns:
        Number of days successfully processed
    """
    base_path = Path(data_dir)
    data_path = base_path / market_area / f"product_{product}"
    data_path.mkdir(parents=True, exist_ok=True)

    end_date = datetime.now()
    start_date = end_date - timedelta(days=days_back)
    current_date = start_date
    success_count = 0

    print(f"Saving EPEX SPOT {market_area} data (product {product}) from {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")

    while current_date <= end_date:
        date_str = current_date.strftime('%Y-%m-%d')
        file_path = data_path / f"{date_str}.csv"

        if file_path.exists():
            print(f"Skipping {date_str} - already exists")
            current_date += timedelta(days=1)
            continue

        print(f"\nProcessing {date_str}")

        df = scrape_epexspot(date_str, market_area=market_area, product=product)

        if df is not None and len(df) > 0:
            df.to_csv(file_path, index=False)
            print(f"✓ Saved data for {date_str}: {len(df)} rows")
            success_count += 1
        else:
            print(f"✗ No data available for {date_str}")

        current_date += timedelta(days=1)

        # Be respectful - add a delay between requests
        time.sleep(3)

    print(f"\n{'='*60}")
    print(f"Completed: {success_count}/{days_back + 1} days processed successfully")
    return success_count


def save_epexspot_auction_history(days_back: int = 90,
                                   data_dir: str = "power_research/data/epexspot_auction",
                                   market_area: str = "GB",
                                   auction: str = "GB-IDA1",
                                   product: str = "30") -> int:
    """
    Download historical EPEX SPOT auction data and save to CSV files.

    Args:
        days_back: Number of days to go back from today
        data_dir: Directory to save the data
        market_area: Market area code (default: 'GB')
        auction: Auction type (default: 'GB-IDA1')
        product: Product type - '30' for 30-minute (default: '30')

    Returns:
        Number of days successfully processed
    """
    base_path = Path(data_dir)
    data_path = base_path / market_area / auction / f"product_{product}"
    data_path.mkdir(parents=True, exist_ok=True)

    end_date = datetime.now()
    start_date = end_date - timedelta(days=days_back)
    current_date = start_date
    success_count = 0

    print(f"Saving EPEX SPOT {auction} data (product {product}) from {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")

    while current_date <= end_date:
        date_str = current_date.strftime('%Y-%m-%d')
        file_path = data_path / f"{date_str}.csv"

        if file_path.exists():
            print(f"Skipping {date_str} - already exists")
            current_date += timedelta(days=1)
            continue

        print(f"\nProcessing {date_str}")

        df = scrape_epexspot_auction(date_str, market_area=market_area, auction=auction, product=product)

        if df is not None and len(df) > 0:
            # Save the period data
            df.to_csv(file_path, index=False)

            # Also save summary data in a separate file
            if hasattr(df, 'attrs') and ('baseload_price' in df.attrs or 'peakload_price' in df.attrs):
                summary_file = data_path / f"{date_str}_summary.txt"
                with open(summary_file, 'w') as f:
                    if 'baseload_price' in df.attrs:
                        f.write(f"Baseload: {df.attrs['baseload_price']}\n")
                    if 'peakload_price' in df.attrs:
                        f.write(f"Peakload: {df.attrs['peakload_price']}\n")

            print(f"✓ Saved data for {date_str}: {len(df)} rows")
            success_count += 1
        else:
            print(f"✗ No data available for {date_str}")

        current_date += timedelta(days=1)

        # Be respectful - add a delay between requests
        time.sleep(3)

    print(f"\n{'='*60}")
    print(f"Completed: {success_count}/{days_back + 1} days processed successfully")
    return success_count


if __name__ == "__main__":
    import sys

    # Test continuous market
    if len(sys.argv) > 1 and sys.argv[1] == 'auction':
        print("Testing EPEX SPOT auction scraper with 2025-12-14...")
        df = scrape_epexspot_auction('2025-12-14', auction='GB-IDA1')

        if df is not None:
            print("\n" + "="*60)
            print("SAMPLE DATA (first 10 rows):")
            print("="*60)
            print(df.head(10).to_string())
            print(f"\nTotal periods: {len(df)}")
            print(f"Columns: {', '.join(df.columns.tolist())}")

            # Show summary data
            print("\n" + "="*60)
            print("SUMMARY DATA:")
            print("="*60)
            if hasattr(df, 'attrs'):
                if 'baseload_price' in df.attrs:
                    print(f"Baseload Price: {df.attrs['baseload_price']:.2f} £/MWh")
                if 'peakload_price' in df.attrs:
                    print(f"Peakload Price: {df.attrs['peakload_price']:.2f} £/MWh")

            # Show summary statistics
            print("\n" + "="*60)
            print("PERIOD STATISTICS:")
            print("="*60)
            print(f"Price: min={df['price'].min():.2f}, max={df['price'].max():.2f}, mean={df['price'].mean():.2f}")
            print(f"Total Volume: {df['volume'].sum():.1f} MWh")
        else:
            print("Failed to scrape auction data")

    else:
        print("Testing EPEX SPOT continuous market scraper with 2025-12-13...")
        df = scrape_epexspot('2025-12-13')

        if df is not None:
            print("\n" + "="*60)
            print("SAMPLE DATA (first 10 rows):")
            print("="*60)
            print(df.head(10).to_string())
            print(f"\nTotal periods: {len(df)}")
            print(f"Columns: {', '.join(df.columns.tolist())}")

            # Show summary statistics
            print("\n" + "="*60)
            print("SUMMARY STATISTICS:")
            print("="*60)
            print(f"Weight Avg Price: min={df['weight_avg_price'].min():.2f}, max={df['weight_avg_price'].max():.2f}, mean={df['weight_avg_price'].mean():.2f}")
            print(f"Total Volume: {df['volume'].sum():.1f} MWh")
        else:
            print("Failed to scrape data")

    # Uncomment to download historical data
    # print("\n\nStarting historical download...")
    # save_epexspot_history(days_back=14)
    # save_epexspot_auction_history(days_back=14, auction='GB-IDA1')
