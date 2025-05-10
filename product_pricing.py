import pandas as pd
import numpy as np
import requests
import matplotlib.pyplot as plt
import streamlit as st
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# --- API Setup ---
SERP_API_KEY = os.getenv("SERP_API_KEY")
SERP_BASE_URL = "https://serpapi.com/search"

# Function to fetch competitor prices from Google Shopping via SerpAPI
def fetch_competitor_prices(product_name):
    params = {
        "engine": "google_shopping",
        "q": product_name,
        "api_key": SERP_API_KEY
    }
    try:
        response = requests.get(SERP_BASE_URL, params=params)
        if response.status_code == 200:
            return response.json().get("shopping_results", [])
        else:
            return []
    except Exception as e:
        st.error(f"Error fetching competitor prices: {e}")
        return []

# Simulated function to estimate sales (based on competitor pricing)
def simulate_sales_estimation(current_price, competitor_prices):
    avg_competitor_price = np.mean([float(item['price'].replace('$', '').replace(',', '')) for item in competitor_prices])
    sales_estimate = max(1000 - (current_price - avg_competitor_price) * 100, 0)  # Simple linear model
    return sales_estimate

# Function to calculate suggested price (example: 5% above market average)
def calculate_suggested_price(competitor_prices):
    avg_competitor_price = np.mean([float(item['price'].replace('$', '').replace(',', '')) for item in competitor_prices])
    suggested_price = round(avg_competitor_price * 1.05, 2)  # 5% markup
    return suggested_price

# Function to create the price comparison plot
def plot_price_comparison(product_name, current_price, competitor_prices):
    prices = [current_price] + [float(item['price'].replace('$', '').replace(',', '')) for item in competitor_prices]
    labels = ['Your Price'] + [item['source'] for item in competitor_prices]

    fig, ax = plt.subplots()
    ax.bar(labels, prices, color=['blue'] + ['orange'] * len(competitor_prices))
    ax.set_title(f"Price Comparison for {product_name}")
    ax.set_ylabel("Price ($)")
    ax.set_xlabel("Store/Competitor")
    
    return fig