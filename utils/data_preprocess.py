import pandas as pd
from sklearn.preprocessing import LabelEncoder

def preprocess_data(data: pd.DataFrame):
    data = data.copy()
    
    required_columns = ['Category', 'Stock', 'Sales', 'Price']
    missing = [col for col in required_columns if col not in data.columns]

    if missing:
        raise ValueError(f"Missing required columns: {missing}")
    
    # Drop rows with missing values in required columns
    data = data.dropna(subset=required_columns)

    # Encode 'Category' if it's a string/categorical
    if data['Category'].dtype == object or data['Category'].dtype.name == 'category':
        le = LabelEncoder()
        data['Category'] = le.fit_transform(data['Category'])

    # Select features (X) and target (y)
    X = data[['Category', 'Stock', 'Sales']]
    y = data['Price']

    return X, y