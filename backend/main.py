from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
import models
import database
import os
import google.generativeai as genai
import requests
from dotenv import load_dotenv

# 0. Load Environment Variables
load_dotenv()

# DEBUG: Laporan status kunci
print("--- SYSTEM CHECK ---")
print(f"🔑 Gemini Key: {bool(os.getenv('GEMINI_API_KEY'))}")
print(f"🔑 HF Token:   {bool(os.getenv('HF_API_TOKEN'))}")
print("--------------------")

# 1. Init App & Database
app = FastAPI()
models.Base.metadata.create_all(bind=database.engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. Config AI Services
GEMINI_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_KEY)

HF_TOKEN = os.getenv("HF_API_TOKEN")

HF_API_URL = "https://router.huggingface.co/hf-inference/models/lxyuan/distilbert-base-multilingual-cased-sentiments-student"
HF_HEADERS = {"Authorization": f"Bearer {HF_TOKEN}"}

# 3. Pydantic Schemas
class ReviewInput(BaseModel):
    product_name: str
    review_text: str

# 4. Helper Functions
def analyze_sentiment_hf(text):
    if not HF_TOKEN:
        print("Error: HF Token belum di-set di .env")
        return "neutral"

    try:

        payload = {"inputs": text}
        response = requests.post(HF_API_URL, headers=HF_HEADERS, json=payload)
        
        if response.status_code != 200:
            print(f"HF Error Status: {response.status_code}") 
            return "neutral"
            
        result = response.json()
        
        # Handle kalau model masih loading (Cold Start)
        if isinstance(result, dict) and "error" in result:
             print(f"HF Model Loading: {result['error']}")
             return "neutral"

        if isinstance(result, list) and len(result) > 0 and isinstance(result[0], list):
             best = max(result[0], key=lambda x: x['score'])
             return best['label'] 
        
        return "neutral"
        
    except Exception as e:
        print(f"❌ HF Exception: {e}")
        return "neutral"

def extract_points_gemini(text):
    if not GEMINI_KEY:
        return "Error: API Key Gemini hilang."

    try:
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        prompt = f"Extract 3-5 key points from this product review as a bulleted list. Keep it concise:\n\n{text}"
        response = model.generate_content(prompt)
        
        return response.text
    except Exception as e:
        print(f"Gemini Error: {e}")
        return "Failed to extract points."

# 5. Endpoints
@app.post("/api/analyze-review")
def create_review(review: ReviewInput, db: Session = Depends(database.get_db)):
    print(f"\nNew Request: {review.product_name}")
    
    sentiment_result = analyze_sentiment_hf(review.review_text)
    print(f"   Sentiment: {sentiment_result}")
    
    key_points_result = extract_points_gemini(review.review_text)
    print(f"   Gemini: Selesai")
    
    db_review = models.Review(
        product_name=review.product_name,
        review_text=review.review_text,
        sentiment=sentiment_result,
        key_points=key_points_result
    )
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    
    return db_review

@app.get("/api/reviews")
def get_reviews(db: Session = Depends(database.get_db)):
    return db.query(models.Review).order_by(models.Review.id.desc()).all()