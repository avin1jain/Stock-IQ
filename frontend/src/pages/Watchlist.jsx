import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import { useCurrency } from "../CurrencyContext";

export default function Watchlist() {
  const [watchlist, setWatchlist] = useState(() => JSON.parse(localStorage.getItem("watchlist") || "[]"));
  const [stocks, setStocks] = useState([]);
  const [input, setInput] = useState("");
  const navigate = useNavigate();
  const { formatPrice, formatCap } = useCurrency();

  useEffect(() => {
    if (watchlist.length === 0) return;
    Promise.all(watchlist.map(s => axios.get("https://stockiq-backend-0mh0.onrender.com/api/stocks/" + s).then(r => r.data)))
      .then(setStocks).catch(() => {});
  }, [watchlist]);

  async function addStock() {
    if (!input.trim()) return;
    let sym = input.trim().toUpperCase();
    try {
      const res = await axios.get("https://stockiq-backend-0mh0.onrender.com/api/search/" + input.trim());
      sym = res.data.symbol;
    } catch {}
    if (!watchlist.includes(sym)) {
      const updated = [...watchlist, sym];
      setWatchlist(updated);
      localStorage.setItem("watchlist", JSON.stringify(updated));
    }
    setInput("");
  }

  function removeStock(sym) {
    const updated = watchlist.filter(s => s !== sym);
    setWatchlist(updated);
    localStorage.setItem("watchlist", JSON.stringify(updated));
    setStocks(stocks.filter(s => s.symbol !== sym));
  }

  return (
    <div style={{ maxWidth: "900px", margin: "0 auto", padding: "32px 24px" }}>
      <h1 style={{ color: "white", fontSize: "28px", fontWeight: "bold", marginBottom: "6px" }}>
        My Watchlist
      </h1>
      <p style={{ color: "#6b7280", marginBottom: "28px" }}>Track your favourite stocks</p>

      <div style={{ display: "flex", gap: "12px", marginBottom: "32px" }}>
        <input
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyDown={e => e.key === "Enter" && addStock()}
          placeholder="Type company name e.g. Apple, Reliance, TCS"
          style={{ flex: 1, backgroundColor: "#111827", border: "1px solid #374151", borderRadius: "8px", padding: "12px 16px", color: "white", fontSize: "15px", outline: "none" }}
        />
        <button onClick={addStock} style={{ backgroundColor: "#3b82f6", color: "white", border: "none", borderRadius: "8px", padding: "12px 24px", cursor: "pointer", fontSize: "15px" }}>
          Add
        </button>
      </div>

      {watchlist.length === 0 && (
        <p style={{ color: "#6b7280" }}>No stocks added yet. Type a company name above!</p>
      )}

      <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: "16px" }}>
        {stocks.map(s => {
          const isIndian = s.symbol?.endsWith(".NS") || s.symbol?.endsWith(".BO");
          return (
            <div key={s.symbol}
              style={{ backgroundColor: "#111827", border: "1px solid #1f2937", borderRadius: "12px", padding: "20px", cursor: "pointer" }}
              onClick={() => navigate("/stock/" + s.symbol)}
              onMouseEnter={e => e.currentTarget.style.borderColor = "#3b82f6"}
              onMouseLeave={e => e.currentTarget.style.borderColor = "#1f2937"}
            >
              <div style={{ display: "flex", justifyContent: "space-between" }}>
                <p style={{ color: "white", fontWeight: "bold", fontSize: "18px" }}>{s.symbol}</p>
                <button
                  onClick={e => { e.stopPropagation(); removeStock(s.symbol); }}
                  style={{ backgroundColor: "#450a0a", color: "#f87171", border: "none", borderRadius: "6px", padding: "2px 8px", cursor: "pointer", fontSize: "12px" }}
                >
                  Remove
                </button>
              </div>
              <p style={{ color: "#6b7280", fontSize: "12px", marginTop: "2px" }}>{s.name?.slice(0, 20)}</p>
              <p style={{ color: "white", fontSize: "24px", fontWeight: "bold", marginTop: "12px" }}>
                {formatPrice(s.price, isIndian)}
              </p>
              <p style={{ color: s.change_pct >= 0 ? "#34d399" : "#f87171", fontSize: "14px", marginTop: "4px" }}>
                {s.change_pct >= 0 ? "+" : ""}{s.change_pct?.toFixed(2)}%
              </p>
              <p style={{ color: "#6b7280", fontSize: "12px", marginTop: "4px" }}>
                {formatCap(s.market_cap, isIndian)}
              </p>
            </div>
          );
        })}
      </div>
    </div>
  );
}
