import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os
import io
import plotly.express as px
import plotly.graph_objects as go
from utils.data_preprocess import preprocess_data
from utils.parser import parse_pdf, parse_docx, extract_financials_from_text

# Load ML model
MODEL_PATH = "model/pricing_model.pkl"
model = joblib.load(MODEL_PATH) if os.path.exists(MODEL_PATH) else None

st.set_page_config(page_title="Dynamic Pricing Dashboard", layout="wide")
st.title("💰 Dynamic Pricing Intelligence Dashboard")
st.sidebar.header("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Upload & Analyze Data", "Upload a Product", "About"])

# ----------------------------- Enhanced Home Page -----------------------------
if page == "Home":
    st.markdown("""
    <div style="background-color: #282828; color: white; padding: 20px; border-radius: 10px; text-align: center;">
        <h2>Welcome to the Dynamic Pricing Intelligence Dashboard!</h2>
        <p>Optimize your pricing strategy with AI-powered insights. Upload your sales data to get intelligent pricing recommendations.</p>
    </div>
    """, unsafe_allow_html=True)

# Simulated competitor price function
def get_competitor_prices(product_name):
    return pd.DataFrame({
        'Competitor': [f"Seller {i+1}" for i in range(5)],
        'Price': np.round(np.random.uniform(20, 200, 5), 2),
        'Sales/Year': np.random.randint(100, 1000, 5)
    })

# Simulated market price function
def get_market_price(product_name):
    return round(np.random.uniform(20, 200), 2)

# -------------- HOME PAGE --------------
if page == "Home":
    st.markdown("""
    """, unsafe_allow_html=True)

