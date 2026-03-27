import pandas as pd
import numpy as np
import pickle

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier
from imblearn.over_sampling import RandomOverSampler

# ─── Load Dataset ─────────────────────────────────────────────
df = pd.read_csv("fertilizer_dataset.csv")

# ─── Features & Target ────────────────────────────────────────
X = df.drop("Fertilizer_Name", axis=1)
y = df["Fertilizer_Name"]

# ─── Encode Categorical (Soil Color etc.) ─────────────────────
X = pd.get_dummies(X)

# ─── Save column order (VERY IMPORTANT) ───────────────────────
columns = X.columns

# ─── Encode Labels ────────────────────────────────────────────
le = LabelEncoder()
y_encoded = le.fit_transform(y)

# ─── Balance Dataset (CRITICAL FIX) ───────────────────────────
ros = RandomOverSampler(random_state=42)
X_res, y_res = ros.fit_resample(X, y_encoded)

# ─── Scale Features ───────────────────────────────────────────
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_res)

# ─── Train/Test Split ─────────────────────────────────────────
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y_res, test_size=0.2, random_state=42
)

# ─── Train Model ──────────────────────────────────────────────
model = RandomForestClassifier(
    n_estimators=300,
    max_depth=None,
    class_weight='balanced',
    random_state=42
)

model.fit(X_train, y_train)

# ─── Accuracy Check ───────────────────────────────────────────
print("Train Accuracy:", model.score(X_train, y_train))
print("Test Accuracy:", model.score(X_test, y_test))

# ─── Save Everything ──────────────────────────────────────────
pickle.dump(model, open("fertilizer_recommendation.pkl", "wb"))
pickle.dump(le, open("fertilizer_le.pkl", "wb"))
pickle.dump(list(columns), open("fertilizer_columns.pkl", "wb"))
pickle.dump(scaler, open("fertilizer_scaler.pkl", "wb"))