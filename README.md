# Dynamic Pricing Intelligence Dashboard

## 🚀 Overview

The **Dynamic Pricing Intelligence Dashboard** is an AI-powered platform that helps businesses optimize pricing strategies using machine learning algorithms. The dashboard analyzes e-commerce sales data, predicts pricing models, and offers dynamic pricing suggestions based on customer behavior and competitor data.

This project is built using Python, Streamlit, Plotly, and machine learning models to help businesses increase profitability by automating pricing decisions and improving pricing strategies.

---

## 🛠️ Features

- **Upload & Analyze Data**: Upload your e-commerce sales or inventory dataset and receive intelligent pricing recommendations.
- **Dynamic Pricing Suggestions**: Get real-time dynamic pricing recommendations based on historical sales data and machine learning models.
- **Competitor Price Analysis**: Compare your prices with competitor data to ensure competitive pricing.
- **Data Visualization**: Interactive charts and graphs to help visualize your sales trends, pricing insights, and customer segmentation.
- **Model Integration**: Integrated machine learning model that predicts optimal pricing based on uploaded data.
- **Easy Deployment**: Run the dashboard locally or deploy it to the web with minimal setup.

---

## 📈 Technologies Used

- **Python**: Main programming language.
- **Streamlit**: Used for building the interactive dashboard.
- **Plotly**: Data visualization for charts and graphs.
- **Machine Learning**: Pricing model built using machine learning techniques (e.g., regression, clustering).
- **Pandas & NumPy**: Data manipulation and analysis.
- **Joblib**: Model serialization for saving/loading the machine learning model.

---

## 📝 Setup Instructions

### 1. Clone the repository

git clone git@github.com:Manibharadwaj/-Dynamic-Pricing-Intelligence-Dashboard.git
cd Dynamic-Pricing-Intelligence-Dashboard

2. Set up the virtual environment

Create and activate a virtual environment:

On macOS/Linux:

python3 -m venv venv
source venv/bin/activate

On Windows:

python -m venv venv
.\venv\Scripts\activate


3. Install dependencies

Install the required Python packages:

pip install -r requirements.txt

4. Run the application

Start the Streamlit app:

streamlit run app.py


---

📊 How to Use

1. Home: Introduction to the project and overview of the platform.


2. Upload & Analyze Data: Upload your e-commerce sales data in CSV format. The app will process the data and generate insights, including pricing recommendations.


3. Upload a Product: Upload product-specific details for personalized pricing predictions.


4. About: Learn more about the platform and download the research paper (coming soon).




---

🔄 Model Training

The machine learning model used for pricing predictions is stored in the model/ folder as pricing_model.pkl. If you need to retrain the model, follow these steps:

1. Prepare your training data.


2. Run train_model.py to train the model and save it as pricing_model.pkl.


3. Once trained, replace the model file in the model/ folder.




---

📂 Project Structure

Dynamic-Pricing-Intelligence-Dashboard/
│
├── app.py                   # Main Streamlit app
├── train_model.py           # Model training script
├── model/                   # Folder containing the trained model
│   └── pricing_model.pkl    # Saved pricing model
├── utils/                   # Utility functions for data processing and parsing
│   ├── data_preprocess.py   # Data preprocessing functions
│   └── parser.py            # Functions for parsing uploaded files
├── static/                  # Static files like research papers, images, etc.
│   └── research-paper.pdf   # PDF of the research paper
├── requirements.txt         # Python dependencies
└── README.md                # Project documentation


---

📝 License

This project is licensed under the MIT License - see the LICENSE file for details.


---

📞 Contact

If you have any questions, feel free to reach out to the project maintainer:

Manibharadwaj
GitHub: @Manibharadwaj
Email: manibharadwajcr@gmail.com


---

💡 Future Enhancements

Integrate more machine learning models for different pricing strategies.

Provide real-time competitor data analysis using web scraping or third-party APIs.

Add support for other file types like Excel or JSON.

Implement user authentication and role-based access for the dashboard.



---

🎉 Acknowledgements

Special thanks to all contributors and resources that helped in making this project a reality. This includes various open-source tools and libraries, as well as the contributors to machine learning practices for dynamic pricing models.