# -------------- UPLOAD & ANALYZE PAGE --------------
elif page == "Upload & Analyze Data":
    uploaded_file = st.file_uploader("📤 Upload your data file", type=["csv", "pdf", "docx"])

    if uploaded_file:
        file_type = uploaded_file.type

        if file_type == "text/csv":
            try:
                data = pd.read_csv(uploaded_file)
                st.subheader("📊 Uploaded Data")
                st.dataframe(data.head())

                if 'Price' not in data.columns or 'Product' not in data.columns:
                    st.error("❌ CSV must contain both 'Product' and 'Price' columns.")
                elif model is None:
                    st.error("❌ Trained model not found at model/pricing_model.pkl.")
                else:
                    if 'Market_Price' not in data.columns:
                        data['Market_Price'] = data['Product'].apply(get_market_price)

                    if 'Category' in data.columns:
                        data = pd.get_dummies(data, columns=['Category'], drop_first=True)

                    numeric_cols = [col for col in data.columns if data[col].dtype in [np.float64, np.int64]]

                    if hasattr(model, 'feature_names_in_'):
                        expected_cols = model.feature_names_in_
                        for col in expected_cols:
                            if col not in data.columns:
                                data[col] = 0
                        X = data[expected_cols]
                    else:
                        st.error("❌ Model missing 'feature_names_in_' attribute.")
                        X = data[numeric_cols]

                    data['Suggested_Sell_Price'] = model.predict(X)

                    data['Price_Advice'] = data.apply(
                        lambda row: 'Raise Price' if row['Suggested_Sell_Price'] > row['Price'] + 5
                        else ('Lower Price' if row['Suggested_Sell_Price'] < row['Price'] - 5 else 'Competitive'),
                        axis=1
                    )

                    st.subheader("📦 Price Strategy Suggestions")
                    st.dataframe(data[['Product', 'Price', 'Market_Price', 'Suggested_Sell_Price', 'Price_Advice']])

                    bar_fig = go.Figure()
                    bar_fig.add_trace(go.Bar(x=data['Product'], y=data['Price'], name='Current Price', marker_color='indianred'))
                    bar_fig.add_trace(go.Bar(x=data['Product'], y=data['Market_Price'], name='Market Price', marker_color='lightgreen'))
                    bar_fig.update_layout(title='💹 Product vs Market Price', barmode='group')
                    st.plotly_chart(bar_fig)

                    st.subheader("🧠 Price Strategy Breakdown")
                    pie_fig = px.pie(values=data['Price_Advice'].value_counts().values,
                                     names=data['Price_Advice'].value_counts().index,
                                     title="Suggested Pricing Actions")
                    st.plotly_chart(pie_fig)

                    st.markdown("📄 **Expected CSV Columns:** Product, Category (optional), Stock, Sales, Price, Market_Price (optional)")
                    sample_csv = """Product,Category,Stock,Sales,Price,Market_Price\nShirt,Clothing,120,200,25.99,30.00\nJeans,Clothing,80,150,49.99,55.00"""
                    st.download_button("⬇️ Download Sample CSV", data=sample_csv, file_name="sample.csv", mime="text/csv")

            except Exception as e:
                st.error(f"❌ Error reading CSV: {e}")

        elif file_type in ["application/pdf", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]:
            try:
                text = parse_pdf(uploaded_file) if file_type.endswith("pdf") else parse_docx(uploaded_file)
                st.subheader("📄 Parsed Text")
                st.text_area("Extracted Text", text, height=300)

                financials = extract_financials_from_text(text)
                st.subheader("💰 Extracted Financials")
                st.write(financials)

                excel_buffer = io.BytesIO()
                with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
                    pd.DataFrame([text], columns=["Text"]).to_excel(writer, sheet_name="Raw Text", index=False)
                    pd.DataFrame.from_dict(financials, orient="index", columns=["Amount"]).to_excel(writer, sheet_name="Financials")

                    df_chart = pd.DataFrame.from_dict({k: v for k, v in financials.items() if isinstance(v, (int, float))}, orient="index", columns=["Amount"])
                    df_chart.to_excel(writer, sheet_name="Chart Data")
                    workbook = writer.book
                    worksheet = writer.sheets["Chart Data"]
                    chart = workbook.add_chart({'type': 'column'})
                    chart.add_series({
                        'categories': ['Chart Data', 1, 0, len(df_chart), 0],
                        'values':     ['Chart Data', 1, 1, len(df_chart), 1],
                        'name':       'Financial Metrics'
                    })
                    worksheet.insert_chart('D2', chart)

                st.download_button("📥 Download Financial Report", data=excel_buffer.getvalue(), file_name="Report.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

            except Exception as e:
                st.error(f"❌ Failed to parse document: {e}")

        else:
            st.warning("⚠️ Unsupported file type.")

# -------------- NEW: UPLOAD A PRODUCT PAGE --------------
elif page == "Upload a Product":
    st.subheader("🛍️ Upload a Product for Smart Pricing")
    with st.form("product_form"):
        product_name = st.text_input("Product Name")
        category = st.text_input("Category")
        price = st.number_input("Your Price ($)", min_value=1.0, value=50.0)
        image = st.file_uploader("Upload Product Image (optional)", type=["jpg", "png"])
        submitted = st.form_submit_button("🔍 Analyze Pricing")

    if submitted and product_name:
        st.info(f"Fetching competitor data for '{product_name}'...")

        competitors = get_competitor_prices(product_name)
        suggested_price = round(competitors['Price'].mean() * 1.05, 2)  # slight margin
        advice = "Raise Price" if suggested_price > price + 5 else ("Lower Price" if suggested_price < price - 5 else "Looks Good")

        st.subheader("📈 Competitor Pricing Overview")
        st.dataframe(competitors)

        st.subheader("💡 Our Recommendation")
        st.markdown(f"""
        - **Your Price:** ${price:.2f}  
        - **Suggested Price:** ${suggested_price:.2f}  
        - **Advice:** 🧠 **{advice}**
        """)

        fig = go.Figure()
        fig.add_trace(go.Box(y=competitors['Price'], name="Competitor Prices"))
        fig.add_trace(go.Scatter(y=[price], x=["Your Price"], mode='markers+text', name='Your Price', textposition="top center"))
        fig.add_trace(go.Scatter(y=[suggested_price], x=["Suggested"], mode='markers+text', name='Suggested Price', textposition="top center"))
        st.plotly_chart(fig)

# -------------- ABOUT PAGE --------------
elif page == "About":
    st.markdown("""
    <div style=" border-radius: 10px; padding: 20px;">
        <h3 style="text-align: center; color: #2D9CDB;">About This Dashboard</h3>
        <p style="font-size: 18px; line-height: 1.6;">
            This AI-powered platform helps businesses optimize pricing strategies using machine learning algorithms and market simulation.
            By analyzing competitor prices and product data, it recommends the optimal pricing strategies for your products, improving your sales performance.
        </p>
        <h4 style="color: #2D9CDB;">Key Features:</h4>
        <ul style="font-size: 16px;">
            <li>Intelligent pricing suggestions based on market data</li>
            <li>Competitor price comparison and market analysis</li>
            <li>Real-time dynamic pricing updates</li>
            <li>Detailed financial reports and recommendations</li>
        </ul>
    </div>
                
    <div style="text-align: center; margin-top: 30px;">
        <a href="static/research-paper.docx" download>
            <button style="background-color: #2D9CDB; color: white; padding: 10px 20px; border: none; border-radius: 5px; font-size: 16px; cursor: pointer;">
                📄 Download Research Paper
            </button>
        </a>
    </div>
""", unsafe_allow_html=True)
# ----------------------------- Enhanced Footer -----------------------------
footer_style = """
<style>
.footer {
    text-align: center;
    font-size: 14px;
    padding: 20px;
    position: fixed;
    bottom: 0;
    width: 100%;
    background-color: #222;
    color: #fff;
    font-family: Arial, sans-serif;
}
.footer a {
    color: #f1f1f1;
    text-decoration: none;
}
.footer a:hover {
    text-decoration: underline;
}
</style>
<div class="footer">
    <p>📊 Powered by <strong>Dynamic Pricing AI</strong> | © 2025 | <a href="https://github.com/yourrepo" target="_blank">GitHub</a></p>
</div>
"""
st.markdown(footer_style, unsafe_allow_html=True)