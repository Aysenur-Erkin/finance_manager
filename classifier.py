import os
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from typing import List, Dict


class ExpenseClassifier:
    def __init__(self, model_path: str = "expense_classifier.joblib"):
        self.model_path = model_path
        self.vectorizer = TfidfVectorizer()
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        if os.path.exists(self.model_path):
            self._load_model()

    def train(self, data: List[Dict]):
        texts = [item['description'] for item in data]
        labels = [item['category'] for item in data]
        X = self.vectorizer.fit_transform(texts)
        self.model.fit(X, labels)

    def predict_category(self, description: str) -> str:
        if not hasattr(self.model, 'classes_'):
            return 'Unknown'
        X = self.vectorizer.transform([description])
        return self.model.predict(X)[0]

    def save_model(self):
        joblib.dump({
            'vectorizer': self.vectorizer,
            'model': self.model
        }, self.model_path)

    def _load_model(self):
        data = joblib.load(self.model_path)
        self.vectorizer = data['vectorizer']
        self.model = data['model']
