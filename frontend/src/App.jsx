import { useState, useEffect } from 'react'
import axios from 'axios'
import './App.css'

function App() {
  // State management
  const [reviews, setReviews] = useState([])
  const [formData, setFormData] = useState({ product_name: '', review_text: '' })
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const API_URL = 'http://127.0.0.1:8000/api'

  useEffect(() => {
    fetchReviews()
  }, [])

  const fetchReviews = async () => {
    try {
      const res = await axios.get(`${API_URL}/reviews`)
      setReviews(res.data)
    } catch (err) {
      console.error("Gagal ambil data:", err)
      setError("Gagal konek ke backend. Pastikan server nyala!")
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError(null)
    
    try {
      // Kirim data ke Backend
      await axios.post(`${API_URL}/analyze-review`, formData)
      setFormData({ product_name: '', review_text: '' }) 
      fetchReviews() 
    } catch (err) {
      console.error(err)
      setError("Gagal analisa review. Cek console log.")
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="container">
      <header className="header">
        <h1>✨ AI Product Review Analyzer</h1>
        <p>Powered by HuggingFace (Sentiment) & Gemini (Key Points)</p>
      </header>

      {/* Error Banner */}
      {error && <div className="error-banner">{error}</div>}
      
      {/* Input Form */}
      <div className="card form-card">
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Product Name</label>
            <input
              type="text"
              placeholder="Contoh: Laptop Gaming ROG"
              value={formData.product_name}
              onChange={(e) => setFormData({...formData, product_name: e.target.value})}
              required
            />
          </div>
          
          <div className="form-group">
            <label>Your Review</label>
            <textarea
              placeholder="Tulis review jujur lo di sini..."
              value={formData.review_text}
              onChange={(e) => setFormData({...formData, review_text: e.target.value})}
              required
              rows="4"
            />
          </div>

          <button type="submit" disabled={loading} className="btn-submit">
            {loading ? '⏳ Sedang Menganalisa...' : '🔍 Analyze Review'}
          </button>
        </form>
      </div>

      <hr className="divider"/>

      {/* Results Display */}
      <div className="results-section">
        <h2>Recent Reviews ({reviews.length})</h2>
        
        {reviews.length === 0 && <p className="empty-state">Belum ada review. Jadilah yang pertama!</p>}

        <div className="review-grid">
          {reviews.map((review) => (
            <div key={review.id} className="review-card">
              <div className="review-header">
                <h3>{review.product_name}</h3>
                <span className={`badge ${review.sentiment}`}>
                  {review.sentiment}
                </span>
              </div>
              
              <p className="review-text">"{review.review_text}"</p>
              
              <div className="ai-insight">
                <strong> Gemini Insights:</strong>
                <div className="points">
                  {review.key_points.split('\n').map((line, i) => (
                    line && <div key={i}>{line}</div>
                  ))}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

export default App