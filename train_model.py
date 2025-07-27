import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

# Load the dataset
df = pd.read_csv("dataset/Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv")

# Drop any rows with missing values
df = df.dropna()

# Separate features and label
X = df.drop(columns=[' Label'])  # Note the space before 'Label'
y = df[' Label']

# Convert all features to numeric (ignore any conversion errors)
X = X.apply(pd.to_numeric, errors='coerce').fillna(0)

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

# Train a random forest classifier
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Predict on test data
y_pred = model.predict(X_test)

# Print the evaluation results
print(classification_report(y_test, y_pred))
