
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder



def load_and_preprocess_data(csv_file):
    # Load dataset
    df = pd.read_csv(csv_file)

    # Encode categorical variables if needed
    label_encoders = {}
    for column in df.select_dtypes(include=['object']).columns:
        le = LabelEncoder()
        df[column] = le.fit_transform(df[column])
        label_encoders[column] = le

    # Split data into X and y
    X = df.drop(columns=['Label'])
    y = df['Label']

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    return X_train, X_test, y_train, y_test, label_encoders
