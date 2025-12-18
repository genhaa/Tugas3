from sqlalchemy import Column, Integer, String, Text, DateTime
from database import Base
import datetime

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String, index=True)
    review_text = Column(Text)
    sentiment = Column(String) # Positive/Negative/Neutral
    key_points = Column(Text) # Hasil ekstraksi Gemini
    created_at = Column(DateTime, default=datetime.datetime.utcnow)