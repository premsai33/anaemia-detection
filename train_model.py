import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.preprocessing import LabelEncoder, StandardScaler

# ==============================
# 1️⃣ Load Large Dataset
# ==============================

df = pd.read_csv("wearable_anemia_large_dataset.csv")

print("Dataset Loaded Successfully")
print("Total rows:", len(df))
print("\n")

# ==============================
# 2️⃣ Encode Categorical Data
# ==============================

le = LabelEncoder()
df["Gender"] = le.fit_transform(df["Gender"])  # Male=1, Female=0

# ==============================
# 3️⃣ Select Features
# ==============================

X = df[["Age", "Gender", "SleepHours", "HeartRate", "SpO2", "Steps"]]
y = df["Anaemia"]

# ==============================
# 4️⃣ Feature Scaling
# ==============================

scaler = StandardScaler()
X = scaler.fit_transform(X)

# ==============================
# 5️⃣ Train-Test Split
# ==============================

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# ==============================
# 6️⃣ Train Logistic Regression
# ==============================

model = LogisticRegression(
    max_iter=1000,
    class_weight='balanced'
)

model.fit(X_train, y_train)

# ==============================
# 7️⃣ Evaluate Model
# ==============================

y_pred = model.predict(X_test)

print("Accuracy:", accuracy_score(y_test, y_pred))
print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# ==============================
# 8️⃣ Save Model + Scaler
# ==============================

joblib.dump(model, "anemia_model.pkl")
joblib.dump(scaler, "scaler.pkl")

print("\nModel and scaler saved successfully.")
