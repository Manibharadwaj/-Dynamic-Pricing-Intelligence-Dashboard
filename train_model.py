# train_model.py
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder

# Load and preprocess training data
df = pd.read_csv('sample_data/ecommerce_sales.csv')

# Encode 'Category' (if categorical)
if 'Category' in df.columns:
    df = pd.get_dummies(df, columns=['Category'], drop_first=True)

# Define features and target
X = df.drop(columns=['Product', 'Price'])  # Drop target + unused cols
y = df['Price']

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Save model
joblib.dump(model, 'model/pricing_model.pkl')
print("✅ Model trained and saved.")