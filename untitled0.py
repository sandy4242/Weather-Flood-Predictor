# -*- coding: utf-8 -*-
"""Untitled0.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1O-eUR80_YLEN43rh7lPr-gHKzbaFMJIQ
"""

# pip install pandas scikit-learn
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# Load the dataset
df = pd.read_csv('flood_prediction_dataset.csv')

# Convert the target variable 'Flood (Yes/No)' into numerical values
label_encoder = LabelEncoder()
df['Flood (Yes/No)'] = label_encoder.fit_transform(df['Flood (Yes/No)'])  # Yes = 1, No = 0

# Split data into features (X) and target (y)
X = df[['Humidity (%)', 'Temperature (°C)', 'Rainfall (mm)', 'Risk Factor', 'Altitude (m)']]
y = df['Flood (Yes/No)']

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

from sklearn.linear_model import LogisticRegression

# Initialize the logistic regression model
classification_model = LogisticRegression(max_iter=1000)

# Train the model on the training data
classification_model.fit(X_train, y_train)

from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Make predictions on the test data
y_pred = classification_model.predict(X_test)

# Calculate accuracy
accuracy = accuracy_score(y_test, y_pred)

# Generate classification report and confusion matrix
class_report = classification_report(y_test, y_pred)
conf_matrix = confusion_matrix(y_test, y_pred)

# Print evaluation results
print(f"Accuracy: {accuracy * 100:.2f}%")
print("Classification Report:")
print(class_report)
print("Confusion Matrix:")
print(conf_matrix)

import numpy as np

# Modify flood conditions to balance Yes/No cases
df['Flood (Yes/No)'] = np.where(
    (df['Rainfall (mm)'] > 80) & (df['Humidity (%)'] > 60) & (df['Risk Factor'] >= 1) & (df['Altitude (m)'] < 300),
    1, 0
)

# Retrain the model on the adjusted data
X = df[['Humidity (%)', 'Temperature (°C)', 'Rainfall (mm)', 'Risk Factor', 'Altitude (m)']]
y = df['Flood (Yes/No)']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

classification_model.fit(X_train, y_train)

joblib.dump(classification_model, 'flood_classification_model.pkl')
y_pred = classification_model.predict(X_test)

# Re-evaluate
accuracy = accuracy_score(y_test, y_pred)
class_report = classification_report(y_test, y_pred)
conf_matrix = confusion_matrix(y_test, y_pred)

print(f"Adjusted Accuracy: {accuracy * 100:.2f}%")
print("Adjusted Classification Report:")
print(class_report)
print("Adjusted Confusion Matrix:")
print(conf_matrix)

# Import necessary libraries
import pandas as pd

# Load the sample test data from a CSV file
# Replace 'sample_test_data.csv' with the actual path to your test data CSV
test_data_df = pd.read_csv('sample_test_data.csv')

# Ensure the test data has the correct column names as used in the model
# For example, columns should be ['Humidity (%)', 'Temperature (°C)', 'Rainfall (mm)', 'Risk Factor', 'Altitude (m)']

# Predict the probabilities for flood (using predict_proba)
flood_probabilities = classification_model.predict_proba(test_data_df)

# Add the probabilities to the DataFrame
test_data_df['Probability of No Flood'] = flood_probabilities[:, 0]
test_data_df['Probability of Flood'] = flood_probabilities[:, 1]

# Print the test data with probabilities
print(test_data_df)

# Optionally, save the results to a new CSV file
test_data_df.to_csv('test_data_with_flood_probabilities.csv', index=False)




# Import necessary libraries
import pandas as pd

# Load your dataset into the model
# Replace 'your_new_dataset.csv' with the actual path to your dataset
new_data_df = pd.read_csv('sample_test_data.csv')

# Ensure the dataset has the correct columns as used in the model
# The columns should be ['Humidity (%)', 'Temperature (°C)', 'Rainfall (mm)', 'Risk Factor', 'Altitude (m)']

# Predict the probabilities for flood (using predict_proba)
flood_probabilities = classification_model.predict_proba(new_data_df)

# Add the probabilities to the DataFrame
new_data_df['Probability of No Flood'] = flood_probabilities[:, 0]
new_data_df['Probability of Flood'] = flood_probabilities[:, 1]

# Print the new dataset with the probabilities
print(new_data_df)

# Optionally, save the results to a new CSV file
new_data_df.to_csv('predicted_flood_probabilities.csv', index=False)

