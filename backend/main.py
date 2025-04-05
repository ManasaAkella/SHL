from fastapi import FastAPI
import pandas as pd
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="SHL Assessment Recommendation System",
    description="🚀 Recommend SHL assessments based on skills",
    version="0.1.0"
)

# CORS setup so frontend can access backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "🎯 SHL Assessment Recommendation System is live and kickin’!"}

@app.get("/recommend_assessments")
def recommend(skill: str):
    try:
        print("📥 Received skill:", skill)
        
        # Load your CSV file fresh every time
        df = pd.read_csv("shl_assessments.csv")
        print("🧠 Columns in CSV:", df.columns)
        print("🔍 First few rows:\n", df.head())

        if 'Skills' not in df.columns:
            return {"error": "CSV file is missing 'Skills' column 😬"}

        matching = df[df['Skills'].str.contains(skill, case=False, na=False)]

        if matching.empty:
            print("❌ No matching assessments found.")
            return {"message": f"No assessments found for skill: '{skill}' 😢"}

        # Use the actual column names from your CSV
        results = matching[['Name', 'Skills', 'URL']].to_dict(orient="records")
        print("✅ Recommendations found:", results)
        return results

    except Exception as e:
        print("💥 Internal Server Error:", str(e))
        return {"error": "Something went wrong on the server 😓"}
