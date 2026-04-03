import { useState } from "react"

export default function App() {
  const [question, setQuestion] = useState("")
  const [answer, setAnswer] = useState("")
  const [loading, setLoading] = useState(false)

  const handleSubmit = async () => {
    if (!question.trim()) return
    setLoading(true)
    setAnswer("")
    try {
      const res = await fetch("http://localhost:8000/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question }),
      })
      const data = await res.json()
      setAnswer(data.answer)
    } catch (e) {
      setAnswer("Error connecting to server. Make sure the API is running.")
    }
    setLoading(false)
  }

  const examples = [
    "What are the main risks for JPMorgan?",
    "How does Goldman Sachs manage market risk?",
    "What is Bank of America's growth strategy?",
    "Compare JPMorgan and Goldman Sachs risk management",
  ]

  return (
    <div style={{ fontFamily: "'Inter', sans-serif", backgroundColor: "#fff", minHeight: "100vh", maxWidth: "1100px", margin: "0 auto" }}>
      
      {/* Navbar */}
      <nav style={{ borderBottom: "1px solid #e0e0e0", padding: "20px 0", display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <span style={{ fontWeight: 600, fontSize: "1em", letterSpacing: "0.5px" }}>Fintech Audit AI</span>
        <span style={{ fontSize: "0.85em", color: "#555" }}>Powered by SEC EDGAR</span>
      </nav>

      {/* Hero */}
      <div style={{ padding: "80px 0 40px" }}>
        <h1 style={{ fontFamily: "Georgia, serif", fontSize: "3.8em", fontWeight: 700, lineHeight: 1.1, color: "#000", maxWidth: "750px", margin: "0 0 24px 0" }}>
          Intelligent financial research, powered by real filings.
        </h1>
        <p style={{ fontSize: "1.1em", color: "#555", maxWidth: "560px", lineHeight: 1.7, margin: 0 }}>
          Ask any question about JPMorgan Chase, Goldman Sachs, or Bank of America. 
          Answers are grounded in real SEC 10-K filings using RAG + AI reasoning.
        </p>
      </div>

      {/* Search */}
      <div style={{ padding: "0 0 30px" }}>
        <textarea
          value={question}
          onChange={e => setQuestion(e.target.value)}
          placeholder="e.g. What are the main risks for JPMorgan in 2025?"
          rows={3}
          style={{ width: "100%", maxWidth: "680px", padding: "16px", fontSize: "1em", border: "1px solid #ccc", borderRadius: "4px", fontFamily: "Inter, sans-serif", resize: "vertical", boxSizing: "border-box", display: "block" }}
        />
        <button
          onClick={handleSubmit}
          disabled={loading}
          style={{ marginTop: "16px", backgroundColor: "#000", color: "#fff", border: "none", borderRadius: "25px", padding: "12px 32px", fontSize: "0.95em", cursor: "pointer", fontFamily: "Inter, sans-serif" }}
        >
          {loading ? "Searching..." : "Search filings →"}
        </button>
      </div>

      {/* Examples */}
      <div style={{ padding: "0 0 40px" }}>
        <p style={{ fontSize: "0.85em", color: "#999", marginBottom: "12px" }}>Try these examples:</p>
        <div style={{ display: "flex", flexWrap: "wrap", gap: "10px" }}>
          {examples.map((ex, i) => (
            <button key={i} onClick={() => setQuestion(ex)}
              style={{ backgroundColor: "#f5f5f5", border: "1px solid #e0e0e0", borderRadius: "20px", padding: "8px 18px", fontSize: "0.85em", cursor: "pointer", fontFamily: "Inter, sans-serif", color: "#333" }}>
              {ex}
            </button>
          ))}
        </div>
      </div>

      {/* Answer */}
      {answer && (
        <div style={{ padding: "0 0 80px" }}>
          <hr style={{ border: "none", borderTop: "1px solid #e0e0e0", marginBottom: "40px" }} />
          <h2 style={{ fontFamily: "Georgia, serif", fontSize: "1.8em", marginBottom: "20px", color: "#000" }}>Answer</h2>
          <p style={{ fontSize: "1em", lineHeight: 1.9, color: "#222", maxWidth: "720px", whiteSpace: "pre-wrap" }}>{answer}</p>
        </div>
      )}

      {/* Footer */}
      <div style={{ borderTop: "1px solid #e0e0e0", padding: "20px 0" }}>
        <p style={{ fontSize: "0.8em", color: "#999", margin: 0 }}>Data sourced from SEC EDGAR public filings · For research purposes only</p>
      </div>
    </div>
  )
}