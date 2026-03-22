import { useState } from "react";
import axios from "axios";
import { useCurrency } from "../CurrencyContext";

const METRICS = [
  ["P/E Ratio",      "pe_ratio",       false],
  ["P/B Ratio",      "pb_ratio",       false],
  ["ROE",            "roe",            false],
  ["Profit Margin",  "profit_margins", false],
  ["Debt/Equity",    "debt_to_equity", false],
  ["Revenue Growth", "revenue_growth", false],
  ["Market Cap",     "market_cap",     true],
];

export default function Compare() {
  const [sym1, setSym1] = useState("AAPL");
  const [sym2, setSym2] = useState("MSFT");
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const { formatPrice, formatCap, symbol: currSymbol } = useCurrency();

  const isIndian = (sym) => sym?.endsWith(".NS") || sym?.endsWith(".BO");

  async function resolveSymbol(input) {
    try {
      const res = await axios.get("https://stockiq-backend-0mh0.onrender.com/api/search/" + input.trim());
      return res.data.symbol;
    } catch {
      return input.trim().toUpperCase();
    }
  }

  async function compare() {
    setLoading(true);
    setError("");
    try {
      const [resolved1, resolved2] = await Promise.all([
        resolveSymbol(sym1),
        resolveSymbol(sym2),
      ]);
      setSym1(resolved1);
      setSym2(resolved2);
      const [s1, s2, f1, f2] = await Promise.all([
        axios.get("https://stockiq-backend-0mh0.onrender.com/api/stocks/" + resolved1),
        axios.get("https://stockiq-backend-0mh0.onrender.com/api/stocks/" + resolved2),
        axios.get("https://stockiq-backend-0mh0.onrender.com/api/financials/" + resolved1),
        axios.get("https://stockiq-backend-0mh0.onrender.com/api/financials/" + resolved2),
      ]);
      setData({
        c1: { ...s1.data, ...f1.data },
        c2: { ...s2.data, ...f2.data },
      });
    } catch {
      setError("Could not load data. Check symbols.");
    }
    setLoading(false);
  }

  function fmt(key, val, isCap, sym) {
    if (val === null || val === undefined) return "—";
    if (isCap) return formatCap(val, isIndian(sym));
    if (key === "roe" || key === "profit_margins" || key === "revenue_growth")
      return (val * 100).toFixed(1) + "%";
    return val.toFixed(2);
  }

  return (
    <div style={{ maxWidth: "900px", margin: "0 auto", padding: "32px 24px" }}>
      <h1 style={{ color: "white", fontSize: "28px", fontWeight: "bold", marginBottom: "6px" }}>
        Compare Companies
      </h1>
      <p style={{ color: "#6b7280", marginBottom: "28px" }}>Side by side financial comparison</p>

      <div style={{ display: "flex", gap: "12px", marginBottom: "32px", flexWrap: "wrap" }}>
        <input value={sym1} onChange={e => setSym1(e.target.value)} placeholder="Type company name or symbol"
          style={{ flex: 1, backgroundColor: "#111827", border: "1px solid #374151", borderRadius: "8px", padding: "12px 16px", color: "white", fontSize: "16px", textAlign: "center", outline: "none" }} />
        <input value={sym2} onChange={e => setSym2(e.target.value)} placeholder="Type company name or symbol"
          style={{ flex: 1, backgroundColor: "#111827", border: "1px solid #374151", borderRadius: "8px", padding: "12px 16px", color: "white", fontSize: "16px", textAlign: "center", outline: "none" }} />
        <button onClick={compare} disabled={loading} style={{ backgroundColor: "#3b82f6", color: "white", border: "none", borderRadius: "8px", padding: "12px 28px", cursor: "pointer", fontSize: "15px" }}>
          {loading ? "Loading..." : "Compare"}
        </button>
      </div>

      {error && <p style={{ color: "#f87171", marginBottom: "16px" }}>{error}</p>}

      {data && (
        <div style={{ backgroundColor: "#111827", border: "1px solid #1f2937", borderRadius: "12px", overflow: "hidden" }}>
          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr 1fr", backgroundColor: "#1f2937", padding: "16px" }}>
            <p style={{ color: "#6b7280", fontSize: "14px" }}>Metric</p>
            <p style={{ color: "white", fontWeight: "bold", fontSize: "18px", textAlign: "center" }}>
              {data.c1.symbol} {isIndian(data.c1.symbol) ? "🇮🇳" : "🇺🇸"}
            </p>
            <p style={{ color: "white", fontWeight: "bold", fontSize: "18px", textAlign: "center" }}>
              {data.c2.symbol} {isIndian(data.c2.symbol) ? "🇮🇳" : "🇺🇸"}
            </p>
          </div>
          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr 1fr", padding: "12px 16px", borderTop: "1px solid #1f2937" }}>
            <p style={{ color: "#6b7280", fontSize: "14px" }}>Price ({currSymbol()})</p>
            <p style={{ color: "white", fontWeight: "600", textAlign: "center" }}>{formatPrice(data.c1.price, isIndian(data.c1.symbol))}</p>
            <p style={{ color: "white", fontWeight: "600", textAlign: "center" }}>{formatPrice(data.c2.price, isIndian(data.c2.symbol))}</p>
          </div>
          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr 1fr", padding: "12px 16px", borderTop: "1px solid #1f2937" }}>
            <p style={{ color: "#6b7280", fontSize: "14px" }}>Change Today</p>
            <p style={{ color: data.c1.change_pct >= 0 ? "#34d399" : "#f87171", fontWeight: "600", textAlign: "center" }}>
              {data.c1.change_pct >= 0 ? "+" : ""}{data.c1.change_pct?.toFixed(2)}%
            </p>
            <p style={{ color: data.c2.change_pct >= 0 ? "#34d399" : "#f87171", fontWeight: "600", textAlign: "center" }}>
              {data.c2.change_pct >= 0 ? "+" : ""}{data.c2.change_pct?.toFixed(2)}%
            </p>
          </div>
          {METRICS.map(([label, key, isCap], i) => (
            <div key={key} style={{ display: "grid", gridTemplateColumns: "1fr 1fr 1fr", padding: "12px 16px", borderTop: "1px solid #1f2937", backgroundColor: i % 2 === 0 ? "" : "#0d1117" }}>
              <p style={{ color: "#6b7280", fontSize: "14px" }}>{label}</p>
              <p style={{ color: "white", fontWeight: "600", textAlign: "center" }}>{fmt(key, data.c1[key], isCap, data.c1.symbol)}</p>
              <p style={{ color: "white", fontWeight: "600", textAlign: "center" }}>{fmt(key, data.c2[key], isCap, data.c2.symbol)}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
