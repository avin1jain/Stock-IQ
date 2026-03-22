import { useState } from "react";
import { getNews } from "../services/api";

export default function News() {
  const [query, setQuery] = useState("");
  const [articles, setArticles] = useState([]);
  const [loading, setLoading] = useState(false);
  const [searched, setSearched] = useState(false);

  async function search() {
    if (!query.trim()) return;
    setLoading(true);
    setSearched(true);
    try {
      const r = await getNews(query.toUpperCase());
      setArticles(r.data.articles);
    } catch {
      setArticles([]);
    }
    setLoading(false);
  }

  return (
    <div style={{ maxWidth: "800px", margin: "0 auto", padding: "32px 24px" }}>
      <h1 style={{ color: "white", fontSize: "28px", fontWeight: "bold", marginBottom: "6px" }}>
        Financial News
      </h1>
      <p style={{ color: "#6b7280", marginBottom: "28px" }}>
        Search for news on any stock or company
      </p>

      <div style={{ display: "flex", gap: "12px", marginBottom: "32px" }}>
        <input
          value={query}
          onChange={e => setQuery(e.target.value)}
          onKeyDown={e => e.key === "Enter" && search()}
          placeholder="e.g. AAPL Tesla Bitcoin..."
          style={{
            flex: 1, backgroundColor: "#111827",
            border: "1px solid #374151", borderRadius: "8px",
            padding: "12px 16px", color: "white", fontSize: "15px", outline: "none",
          }}
        />
        <button onClick={search} style={{
          backgroundColor: "#3b82f6", color: "white",
          border: "none", borderRadius: "8px",
          padding: "12px 24px", cursor: "pointer", fontSize: "15px",
        }}>
          {loading ? "..." : "Search"}
        </button>
      </div>

      {searched && articles.length === 0 && !loading && (
        <p style={{ color: "#6b7280" }}>No articles found. Try a different search.</p>
      )}

      <div style={{ display: "flex", flexDirection: "column", gap: "12px" }}>
        {articles.map((a, i) => (
          <a key={i} href={a.url} target="_blank" rel="noreferrer" style={{ textDecoration: "none" }}>
            <div
              style={{ backgroundColor: "#111827", border: "1px solid #1f2937", borderRadius: "12px", padding: "18px 20px" }}
              onMouseEnter={e => e.currentTarget.style.borderColor = "#374151"}
              onMouseLeave={e => e.currentTarget.style.borderColor = "#1f2937"}
            >
              <p style={{ color: "white", fontSize: "15px", fontWeight: "500", lineHeight: "1.5" }}>
                {a.title}
              </p>
              {a.summary && (
                <p style={{ color: "#6b7280", fontSize: "13px", marginTop: "6px", lineHeight: "1.5" }}>
                  {a.summary?.slice(0, 140)}...
                </p>
              )}
              <p style={{ color: "#4b5563", fontSize: "12px", marginTop: "8px" }}>
                {a.source} · {a.date}
              </p>
            </div>
          </a>
        ))}
      </div>
    </div>
  );
}