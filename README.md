# 🎯 AI Product Review Analyzer

Aplikasi full-stack untuk menganalisis review produk menggunakan AI. Sistem ini menggunakan HuggingFace DistilBERT untuk analisis sentimen dan Google Gemini AI untuk ekstraksi poin-poin penting.

## ✨ Features

- 🤖 **AI-Powered Sentiment Analysis** - Menggunakan HuggingFace DistilBERT multilingual model
- 📝 **Key Points Extraction** - Google Gemini AI mengekstrak poin-poin penting dari review
- 💾 **Persistent Storage** - Menyimpan semua review dan hasil analisis
- 🎨 **Modern UI** - Interface yang clean dan responsive
- ⚡ **Real-time Analysis** - Hasil analisis langsung ditampilkan

## 🏗️ Tech Stack

**Backend:**
- FastAPI
- SQLAlchemy ORM
- PostgreSQL / SQLite
- Google Gemini AI
- HuggingFace Inference API

**Frontend:**
- React 18
- Vite
- Axios
- CSS3

## 📁 Project Structure

```
ai-review-analyzer/
├── backend/
│   ├── main.py              # FastAPI app & endpoints
│   ├── models.py            # SQLAlchemy models
│   ├── database.py          # Database configuration
│   ├── requirements.txt     # Python dependencies
│   └── .env                 # Environment variables
└── frontend/
    ├── src/
    │   ├── App.jsx          # Main React component
    │   ├── App.css          # Styling
    │   ├── main.jsx         # Entry point
    │   └── index.css        # Global styles
    ├── index.html           # HTML template
    ├── package.json         # Node dependencies
    └── vite.config.js       # Vite configuration
```

## 🚀 Installation Guide

### Prerequisites

- Python 3.8+
- Node.js 16+
- PostgreSQL (optional, bisa pakai SQLite)
- API Keys:
  - Google Gemini API Key → https://makersuite.google.com/app/apikey
  - HuggingFace Token → https://huggingface.co/settings/tokens

### 1️⃣ Backend Setup

```bash
# Masuk ke folder backend
cd backend

# Buat virtual environment
python -m venv venv

# Aktifkan virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Buat file .env dan isi dengan:
# DATABASE_URL=sqlite:///./reviews.db
# GEMINI_API_KEY=your_key_here
# HF_API_TOKEN=your_token_here

# Jalankan server
uvicorn main:app --reload
```

✅ Server akan berjalan di: **http://127.0.0.1:8000**

### 2️⃣ Frontend Setup

```bash
# Buka terminal baru, masuk ke folder frontend
cd frontend

# Install dependencies
npm install

# Jalankan development server
npm run dev
```

✅ Frontend akan berjalan di: **http://localhost:5173**

## 📡 API Endpoints

### POST `/api/analyze-review`

Menganalisis review produk baru.

**Request Body:**
```json
{
  "product_name": "Laptop Gaming ROG",
  "review_text": "Laptop ini sangat bagus untuk gaming, performa tinggi tapi agak berat"
}
```

**Response:**
```json
{
  "id": 1,
  "product_name": "Laptop Gaming ROG",
  "review_text": "Laptop ini sangat bagus untuk gaming...",
  "sentiment": "positive",
  "key_points": "• High gaming performance\n• Heavy weight\n• Good value",
  "created_at": "2024-01-15T10:30:00"
}
```

### GET `/api/reviews`

Mengambil semua review yang sudah dianalisis.

**Response:**
```json
[
  {
    "id": 1,
    "product_name": "Laptop Gaming ROG",
    "review_text": "...",
    "sentiment": "positive",
    "key_points": "...",
    "created_at": "2024-01-15T10:30:00"
  }
]
```

## 🧪 Testing Guide

### Test Backend dengan cURL

```bash
# Test POST - Analyze Review
curl -X POST "http://127.0.0.1:8000/api/analyze-review" \
  -H "Content-Type: application/json" \
  -d '{
    "product_name": "iPhone 15 Pro",
    "review_text": "This is an amazing product! Highly recommended."
  }'

# Test GET - Get All Reviews
curl http://127.0.0.1:8000/api/reviews
```

