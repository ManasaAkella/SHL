from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd

app = FastAPI(
    title="SHL Assessment Recommendation System",
    description="🚀 Recommends SHL assessments based on skills or job descriptions",
    version="0.1.0"
)

# 💫 CORS Setup: Allow frontend from anywhere to talk to us!
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "🎯 SHL Assessment Recommendation System is LIVE! Ping me with skills to get started!"}

@app.get("/recommend_assessments")
def recommend(skill: str):
    try:
        print("📥 Skill received:", skill)

        # 🚨 Load CSV each time to get latest updates (or cache this later)
        df = pd.read_csv("shl_assessments.csv")

        # ✅ Debug print
        print("🧠 Columns loaded:", df.columns.tolist())

        if 'Skills' not in df.columns:
            return {"error": "CSV is missing the 'Skills' column 😬"}

        # 🔍 Case-insensitive match
        matches = df[df['Skills'].str.contains(skill, case=False, na=False)]

        if matches.empty:
            return {"message": f"No assessments found for '{skill}' 😢"}

        # 🎯 Limit to top 10, clean output
        top_matches = matches[['Name', 'Skills', 'URL']].head(10).to_dict(orient="records")
        print(f"✅ Found {len(top_matches)} recommendations")

        return {"results": top_matches}

    except Exception as e:
        print("💥 Error in /recommend_assessments:", str(e))
        return {"error": "Something went wrong on the server. 😓"}
