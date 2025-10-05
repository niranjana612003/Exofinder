import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import joblib
import os

DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'combined.csv')

df = pd.read_csv(DATA_PATH)

mapping = {
    'CONFIRMED': 'planet',
    'CANDIDATE': 'planet',
    'PC': 'planet',
    'KP': 'planet',
    'FALSE POSITIVE': 'non-planet',
    'FP': 'non-planet'
}
df['label'] = df['disposition'].str.upper().map(mapping)
df = df.dropna(subset=['label'])

features = ['orbital_period', 'transit_duration', 'planet_radius', 'transit_depth', 'snr']
features = [f for f in features if f in df.columns]

X = df[features]
y = (df['label'] == 'planet').astype(int)

X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, test_size=0.2, random_state=42)

pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler()),
    ('clf', RandomForestClassifier(n_estimators=200, random_state=42))
])

pipeline.fit(X_train, y_train)

y_pred = pipeline.predict(X_test)
print(classification_report(y_test, y_pred))

MODEL_PATH = os.path.join(os.path.dirname(__file__), 'model', 'pipeline.joblib')
os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
joblib.dump(pipeline, MODEL_PATH)
print(f"✅ Model saved to {MODEL_PATH}")
