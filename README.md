# Autonomous FBA AI Agent (Streamlit Edition)

This repository contains the complete, enterprise-grade Python application for the Autonomous FBA AI Agent. It actively generates up to 150 elite, strictly-rule-abiding Amazon product niches and simulates a 24-hour scraping cycle log.

## GitHub to Streamlit Deployment Guide

Since this is now a pure Python Streamlit app, you can host it securely and for free via Streamlit Community Cloud.

### Step 1: Upload to GitHub
1. Create a free account on [GitHub](https://github.com).
2. Create a new **Public Repository** (e.g., `amazon-fba-agent`).
3. Upload exactly these 3 critical files into the main directory of your repository:
   - `app.py`
   - `data_engine.py`
   - `requirements.txt`
4. Commit your changes.

### Step 2: Deploy to Streamlit
1. Go to [Streamlit Community Cloud](https://share.streamlit.io/) and log in with your GitHub account.
2. Click **New App** -> **Deploy from GitHub**.
3. Select your repository from the dropdown. 
4. Ensure the Main file path is set to `app.py`.
5. Click **Deploy!**

Within 60 seconds, Streamlit will automatically read the `requirements.txt`, install pandas/streamlit, boot up the UI, and give you a global shareable link! 

## Local Testing
If you want to run it on your computer before uploading:
1. Make sure Python is installed.
2. Run `pip install -r requirements.txt`.
3. Stop the current process and run `streamlit run app.py`.
