# Irradiance Data Extractor

## Overview
The **Irradiance Data Extractor** is a web-based application that allows users to extract hourly irradiance data for a given location and time range. Users can input latitude and longitude coordinates, specify a date range, and choose the hours of interest to retrieve irradiance data. The application provides real-time progress updates, dynamically displays extracted data, and allows users to download the results in CSV or Excel format.

Built with **Streamlit**, this app uses multithreading to ensure efficient and fast data extraction, making it suitable for both small-scale and large-scale data retrieval.

---

## Features
- Input location via latitude and longitude.
- Specify date and time range for data extraction.
- Real-time progress updates during data extraction.
- Dynamically display extracted data as it is retrieved.
- Download extracted data in CSV or Excel format.
- Interactive visualization of hourly irradiance over time.

---

## Installation
### Prerequisites
Ensure the following are installed on your system:
1. **Python 3.8 or higher**
2. **Pip** (Python package manager)

### Clone the Repository
```bash
git clone https://github.com/your-username/irradiance-data-extractor.git
cd irradiance-data-extractor
```

### Install Dependencies
1. Create a virtual environment (optional but recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Install Playwright (used for fetching data):
   ```bash
   playwright install
   ```

---

## Usage
### Running the Application Locally
1. Start the Streamlit app:
   ```bash
   streamlit run app.py
   ```

2. Open the URL displayed in the terminal (default: `http://localhost:8501`) in your web browser.

---

## How to Use the Application
1. **Location Input**:
   - Enter the latitude and longitude coordinates for the location of interest.

2. **Date and Time Range**:
   - Specify the start and end dates.
   - Select the start and end hours for each day.

3. **Data Points**:
   - The app will display the total number of data points to be extracted.

4. **Estimate Time**:
   - Click the **Estimate Extraction Time** button to measure the average call duration and see the expected total extraction time.

5. **Start Extraction**:
   - Click the **Start Extraction** button to begin data retrieval.
   - Monitor the real-time progress bar and dynamically updated data table.

6. **Download Data**:
   - Once extraction is complete, download the data in CSV or Excel format.

7. **Visualize Data**:
   - Navigate to the **Visualization** tab to view an interactive graph of hourly irradiance over time.

---

## Deployment
To deploy the application on a remote server or cloud platform, follow these steps:

### Using Docker
1. **Build the Docker Image**:
   ```bash
   docker build -t irradiance-extractor .
   ```

2. **Run the Docker Container**:
   ```bash
   docker run -p 8501:8501 irradiance-extractor
   ```

3. Access the app at `http://localhost:8501`.

---

## Directory Structure
```
irradiance-data-extractor/
├── app.py                     # Main Streamlit app
├── extract.py                 # Data extraction logic
├── requirements.txt           # Python dependencies
├── README.md                  # Documentation
├── Dockerfile                 # Docker configuration (if deploying via Docker)
└── venv/                      # Virtual environment (optional)
```

---

## Contributing
Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Submit a pull request with a detailed explanation of your changes.

---

## License
This project is licensed under the [MIT License](LICENSE).

---

## Troubleshooting
1. **Playwright Errors**:
   - Ensure Playwright is installed:
     ```bash
     playwright install
     ```
   - Verify that your browser is supported by Playwright.

2. **Streamlit Not Found**:
   - Install Streamlit:
     ```bash
     pip install streamlit
     ```

3. **Dependencies Not Installed**:
   - Re-run the installation command:
     ```bash
     pip install -r requirements.txt
     ```