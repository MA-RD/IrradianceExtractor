import streamlit as st
from datetime import datetime, timedelta
from extract import fetch_irradiance
import pandas as pd
import plotly.express as px
from concurrent.futures import ThreadPoolExecutor
import threading
import time


def fetch_data_parallel_with_progress(latitude, longitude, start_date, end_date, start_hour, end_hour):
    """
    Fetch data in parallel for the given date range and hour range, with progress updates.
    """
    progress_lock = threading.Lock()  # Lock for thread-safe updates
    data_lock = threading.Lock()  # Lock for shared data updates
    progress = {"current": 0, "total": 0}
    shared_data = []

    def fetch_for_day(date):
        nonlocal progress, shared_data
        day_data = fetch_irradiance(latitude, longitude, date, date, start_hour, end_hour)
        
        # Update progress safely
        with progress_lock:
            progress["current"] += (end_hour - start_hour + 1)
        
        # Append to shared data safely
        with data_lock:
            shared_data.append(day_data)

    # Generate list of dates
    dates = [start_date + timedelta(days=i) for i in range((end_date - start_date).days + 1)]
    progress["total"] = len(dates) * (end_hour - start_hour + 1)

    # Use ThreadPoolExecutor for parallel execution
    with ThreadPoolExecutor() as executor:
        list(executor.map(fetch_for_day, dates))

    # Combine all results into a single DataFrame
    return pd.concat(shared_data, ignore_index=True), progress


def main():
    st.set_page_config(page_title="Irradiance Data Extractor", layout="wide")
    st.title("☀️ Irradiance Data Extractor")
    st.markdown("Extract hourly irradiance data for a given location and time range.")

    tabs = st.tabs(["📍 Location & Inputs", "📊 Extracted Data", "📈 Visualization"])

    with tabs[0]:
        st.header("📍 Location & Inputs")

        # Manual coordinate input
        st.markdown("### Enter Location Coordinates:")
        default_coords = [48.85826, 2.29451]  # Eiffel Tower
        latitude = st.number_input("Latitude", value=default_coords[0], format="%.5f")
        longitude = st.number_input("Longitude", value=default_coords[1], format="%.5f")
        st.write(f"Selected Location: Latitude {latitude:.5f}, Longitude {longitude:.5f}")

        # Date range and hour range inputs
        st.markdown("### Select Date and Time Range:")
        start_date = st.date_input("Start Date", datetime(2023, 1, 1))
        end_date = st.date_input("End Date", datetime(2023, 1, 7))
        start_hour = st.slider("Start Hour", 0, 23, 6)
        end_hour = st.slider("End Hour", 0, 23, 18)

        # Number of data points
        total_days = (end_date - start_date).days + 1
        total_hours = (end_hour - start_hour + 1) * total_days
        st.info(f"Total data points to be extracted: {total_hours}")

        # Measure average call time
        if st.button("Estimate Extraction Time"):
            st.info("Measuring average call time... Please wait.")
            test_date = start_date
            start_time = time.time()
            fetch_irradiance(latitude, longitude, test_date, test_date, start_hour, end_hour)
            avg_call_time = time.time() - start_time
            st.session_state["avg_call_time"] = avg_call_time
            st.success(f"Average call time measured: {avg_call_time:.2f} seconds")

        # Expected time
        if "avg_call_time" in st.session_state:
            expected_time = st.session_state["avg_call_time"] * total_hours / total_days
            st.info(f"Expected total time: {expected_time:.2f} seconds (parallelized).")

        # Start data extraction
        if st.button("Start Extraction"):
            st.session_state["fetch_data"] = True
            st.session_state["extracted_data"] = []

    with tabs[1]:
        st.header("📊 Extracted Data")
        if st.session_state.get("fetch_data"):
            progress_bar = st.progress(0)
            data_placeholder = st.empty()

            # Fetch data with progress
            data, progress = fetch_data_parallel_with_progress(
                latitude, longitude, start_date, end_date, start_hour, end_hour
            )

            # Update progress and display data in real-time
            while progress["current"] < progress["total"]:
                progress_bar.progress(progress["current"] / progress["total"])
                data_placeholder.dataframe(pd.concat(st.session_state["extracted_data"], ignore_index=True))
            
            # Final updates
            st.session_state["extracted_data"] = data
            progress_bar.progress(1.0)
            st.success("✅ Data extraction complete!")
            st.dataframe(data)

            # Download options
            csv = data.to_csv(index=False)
            xlsx = data.to_excel("irradiance.xlsx", index=False)

            st.download_button("📥 Download CSV", csv, "irradiance.csv")
            st.download_button("📥 Download Excel", open("irradiance.xlsx", "rb"), "irradiance.xlsx")

    with tabs[2]:
        st.header("📈 Visualization")
        data = st.session_state.get("extracted_data")
        if data is not None and not data.empty:
            fig = px.line(data, x="hour", y="irradiance", color="date", title="Hourly Irradiance")
            st.plotly_chart(fig)
        else:
            st.info("No data to visualize. Perform extraction first.")


if __name__ == "__main__":
    main()
