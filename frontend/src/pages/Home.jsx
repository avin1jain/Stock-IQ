import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { getMarket, getStock } from "../services/api";
import { useCurrency } from "../CurrencyContext";

const STOCKS = ["AAPL", "MSFT", "GOOGL", "TSLA", "AMZN", "NVDA"];

export default function Home() {
  const [indices, setIndices] = useState([]);
  const [stocks,  setStocks]  = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();
  const { formatPrice, formatCap } = useCurrency();

  useEffect(() => {
    getMarket().then(r => setIndices(r.data.indices)).catch(() => {});
    Promise.all(STOCKS.map(s => getStock(s).then(r => r.data)))
      .then(r => { setStocks(r); setLoading(false); })
      .catch(() => setLoading(false));
  }, []);

  return (
    <div style={{ maxWidth: "1100px", margin: "0 auto", padding: "32px 24px" }}>
      <h1 style={{ fontSize: "28px", fontWeight: "bold", color: "white", marginBottom: "6px" }}>
        Market Overview
      </h1>
      <p style={{ color: "#6b7280", marginBottom: "32px" }}>
        Real-time stock market intelligence
      </p>

      <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: "16px", marginBottom: "40px" }}>
        {indices.map(i => (
          <div key={i.name} style={{ backgroundColor: "#111827", border: "1px solid #1f2937", borderRadius: "12px", padding: "20px" }}>
            <p style={{ color: "#6b7280", fontSize: "13px", marginBottom: "8px" }}>{i.name}</p>
            <p style={{ color: "white", fontSize: "22px", fontWeight: "bold" }}>
              {formatPrice(i.price, false)}
            </p>
            <p style={{ color: i.change_pct >= 0 ? "#34d399" : "#f87171", fontSize: "14px", marginTop: "4px" }}>
              {i.change_pct >= 0 ? "▲" : "▼"} {Math.abs(i.change_pct)}%
            </p>
          </div>
        ))}
      </div>

      <h2 style={{ fontSize: "18px", fontWeight: "600", color: "white", marginBottom: "16px" }}>
        Popular Stocks
      </h2>

      {loading ? (
        <p style={{ color: "#6b7280" }}>Loading stocks...</p>
      ) : (
        <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: "16px" }}>
          {stocks.map(s => {
            const isIndian = s.symbol?.endsWith(".NS") || s.symbol?.endsWith(".BO");
            return (
              <div key={s.symbol} onClick={() => navigate("/stock/" + s.symbol)}
                style={{ backgroundColor: "#111827", border: "1px solid #1f2937", borderRadius: "12px", padding: "20px", cursor: "pointer" }}
                onMouseEnter={e => e.currentTarget.style.borderColor = "#3b82f6"}
                onMouseLeave={e => e.currentTarget.style.borderColor = "#1f2937"}
              >
                <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start" }}>
                  <div>
                    <p style={{ color: "white", fontWeight: "bold", fontSize: "18px" }}>{s.symbol}</p>
                    <p style={{ color: "#6b7280", fontSize: "12px" }}>{s.name?.slice(0, 20)}</p>
                  </div>
                  <span style={{
                    backgroundColor: s.change_pct >= 0 ? "#064e3b" : "#450a0a",
                    color: s.change_pct >= 0 ? "#34d399" : "#f87171",
                    padding: "4px 10px", borderRadius: "99px", fontSize: "13px"
                  }}>
                    {s.change_pct >= 0 ? "+" : ""}{s.change_pct?.toFixed(2)}%
                  </span>
                </div>
                <p style={{ color: "white", fontSize: "24px", fontWeight: "bold", marginTop: "12px" }}>
                  {formatPrice(s.price, isIndian)}
                </p>
                <p style={{ color: "#6b7280", fontSize: "12px", marginTop: "4px" }}>
                  {formatCap(s.market_cap, isIndian)}
                </p>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
