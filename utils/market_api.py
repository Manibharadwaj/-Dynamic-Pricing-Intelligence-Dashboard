import streamlit as st
import pandas as pd
import numpy as np
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set page config
st.set_page_config(page_title="🛒 Dynamic Pricing Dashboard", layout="centered")
st.title("🧠 AI-Powered Dynamic Pricing Dashboard")

# --- API Setup ---
SERP_API_KEY = os.getenv("SERP_API_KEY")  # now hidden
SERP_BASE_URL = "https://serpapi.com/search"

# Function to get real market prices using SerpAPI
def fetch_google_prices(query, api_key):
    params = {
        "engine": "google_shopping",
        "q": query,
        "api_key": api_key
    }
    try:
        response = requests.get(SERP_BASE_URL, params=params)
        if response.status_code == 200:
            return response.json().get("shopping_results", [])
        else:
            return []
    except Exception as e:
        st.error(f"API error: {e}")
        return []

# Simulated model suggestion (fallback if API fails)
def simulated_model_price(current_price):
    fluctuation = np.random.uniform(-0.1, 0.15)  # -10% to +15%
    return round(current_price * (1 + fluctuation), 2)

# --- UI Elements ---
product_name = st.text_input("Enter Product Name:", "iPhone 14")
current_price = st.number_input("Your Current Selling Price ($):", min_value=1.0, step=0.5)

if st.button("Analyze Pricing"):
    with st.spinner("🔍 Fetching market data..."):
        market_data = fetch_google_prices(product_name, SERP_API_KEY)

    if market_data:
        st.success("✅ Live data fetched from Google Shopping")
        st.subheader("📊 Market Comparison Table")

        df = pd.DataFrame([
            {
                "Title": item.get("title"),
                "Store": item.get("source"),
                "Price": item.get("price")
            }
            for item in market_data
        ])
        df["Numeric_Price"] = df["Price"].str.replace(r"[^\d.]", "", regex=True).astype(float)

        avg_price = df["Numeric_Price"].mean()
        suggested_price = round(avg_price * 1.05, 2)  # 5% markup over market average

        st.dataframe(df[["Title", "Store", "Price"]], use_container_width=True)

        st.markdown(f"### 🧮 Average Market Price: **${avg_price:.2f}**")
        st.markdown(f"### 💡 Suggested Selling Price: **${suggested_price:.2f}**")

        if current_price < avg_price - 10:
            st.warning("Your price is too low. Consider increasing it.")
        elif current_price > avg_price + 10:
            st.info("Your price is above average. Check if you're offering premium value.")
        else:
            st.success("Your price is competitive!")

    else:
        st.error("❌ Couldn't fetch market data. Using simulated AI model suggestion.")
        fallback_price = simulated_model_price(current_price)
        st.markdown(f"💡 AI Model Suggests: **${fallback_price:.2f}**")

# Footer
st.markdown("""
<hr>
<div style='text-align: center; font-size: 14px;'>
📦 Powered by <b>SerpAPI + Streamlit</b> | 🔒 Secure & Private | 🧠 AI-Enhanced Pricing
</div>
""", unsafe_allow_html=True)