### Test Frontend Manual

1. Buka browser ke `http://localhost:5173`
2. Isi form dengan contoh data:
   - **Product Name:** "iPhone 15 Pro"
   - **Review:** "Kamera bagus banget, tapi baterainya kurang tahan lama"
3. Klik **"🔍 Analyze Review"**
4. Verifikasi hasil muncul dengan:
   - ✅ Badge sentiment (positive/negative/neutral)
   - ✅ Key points dari Gemini AI
5. Refresh halaman untuk memastikan data tersimpan

### Test dengan Postman/Thunder Client

1. Import collection atau buat request baru
2. **POST** `http://127.0.0.1:8000/api/analyze-review`
3. Headers: `Content-Type: application/json`
4. Body (raw JSON):
```json
{
  "product_name": "Samsung Galaxy S24",
  "review_text": "Performa mantap, layar jernih, tapi harganya mahal"
}
```
5. Send dan verifikasi response

## ⚠️ Troubleshooting

### ❌ Problem: "HF Model Loading"

**Penyebab:** Model HuggingFace sedang cold start (loading pertama kali).

**Solusi:** 
- Tunggu 30-60 detik dan coba lagi
- Model akan stay loaded setelah request pertama
- Jika tetap error, cek HF token valid di https://huggingface.co/settings/tokens

---

### ❌ Problem: CORS Error di Browser

**Error Message:**
```
Access to XMLHttpRequest at 'http://127.0.0.1:8000' from origin 
'http://localhost:5173' has been blocked by CORS policy
```

**Solusi:** 
1. Pastikan CORS middleware sudah ada di `main.py`
2. Restart backend server
3. Clear browser cache (Ctrl + Shift + R)

---

### ❌ Problem: Database Connection Error

**Error Message:**
```
sqlalchemy.exc.OperationalError: could not connect to server
```

**Solusi:**
1. **Jika pakai PostgreSQL:** Pastikan PostgreSQL running
2. **Solusi mudah:** Gunakan SQLite di `.env`:
   ```env
   DATABASE_URL=sqlite:///./reviews.db
   ```
3. Restart backend server
4. Database akan otomatis dibuat

---

### ❌ Problem: "GEMINI_API_KEY not found"

**Solusi:**
1. Pastikan file `.env` ada di folder `backend/`
2. Format harus tepat (tidak ada spasi):
   ```env
   GEMINI_API_KEY=AIzaSyXXXXXXXXXXXXXX
   HF_API_TOKEN=hf_XXXXXXXXXXXXXXXX
   ```
3. Restart backend setelah edit `.env`
4. Cek dengan print statement di terminal

---

### ❌ Problem: Module Not Found

**Error Message:**
```
ModuleNotFoundError: No module named 'fastapi'
```

**Solusi:**
```bash
# Pastikan virtual environment AKTIF
# Lihat ada (venv) di terminal

# Reinstall dependencies
pip install -r requirements.txt

# Jika masih error, install manual:
pip install fastapi uvicorn sqlalchemy python-dotenv google-generativeai requests
```

---

### ❌ Problem: Port Already in Use

**Error Message:**
```
[ERROR] [Errno 48] Address already in use
```

**Solusi:**
```bash
# Cari process yang pakai port 8000
# Mac/Linux:
lsof -ti:8000 | xargs kill -9

# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Atau ubah port di command:
uvicorn main:app --reload --port 8001
```

---

### ❌ Problem: Frontend Cannot Connect to Backend

**Checklist:**
- [ ] Backend server sudah running di http://127.0.0.1:8000
- [ ] Frontend sudah running di http://localhost:5173
- [ ] Cek URL di `App.jsx` sesuai dengan backend port
- [ ] Test backend dengan curl terlebih dahulu
- [ ] Cek browser console untuk error detail

---

## 🔒 Security Notes

⚠️ **PENTING - JANGAN commit file `.env` ke Git!**

Tambahkan ke `.gitignore`:
```gitignore
# Backend
backend/.env
backend/venv/
backend/__pycache__/
backend/*.db

# Frontend
frontend/node_modules/
frontend/dist/
frontend/.env
```
