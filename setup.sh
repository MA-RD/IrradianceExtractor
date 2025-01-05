#!/bin/bash

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Installing Playwright..."
playwright install

echo "Setup complete. Run the app using: streamlit run app/app.py"
