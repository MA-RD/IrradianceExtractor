from playwright.sync_api import sync_playwright
import pandas as pd
from datetime import datetime, timedelta


def fetch_irradiance(latitude, longitude, start_date, end_date, start_hour, end_hour):
    """
    Extract hourly irradiance data for a given location, date range, and hour range.
    """
    data = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        current_date = start_date
        while current_date <= end_date:
            for hour in range(start_hour, end_hour + 1):
                # Format date and time for the URL
                formatted_date = current_date.strftime("%Y.%m.%d")
                formatted_time = f"{hour:02}:00"

                # Navigate to the URL
                url = f"https://suncalc.org/#/{latitude},{longitude},17/{formatted_date}/{formatted_time}/324.0/2"
                page.goto(url)

                # Wait for data to load
                page.wait_for_load_state("networkidle")

                # Extract irradiance value
                irradiance = page.eval_on_selector("#sE_e", "element => element.textContent")
                data.append({
                    "date": current_date.strftime("%Y-%m-%d"),
                    "hour": formatted_time,
                    "irradiance": irradiance.strip()
                })

            # Move to the next day
            current_date += timedelta(days=1)

        browser.close()

    # Convert to DataFrame
    df = pd.DataFrame(data)
    return df
