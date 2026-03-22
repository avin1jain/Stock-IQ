import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import axios from "axios";
import { useCurrency } from "../CurrencyContext";

export default function Navbar() {
  const [query, setQuery] = useState("");
  const [searching, setSearching] = useState(false);
  const navigate = useNavigate();
  const { currency, setCurrency } = useCurrency();

  async function handleSearch(e) {
    e.preventDefault();
    if (!query.trim()) return;
    setSearching(true);
    try {
      const res = await axios.get("http://localhost:8000/api/search/" + query.trim());
      navigate("/stock/" + res.data.symbol);
      setQuery("");
    } catch {
      navigate("/stock/" + query.trim().toUpperCase());
      setQuery("");
    }
    setSearching(false);
  }

  return (
    <nav style={{
      backgroundColor: "#111827",
      borderBottom: "1px solid #1f2937",
      padding: "12px 24px",
      display: "flex",
      alignItems: "center",
      justifyContent: "space-between",
      flexWrap: "wrap",
      gap: "12px",
    }}>
      <Link to="/" style={{ color: "#60a5fa", fontWeight: "bold", fontSize: "20px", textDecoration: "none" }}>
        StockIQ
      </Link>

      <form onSubmit={handleSearch} style={{ display: "flex", gap: "8px" }}>
        <input
          value={query}
          onChange={e => setQuery(e.target.value)}
          placeholder="Search... Apple Reliance TCS"
          style={{
            backgroundColor: "#1f2937",
            border: "1px solid #374151",
            borderRadius: "8px",
            padding: "8px 14px",
            color: "white",
            fontSize: "14px",
            width: "260px",
            outline: "none",
          }}
        />
        <button type="submit" disabled={searching} style={{
          backgroundColor: searching ? "#1d4ed8" : "#3b82f6",
          color: "white",
          border: "none",
          borderRadius: "8px",
          padding: "8px 16px",
          cursor: "pointer",
          fontSize: "14px",
        }}>
          {searching ? "..." : "Search"}
        </button>
      </form>

      <div style={{ display: "flex", alignItems: "center", gap: "20px" }}>
        <Link to="/"         style={{ color: "#9ca3af", textDecoration: "none", fontSize: "14px" }}>Home</Link>
        <Link to="/compare"  style={{ color: "#9ca3af", textDecoration: "none", fontSize: "14px" }}>Compare</Link>
        <Link to="/watchlist"style={{ color: "#9ca3af", textDecoration: "none", fontSize: "14px" }}>Watchlist</Link>
        <Link to="/news"     style={{ color: "#9ca3af", textDecoration: "none", fontSize: "14px" }}>News</Link>

        {/* Currency Toggle */}
        <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
          <span style={{ color: "#6b7280", fontSize: "13px" }}>Currency:</span>
          <div style={{ display: "flex", backgroundColor: "#1f2937", borderRadius: "8px", padding: "3px" }}>
            <button
              onClick={() => setCurrency("USD")}
              style={{
                backgroundColor: currency === "USD" ? "#3b82f6" : "transparent",
                color: currency === "USD" ? "white" : "#9ca3af",
                border: "none", borderRadius: "6px",
                padding: "4px 12px", cursor: "pointer",
                fontSize: "13px", fontWeight: "500",
              }}
            >
              $ USD
            </button>
            <button
              onClick={() => setCurrency("INR")}
              style={{
                backgroundColor: currency === "INR" ? "#f97316" : "transparent",
                color: currency === "INR" ? "white" : "#9ca3af",
                border: "none", borderRadius: "6px",
                padding: "4px 12px", cursor: "pointer",
                fontSize: "13px", fontWeight: "500",
              }}
            >
              ₹ INR
            </button>
          </div>
        </div>
      </div>
    </nav>
  );
}