import pandas as pd
import joblib
import os
import ssl

ssl._create_default_https_context = ssl._create_unverified_context
import os
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline

def download_data():
    url = "https://raw.githubusercontent.com/abbylmm/fake_job_posting/main/data/fake_job_postings.csv"
    print(f"Downloading dataset from {url}...")
    df = pd.read_csv(url)
    return df

def preprocess_and_train():
    # 1. Load Data
    df = download_data()
    
    # 2. Basic Preprocessing
    # We'll use a combination of title and description for text analysis
    df['text'] = df['title'].fillna('') + ' ' + df['description'].fillna('')
    
    # Target variable is 'fraudulent'
    X = df['text']
    y = df['fraudulent']
    
    print(f"Dataset shape: {df.shape}")
    print(f"Fake jobs: {y.sum()} / {len(y)}")
    
    # 3. Train/Test Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # 4. Create a Pipeline (TF-IDF + Random Forest)
    print("Training model...")
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(max_features=5000, stop_words='english')),
        ('clf', RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1))
    ])
    
    pipeline.fit(X_train, y_train)
    
    # 5. Evaluate
    score = pipeline.score(X_test, y_test)
    print(f"Model Accuracy on Test Set: {score:.4f}")
    
    # 6. Save the Model
    model_path = os.path.join(os.path.dirname(__file__), 'model.pkl')
    joblib.dump(pipeline, model_path)
    print(f"Model saved to {model_path}")

if __name__ == "__main__":
    preprocess_and_train()
