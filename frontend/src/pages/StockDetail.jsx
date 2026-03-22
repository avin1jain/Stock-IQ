import { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import { AreaChart, Area, XAxis, YAxis, Tooltip, CartesianGrid, ResponsiveContainer } from "recharts";
import { getStock, getHistory, getNews, getPrediction, getInsights } from "../services/api";
import { useCurrency } from "../CurrencyContext";
import axios from "axios";

const PERIODS = ["1mo", "3mo", "6mo", "1y"];
const IC = {
  positive: { bg: "#052e16", border: "#166534", text: "#4ade80" },
  warning:  { bg: "#422006", border: "#92400e", text: "#fcd34d" },
  risk:     { bg: "#450a0a", border: "#991b1b", text: "#f87171" },
  neutral:  { bg: "#111827", border: "#374151", text: "#9ca3af" }
};

const VERDICT_COLORS = {
  "STRONG BUY":  { bg: "#052e16", border: "#166534", text: "#4ade80", emoji: "🚀" },
  "BUY":         { bg: "#052e16", border: "#166534", text: "#86efac", emoji: "✅" },
  "HOLD":        { bg: "#422006", border: "#92400e", text: "#fcd34d", emoji: "⏳" },
  "SELL":        { bg: "#450a0a", border: "#991b1b", text: "#fca5a5", emoji: "⚠️" },
  "STRONG SELL": { bg: "#450a0a", border: "#991b1b", text: "#f87171", emoji: "🚨" },
};

export default function StockDetail() {
  const { symbol } = useParams();
  const { formatPrice, formatCap, symbol: currSymbol, convert } = useCurrency();
  const isIndian = symbol?.endsWith(".NS") || symbol?.endsWith(".BO");

  const [stock,       setStock]       = useState(null);
  const [history,     setHistory]     = useState([]);
  const [news,        setNews]        = useState([]);
  const [predict,     setPredict]     = useState(null);
  const [insights,    setInsights]    = useState([]);
  const [competitors, setCompetitors] = useState([]);
  const [suggestion,  setSuggestion]  = useState(null);
  const [suggLoading, setSuggLoading] = useState(false);
  const [period,      setPeriod]      = useState("3mo");
  const [loading,     setLoading]     = useState(true);
  const [error,       setError]       = useState(false);

  useEffect(() => {
    if (!symbol) return;
    setLoading(true);
    setError(false);
    setStock(null);
    setSuggestion(null);

    getStock(symbol).then(r => setStock(r.data)).catch(() => setError(true));
    getHistory(symbol, period).then(r => setHistory(r.data.data)).catch(() => setHistory([]));
    getNews(symbol).then(r => setNews(r.data.articles)).catch(() => setNews([]));
    getPrediction(symbol).then(r => setPredict(r.data)).catch(() => setPredict(null));
    getInsights(symbol).then(r => setInsights(r.data.insights)).catch(() => setInsights([]));
    axios.get("http://localhost:8000/api/competitors/" + symbol)
      .then(r => setCompetitors(r.data.competitors)).catch(() => setCompetitors([]));

    setLoading(false);
  }, [symbol, period]);

  async function loadSuggestion() {
    setSuggLoading(true);
    try {
      const res = await axios.get("http://localhost:8000/api/suggestion/" + symbol);
      setSuggestion(res.data);
    } catch {}
    setSuggLoading(false);
  }

  if (loading) return (
    <div style={{ textAlign: "center", padding: "80px", color: "#6b7280" }}>Loading {symbol}...</div>
  );
  if (error || !stock) return (
    <div style={{ textAlign: "center", padding: "80px" }}>
      <p style={{ fontSize: "48px", marginBottom: "16px" }}>🔍</p>
      <p style={{ color: "#f87171", fontSize: "24px", fontWeight: "bold", marginBottom: "12px" }}>Stock Not Found</p>
      <p style={{ color: "#6b7280", fontSize: "16px", marginBottom: "8px" }}>We could not find any stock with the symbol "{symbol}"</p>
      <p style={{ color: "#4b5563", fontSize: "14px", marginBottom: "32px" }}>Try searching by company name like "Apple", "Reliance", "TCS"</p>
      <button onClick={() => window.history.back()}
        style={{ backgroundColor: "#3b82f6", color: "white", border: "none", borderRadius: "8px", padding: "12px 24px", cursor: "pointer", fontSize: "15px" }}>
        Go Back
      </button>
    </div>
  );

  const isUp = stock.change_pct >= 0;
  const convertedHistory = history.map(h => ({
    ...h,
    close: parseFloat(convert(h.close, isIndian).toFixed(2)),
    open:  parseFloat(convert(h.open,  isIndian).toFixed(2)),
    high:  parseFloat(convert(h.high,  isIndian).toFixed(2)),
    low:   parseFloat(convert(h.low,   isIndian).toFixed(2)),
  }));

  const vc = suggestion ? (VERDICT_COLORS[suggestion.verdict] || VERDICT_COLORS["HOLD"]) : null;

  return (
    <div style={{ maxWidth: "1000px", margin: "0 auto", padding: "32px 24px" }}>

      {/* Header */}
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: "32px" }}>
        <div>
          <h1 style={{ color: "white", fontSize: "32px", fontWeight: "bold" }}>{stock.symbol}</h1>
          <p style={{ color: "#6b7280", marginTop: "4px" }}>{stock.name}</p>
          <p style={{ color: "#4b5563", fontSize: "13px" }}>{stock.sector}</p>
          <span style={{
            display: "inline-block", marginTop: "8px",
            backgroundColor: isIndian ? "#1e3a5f" : "#052e16",
            color: isIndian ? "#60a5fa" : "#4ade80",
            padding: "3px 10px", borderRadius: "99px", fontSize: "12px", fontWeight: "500"
          }}>
            {isIndian ? "🇮🇳 NSE — Originally in ₹ INR" : "🇺🇸 NYSE/NASDAQ — Originally in $ USD"}
          </span>
        </div>
        <div style={{ textAlign: "right" }}>
          <p style={{ color: "white", fontSize: "36px", fontWeight: "bold" }}>{formatPrice(stock.price, isIndian)}</p>
          <p style={{ color: isUp ? "#34d399" : "#f87171", fontSize: "18px", marginTop: "4px" }}>
            {isUp ? "▲" : "▼"} {Math.abs(stock.change_pct)?.toFixed(2)}% today
          </p>
        </div>
      </div>

      {/* AI Investment Suggestion Button */}
      {!suggestion && (
        <div style={{ marginBottom: "24px", textAlign: "center" }}>
          <button
            onClick={loadSuggestion}
            disabled={suggLoading}
            style={{
              background: "linear-gradient(135deg, #3b82f6, #8b5cf6)",
              color: "white", border: "none", borderRadius: "12px",
              padding: "14px 32px", cursor: "pointer", fontSize: "16px",
              fontWeight: "600", width: "100%",
              opacity: suggLoading ? 0.7 : 1,
            }}
          >
            {suggLoading ? "🤖 Analyzing stock with AI..." : "🤖 Get AI Investment Suggestion"}
          </button>
        </div>
      )}

      {/* AI Suggestion Result */}
      {suggestion && vc && (
        <div style={{
          backgroundColor: vc.bg, border: "1px solid " + vc.border,
          borderRadius: "16px", padding: "28px", marginBottom: "24px"
        }}>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: "16px" }}>
            <div>
              <p style={{ color: vc.text, fontSize: "32px", fontWeight: "bold" }}>
                {vc.emoji} {suggestion.verdict}
              </p>
              <p style={{ color: vc.text, fontSize: "20px", marginTop: "4px" }}>
                Score: {suggestion.score}
              </p>
            </div>
            <div style={{ textAlign: "right" }}>
              <p style={{ color: "#6b7280", fontSize: "12px" }}>12-month target</p>
              <p style={{ color: "white", fontSize: "24px", fontWeight: "bold" }}>
                {formatPrice(parseFloat(suggestion.target), isIndian)}
              </p>
            </div>
          </div>

          <p style={{ color: "white", fontSize: "15px", lineHeight: "1.6", marginBottom: "20px" }}>
            {suggestion.summary}
          </p>

          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "16px" }}>
            <div style={{ backgroundColor: "rgba(0,0,0,0.2)", borderRadius: "10px", padding: "16px" }}>
              <p style={{ color: "#4ade80", fontWeight: "600", marginBottom: "10px" }}>✅ Positives</p>
              {suggestion.positives.map((p, i) => (
                <p key={i} style={{ color: "#d1fae5", fontSize: "13px", marginBottom: "6px", lineHeight: "1.4" }}>
                  • {p}
                </p>
              ))}
            </div>
            <div style={{ backgroundColor: "rgba(0,0,0,0.2)", borderRadius: "10px", padding: "16px" }}>
              <p style={{ color: "#f87171", fontWeight: "600", marginBottom: "10px" }}>⚠️ Risks</p>
              {suggestion.risks.map((r, i) => (
                <p key={i} style={{ color: "#fecaca", fontSize: "13px", marginBottom: "6px", lineHeight: "1.4" }}>
                  • {r}
                </p>
              ))}
            </div>
          </div>

          <p style={{ color: "#6b7280", fontSize: "11px", marginTop: "16px", textAlign: "center" }}>
            ⚠️ This is AI-generated analysis for educational purposes only. Not financial advice. Always do your own research before investing.
          </p>

          <button onClick={() => setSuggestion(null)} style={{
            backgroundColor: "transparent", color: "#6b7280",
            border: "1px solid #374151", borderRadius: "8px",
            padding: "6px 16px", cursor: "pointer", fontSize: "12px",
            marginTop: "12px", display: "block", marginLeft: "auto",
          }}>
            Refresh Analysis
          </button>
        </div>
      )}

      {/* Chart */}
      <div style={{ backgroundColor: "#111827", border: "1px solid #1f2937", borderRadius: "12px", padding: "24px", marginBottom: "24px" }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "20px" }}>
          <h2 style={{ color: "white", fontSize: "16px", fontWeight: "600" }}>Price Chart ({currSymbol()})</h2>
          <div style={{ display: "flex", gap: "8px" }}>
            {PERIODS.map(p => (
              <button key={p} onClick={() => setPeriod(p)} style={{
                backgroundColor: period === p ? "#3b82f6" : "#1f2937",
                color: period === p ? "white" : "#9ca3af",
                border: "none", borderRadius: "6px", padding: "4px 12px", cursor: "pointer", fontSize: "13px",
              }}>{p}</button>
            ))}
          </div>
        </div>
        <ResponsiveContainer width="100%" height={260}>
          <AreaChart data={convertedHistory}>
            <defs>
              <linearGradient id="grad" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%"  stopColor="#3b82f6" stopOpacity={0.3} />
                <stop offset="95%" stopColor="#3b82f6" stopOpacity={0} />
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="#1f2937" />
            <XAxis dataKey="date" tick={{ fill: "#6b7280", fontSize: 11 }} tickFormatter={d => d.slice(5)} />
            <YAxis tick={{ fill: "#6b7280", fontSize: 11 }} tickFormatter={v => currSymbol() + v.toLocaleString()} domain={["auto", "auto"]} />
            <Tooltip
              contentStyle={{ backgroundColor: "#111827", border: "1px solid #374151", borderRadius: "8px" }}
              labelStyle={{ color: "#9ca3af" }}
              itemStyle={{ color: "#60a5fa" }}
              formatter={v => [currSymbol() + v.toLocaleString(), "Price"]}
            />
            <Area type="monotone" dataKey="close" stroke="#3b82f6" strokeWidth={2} fill="url(#grad)" />
          </AreaChart>
        </ResponsiveContainer>
      </div>

      {/* Prediction + Stats */}
      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "24px", marginBottom: "24px" }}>
        {predict && (
          <div style={{ backgroundColor: "#111827", border: "1px solid #1f2937", borderRadius: "12px", padding: "24px" }}>
            <h2 style={{ color: "white", fontSize: "16px", fontWeight: "600", marginBottom: "16px" }}>Trend Prediction</h2>
            <div style={{
              backgroundColor: predict.trend === "bullish" ? "#052e16" : "#450a0a",
              border: "1px solid " + (predict.trend === "bullish" ? "#166534" : "#991b1b"),
              borderRadius: "10px", padding: "20px", textAlign: "center",
            }}>
              <p style={{ color: predict.trend === "bullish" ? "#4ade80" : "#f87171", fontSize: "28px", fontWeight: "bold" }}>
                {predict.trend === "bullish" ? "▲ BULLISH" : "▼ BEARISH"}
              </p>
              <p style={{ color: "#9ca3af", fontSize: "14px", marginTop: "8px" }}>Confidence: {predict.confidence}%</p>
              <p style={{ color: "#4b5563", fontSize: "12px", marginTop: "6px" }}>
                20-day: {formatPrice(predict.ma20, isIndian)} · 50-day: {formatPrice(predict.ma50, isIndian)}
              </p>
            </div>
          </div>
        )}
        <div style={{ backgroundColor: "#111827", border: "1px solid #1f2937", borderRadius: "12px", padding: "24px" }}>
          <h2 style={{ color: "white", fontSize: "16px", fontWeight: "600", marginBottom: "16px" }}>Key Stats</h2>
          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "12px" }}>
            {[
              ["P/E Ratio",  stock.pe_ratio?.toFixed(1) ?? "—"],
              ["52W High",   formatPrice(stock.high_52w, isIndian)],
              ["52W Low",    formatPrice(stock.low_52w,  isIndian)],
              ["Market Cap", formatCap(stock.market_cap, isIndian)],
            ].map(([l, v]) => (
              <div key={l} style={{ backgroundColor: "#1f2937", borderRadius: "8px", padding: "12px" }}>
                <p style={{ color: "#6b7280", fontSize: "12px" }}>{l}</p>
                <p style={{ color: "white", fontSize: "16px", fontWeight: "600", marginTop: "4px" }}>{v}</p>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Insights */}
      <div style={{ backgroundColor: "#111827", border: "1px solid #1f2937", borderRadius: "12px", padding: "24px", marginBottom: "24px" }}>
        <h2 style={{ color: "white", fontSize: "16px", fontWeight: "600", marginBottom: "16px" }}>AI Insights</h2>
        <div style={{ display: "flex", flexDirection: "column", gap: "10px" }}>
          {insights.map((ins, i) => {
            const c = IC[ins.type] || IC.neutral;
            return (
              <div key={i} style={{ backgroundColor: c.bg, border: "1px solid " + c.border, borderRadius: "8px", padding: "12px 16px" }}>
                <p style={{ color: c.text, fontSize: "14px" }}>{ins.text}</p>
              </div>
            );
          })}
        </div>
      </div>

      {/* Competitors */}
      {competitors.length > 0 && (
        <div style={{ backgroundColor: "#111827", border: "1px solid #1f2937", borderRadius: "12px", padding: "24px", marginBottom: "24px" }}>
          <h2 style={{ color: "white", fontSize: "16px", fontWeight: "600", marginBottom: "16px" }}>Competitor Comparison</h2>
          <div style={{ overflowX: "auto" }}>
            <table style={{ width: "100%", borderCollapse: "collapse" }}>
              <thead>
                <tr style={{ backgroundColor: "#1f2937" }}>
                  {["Company", "Price", "Change", "Market Cap", "P/E Ratio", "Profit Margin"].map(h => (
                    <th key={h} style={{ color: "#6b7280", fontSize: "13px", padding: "10px 14px", textAlign: "left", fontWeight: "500" }}>{h}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                <tr style={{ backgroundColor: "#1e3a5f", borderBottom: "1px solid #1f2937" }}>
                  <td style={{ padding: "10px 14px" }}>
                    <p style={{ color: "#60a5fa", fontWeight: "bold", fontSize: "14px" }}>{stock.symbol} ★</p>
                    <p style={{ color: "#6b7280", fontSize: "11px" }}>{stock.name?.slice(0, 20)}</p>
                  </td>
                  <td style={{ padding: "10px 14px", color: "white", fontSize: "14px" }}>{formatPrice(stock.price, isIndian)}</td>
                  <td style={{ padding: "10px 14px", color: isUp ? "#34d399" : "#f87171", fontSize: "14px" }}>
                    {isUp ? "+" : ""}{stock.change_pct?.toFixed(2)}%
                  </td>
                  <td style={{ padding: "10px 14px", color: "white", fontSize: "14px" }}>{formatCap(stock.market_cap, isIndian)}</td>
                  <td style={{ padding: "10px 14px", color: "white", fontSize: "14px" }}>{stock.pe_ratio?.toFixed(1) ?? "—"}</td>
                  <td style={{ padding: "10px 14px", color: "white", fontSize: "14px" }}>—</td>
                </tr>
                {competitors.map((comp, i) => {
                  const compIsIndian = comp.symbol?.endsWith(".NS") || comp.symbol?.endsWith(".BO");
                  return (
                    <tr key={comp.symbol} style={{ borderBottom: "1px solid #1f2937", backgroundColor: i % 2 === 0 ? "" : "#0d1117" }}>
                      <td style={{ padding: "10px 14px" }}>
                        <p style={{ color: "white", fontWeight: "600", fontSize: "14px" }}>{comp.symbol}</p>
                        <p style={{ color: "#6b7280", fontSize: "11px" }}>{comp.name?.slice(0, 20)}</p>
                      </td>
                      <td style={{ padding: "10px 14px", color: "white", fontSize: "14px" }}>{formatPrice(comp.price, compIsIndian)}</td>
                      <td style={{ padding: "10px 14px", color: comp.change_pct >= 0 ? "#34d399" : "#f87171", fontSize: "14px" }}>
                        {comp.change_pct >= 0 ? "+" : ""}{comp.change_pct?.toFixed(2)}%
                      </td>
                      <td style={{ padding: "10px 14px", color: "white", fontSize: "14px" }}>{formatCap(comp.market_cap, compIsIndian)}</td>
                      <td style={{ padding: "10px 14px", color: "white", fontSize: "14px" }}>{comp.pe_ratio?.toFixed(1) ?? "—"}</td>
                      <td style={{ padding: "10px 14px", color: "white", fontSize: "14px" }}>
                        {comp.profit_margins ? (comp.profit_margins * 100).toFixed(1) + "%" : "—"}
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* News */}
      <div style={{ backgroundColor: "#111827", border: "1px solid #1f2937", borderRadius: "12px", padding: "24px" }}>
        <h2 style={{ color: "white", fontSize: "16px", fontWeight: "600", marginBottom: "16px" }}>Latest News</h2>
        <div style={{ display: "flex", flexDirection: "column", gap: "10px" }}>
          {news.slice(0, 6).map((a, i) => (
            <a key={i} href={a.url} target="_blank" rel="noreferrer" style={{ textDecoration: "none" }}>
              <div style={{ backgroundColor: "#1f2937", borderRadius: "8px", padding: "14px 16px" }}
                onMouseEnter={e => e.currentTarget.style.backgroundColor = "#374151"}
                onMouseLeave={e => e.currentTarget.style.backgroundColor = "#1f2937"}>
                <p style={{ color: "white", fontSize: "14px", fontWeight: "500", lineHeight: "1.4" }}>{a.title}</p>
                <p style={{ color: "#6b7280", fontSize: "12px", marginTop: "6px" }}>{a.source} · {a.date}</p>
              </div>
            </a>
          ))}
        </div>
      </div>

    </div>
  );
}
