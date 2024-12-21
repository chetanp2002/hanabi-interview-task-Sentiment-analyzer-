from fastapi import FastAPI, File, UploadFile, HTTPException, Depends
from fastapi.security import APIKeyHeader
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import io

# FastAPI App
app = FastAPI()

# CORS Middleware - Allow requests from React app running on localhost:3000
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Authentication - API Key
api_key_header = APIKeyHeader(name="Authorization")

# Sentiment Analysis with VADER
analyzer = SentimentIntensityAnalyzer()

# Function to analyze sentiment
def analyze_sentiment(text: str) -> str:
    score = analyzer.polarity_scores(text)['compound']
    if score >= 0.05:
        return 'Positive'
    elif score <= -0.05:
        return 'Negative'
    else:
        return 'Neutral'

# API endpoint to analyze text directly
@app.post("/analyze")
async def analyze_text(text: str, api_key: str = Depends(api_key_header)):
    sentiment = analyze_sentiment(text)
    return {"text": text, "sentiment": sentiment}

# API endpoint to upload CSV and analyze sentiment
@app.post("/upload")
async def upload_csv(file: UploadFile = File(...), api_key: str = Depends(api_key_header)):
    try:
        content = await file.read()
        df = pd.read_csv(io.BytesIO(content))
        
        if 'id' not in df or 'text' not in df:
            raise HTTPException(status_code=400, detail="CSV must contain 'id' and 'text' columns.")
        
        results = []
        for index, row in df.iterrows():
            sentiment = analyze_sentiment(row['text'])
            results.append({
                "id": row['id'],
                "text": row['text'],
                "timestamp": row.get('timestamp', None),
                "sentiment": sentiment
            })
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Run with: uvicorn app:app --reload
