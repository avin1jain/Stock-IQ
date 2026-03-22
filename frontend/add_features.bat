@echo off
title Adding New Features...
color 0A
echo Adding all missing features...

cd %USERPROFILE%\Desktop\stock-app\frontend\src\pages

(
echo import { useState } from "react";
echo import axios from "axios";
echo.
echo const METRICS = [
echo   ["P/E Ratio", "pe_ratio"],
echo   ["P/B Ratio", "pb_ratio"],
echo   ["ROE", "roe"],
echo   ["Profit Margin", "profit_margins"],
echo   ["Debt/Equity", "debt_to_equity"],
echo   ["Revenue Growth", "revenue_growth"],
echo   ["Market Cap", "market_cap"],
echo ];
echo.
echo export default function Compare(^) {
echo   const [sym1, setSym1] = useState("AAPL"^);
echo   const [sym2, setSym2] = useState("MSFT"^);
echo   const [data, setData] = useState(null^);
echo   const [loading, setLoading] = useState(false^);
echo   const [error, setError] = useState(""^);
echo.
echo   async function compare(^) {
echo     setLoading(true^); setError(""^);
echo     try {
echo       const [r1, r2] = await Promise.all([
echo         axios.get("http://localhost:8000/api/stocks/" + sym1^),
echo         axios.get("http://localhost:8000/api/stocks/" + sym2^),
echo       ]^);
echo       setData({ c1: r1.data, c2: r2.data }^);
echo     } catch { setError("Could not load data. Check symbols."^); }
echo     setLoading(false^);
echo   }
echo.
echo   function fmt(key, val^) {
echo     if (val === null ^|^| val === undefined^) return "—";
echo     if (key === "roe" ^|^| key === "profit_margins" ^|^| key === "revenue_growth"^) return (val * 100^).toFixed(1^) + "%%";
echo     if (key === "market_cap"^) return val ^>= 1e12 ? "$" + (val/1e12^).toFixed(2^) + "T" : "$" + (val/1e9^).toFixed(1^) + "B";
echo     return val.toFixed(2^);
echo   }
echo.
echo   return (
echo     ^<div style={{maxWidth:"900px",margin:"0 auto",padding:"32px 24px"}}^>
echo       ^<h1 style={{color:"white",fontSize:"28px",fontWeight:"bold",marginBottom:"6px"}}^>Compare Companies^</h1^>
echo       ^<p style={{color:"#6b7280",marginBottom:"28px"}}^>Side by side financial comparison^</p^>
echo       ^<div style={{display:"flex",gap:"12px",marginBottom:"32px",flexWrap:"wrap"}}^>
echo         ^<input value={sym1} onChange={e=^>setSym1(e.target.value.toUpperCase(^)^)} placeholder="Symbol 1 e.g. AAPL" style={{flex:1,backgroundColor:"#111827",border:"1px solid #374151",borderRadius:"8px",padding:"12px 16px",color:"white",fontSize:"16px",fontWeight:"bold",textAlign:"center",outline:"none"}} /^>
echo         ^<input value={sym2} onChange={e=^>setSym2(e.target.value.toUpperCase(^)^)} placeholder="Symbol 2 e.g. MSFT" style={{flex:1,backgroundColor:"#111827",border:"1px solid #374151",borderRadius:"8px",padding:"12px 16px",color:"white",fontSize:"16px",fontWeight:"bold",textAlign:"center",outline:"none"}} /^>
echo         ^<button onClick={compare} disabled={loading} style={{backgroundColor:"#3b82f6",color:"white",border:"none",borderRadius:"8px",padding:"12px 28px",cursor:"pointer",fontSize:"15px"}}^>{loading?"Loading...":"Compare"}^</button^>
echo       ^</div^>
echo       {error ^&^& ^<p style={{color:"#f87171",marginBottom:"16px"}}^>{error}^</p^>}
echo       {data ^&^& (
echo         ^<div style={{backgroundColor:"#111827",border:"1px solid #1f2937",borderRadius:"12px",overflow:"hidden"}}^>
echo           ^<div style={{display:"grid",gridTemplateColumns:"1fr 1fr 1fr",backgroundColor:"#1f2937",padding:"16px"}}^>
echo             ^<p style={{color:"#6b7280",fontSize:"14px"}}^>Metric^</p^>
echo             ^<p style={{color:"white",fontWeight:"bold",fontSize:"18px",textAlign:"center"}}^>{data.c1.symbol}^</p^>
echo             ^<p style={{color:"white",fontWeight:"bold",fontSize:"18px",textAlign:"center"}}^>{data.c2.symbol}^</p^>
echo           ^</div^>
echo           ^<div style={{display:"grid",gridTemplateColumns:"1fr 1fr 1fr",padding:"12px 16px",borderTop:"1px solid #1f2937"}}^>
echo             ^<p style={{color:"#6b7280",fontSize:"14px"}}^>Price^</p^>
echo             ^<p style={{color:"white",fontWeight:"600",textAlign:"center"}}^>${data.c1.price?.toFixed(2^)}^</p^>
echo             ^<p style={{color:"white",fontWeight:"600",textAlign:"center"}}^>${data.c2.price?.toFixed(2^)}^</p^>
echo           ^</div^>
echo           ^<div style={{display:"grid",gridTemplateColumns:"1fr 1fr 1fr",padding:"12px 16px",borderTop:"1px solid #1f2937"}}^>
echo             ^<p style={{color:"#6b7280",fontSize:"14px"}}^>Change Today^</p^>
echo             ^<p style={{color:data.c1.change_pct^>=0?"#34d399":"#f87171",fontWeight:"600",textAlign:"center"}}^>{data.c1.change_pct^>=0?"+":""}{data.c1.change_pct?.toFixed(2^)}%%^</p^>
echo             ^<p style={{color:data.c2.change_pct^>=0?"#34d399":"#f87171",fontWeight:"600",textAlign:"center"}}^>{data.c2.change_pct^>=0?"+":""}{data.c2.change_pct?.toFixed(2^)}%%^</p^>
echo           ^</div^>
echo           {METRICS.map(([label,key],i^)=^>(
echo             ^<div key={key} style={{display:"grid",gridTemplateColumns:"1fr 1fr 1fr",padding:"12px 16px",borderTop:"1px solid #1f2937",backgroundColor:i%%2===0?"":"#0d1117"}}^>
echo               ^<p style={{color:"#6b7280",fontSize:"14px"}}^>{label}^</p^>
echo               ^<p style={{color:"white",fontWeight:"600",textAlign:"center"}}^>{fmt(key,data.c1[key]^)}^</p^>
echo               ^<p style={{color:"white",fontWeight:"600",textAlign:"center"}}^>{fmt(key,data.c2[key]^)}^</p^>
echo             ^</div^>
echo           ^)^)}
echo         ^</div^>
echo       ^)}
echo     ^</div^>
echo   ^);
echo }
) > Compare.jsx

(
echo import { useState, useEffect } from "react";
echo import { useNavigate } from "react-router-dom";
echo import axios from "axios";
echo.
echo export default function Watchlist(^) {
echo   const [watchlist, setWatchlist] = useState(() =^> JSON.parse(localStorage.getItem("watchlist"^) ^|^| "[]"^)^);
echo   const [stocks, setStocks] = useState([]^);
echo   const [input, setInput] = useState(""^);
echo   const navigate = useNavigate(^);
echo.
echo   useEffect((^) =^> {
echo     if (watchlist.length === 0^) return;
echo     Promise.all(watchlist.map(s =^> axios.get("http://localhost:8000/api/stocks/" + s^).then(r =^> r.data^)^)^)
echo       .then(setStocks^).catch((^) =^> {});
echo   }, [watchlist]^);
echo.
echo   function addStock(^) {
echo     if (!input.trim(^)^) return;
echo     const sym = input.trim(^).toUpperCase(^);
echo     if (!watchlist.includes(sym^)^) {
echo       const updated = [...watchlist, sym];
echo       setWatchlist(updated^);
echo       localStorage.setItem("watchlist", JSON.stringify(updated^)^);
echo     }
echo     setInput(""^);
echo   }
echo.
echo   function removeStock(sym^) {
echo     const updated = watchlist.filter(s =^> s !== sym^);
echo     setWatchlist(updated^);
echo     localStorage.setItem("watchlist", JSON.stringify(updated^)^);
echo     setStocks(stocks.filter(s =^> s.symbol !== sym^)^);
echo   }
echo.
echo   return (
echo     ^<div style={{maxWidth:"900px",margin:"0 auto",padding:"32px 24px"}}^>
echo       ^<h1 style={{color:"white",fontSize:"28px",fontWeight:"bold",marginBottom:"6px"}}^>My Watchlist^</h1^>
echo       ^<p style={{color:"#6b7280",marginBottom:"28px"}}^>Track your favourite stocks^</p^>
echo       ^<div style={{display:"flex",gap:"12px",marginBottom:"32px"}}^>
echo         ^<input value={input} onChange={e=^>setInput(e.target.value.toUpperCase(^)^)} onKeyDown={e=^>e.key==="Enter"^&^&addStock(^)} placeholder="Add symbol e.g. AAPL or RELIANCE.NS" style={{flex:1,backgroundColor:"#111827",border:"1px solid #374151",borderRadius:"8px",padding:"12px 16px",color:"white",fontSize:"15px",outline:"none"}} /^>
echo         ^<button onClick={addStock} style={{backgroundColor:"#3b82f6",color:"white",border:"none",borderRadius:"8px",padding:"12px 24px",cursor:"pointer",fontSize:"15px"}}^>Add^</button^>
echo       ^</div^>
echo       {watchlist.length === 0 ^&^& ^<p style={{color:"#6b7280"}}^>No stocks added yet. Add a symbol above!^</p^>}
echo       ^<div style={{display:"grid",gridTemplateColumns:"repeat(3,1fr)",gap:"16px"}}^>
echo         {stocks.map(s=^>(
echo           ^<div key={s.symbol} style={{backgroundColor:"#111827",border:"1px solid #1f2937",borderRadius:"12px",padding:"20px",cursor:"pointer"}} onClick={(^)=^>navigate("/stock/"+s.symbol^)} onMouseEnter={e=^>e.currentTarget.style.borderColor="#3b82f6"} onMouseLeave={e=^>e.currentTarget.style.borderColor="#1f2937"}^>
echo             ^<div style={{display:"flex",justifyContent:"space-between"}}^>
echo               ^<p style={{color:"white",fontWeight:"bold",fontSize:"18px"}}^>{s.symbol}^</p^>
echo               ^<button onClick={e=^>{e.stopPropagation(^);removeStock(s.symbol^);}} style={{backgroundColor:"#450a0a",color:"#f87171",border:"none",borderRadius:"6px",padding:"2px 8px",cursor:"pointer",fontSize:"12px"}}^>Remove^</button^>
echo             ^</div^>
echo             ^<p style={{color:"#6b7280",fontSize:"12px",marginTop:"2px"}}^>{s.name?.slice(0,20^)}^</p^>
echo             ^<p style={{color:"white",fontSize:"24px",fontWeight:"bold",marginTop:"12px"}}^>${s.price?.toFixed(2^)}^</p^>
echo             ^<p style={{color:s.change_pct^>=0?"#34d399":"#f87171",fontSize:"14px",marginTop:"4px"}}^>{s.change_pct^>=0?"+":""}{s.change_pct?.toFixed(2^)}%%^</p^>
echo           ^</div^>
echo         ^)^)}
echo       ^</div^>
echo     ^</div^>
echo   ^);
echo }
) > Watchlist.jsx

echo Pages created!

cd %USERPROFILE%\Desktop\stock-app\frontend\src
(
echo import { BrowserRouter, Routes, Route } from "react-router-dom";
echo import Navbar from "./components/Navbar";
echo import Home from "./pages/Home";
echo import StockDetail from "./pages/StockDetail";
echo import News from "./pages/News";
echo import Compare from "./pages/Compare";
echo import Watchlist from "./pages/Watchlist";
echo.
echo export default function App(^) {
echo   return (
echo     ^<BrowserRouter^>
echo       ^<div style={{minHeight:"100vh",backgroundColor:"#030712"}}^>
echo         ^<Navbar /^>
echo         ^<Routes^>
echo           ^<Route path="/" element={^<Home /^>} /^>
echo           ^<Route path="/stock/:symbol" element={^<StockDetail /^>} /^>
echo           ^<Route path="/news" element={^<News /^>} /^>
echo           ^<Route path="/compare" element={^<Compare /^>} /^>
echo           ^<Route path="/watchlist" element={^<Watchlist /^>} /^>
echo         ^</Routes^>
echo       ^</div^>
echo     ^</BrowserRouter^>
echo   ^);
echo }
) > App.jsx

cd %USERPROFILE%\Desktop\stock-app\frontend\src\components
(
echo import { useState } from "react";
echo import { useNavigate, Link } from "react-router-dom";
echo import axios from "axios";
echo.
echo export default function Navbar(^) {
echo   const [query, setQuery] = useState(""^);
echo   const [searching, setSearching] = useState(false^);
echo   const navigate = useNavigate(^);
echo.
echo   async function handleSearch(e^) {
echo     e.preventDefault(^);
echo     if (!query.trim(^)^) return;
echo     setSearching(true^);
echo     try {
echo       const res = await axios.get("http://localhost:8000/api/search/" + query.trim(^)^);
echo       navigate("/stock/" + res.data.symbol^);
echo       setQuery(""^);
echo     } catch {
echo       navigate("/stock/" + query.trim(^).toUpperCase(^)^);
echo       setQuery(""^);
echo     }
echo     setSearching(false^);
echo   }
echo.
echo   return (
echo     ^<nav style={{backgroundColor:"#111827",borderBottom:"1px solid #1f2937",padding:"12px 24px",display:"flex",alignItems:"center",justifyContent:"space-between",flexWrap:"wrap",gap:"12px"}}^>
echo       ^<Link to="/" style={{color:"#60a5fa",fontWeight:"bold",fontSize:"20px",textDecoration:"none"}}^>StockIQ^</Link^>
echo       ^<form onSubmit={handleSearch} style={{display:"flex",gap:"8px"}}^>
echo         ^<input value={query} onChange={e=^>setQuery(e.target.value^)} placeholder="Search... Apple Reliance TCS" style={{backgroundColor:"#1f2937",border:"1px solid #374151",borderRadius:"8px",padding:"8px 14px",color:"white",fontSize:"14px",width:"260px",outline:"none"}} /^>
echo         ^<button type="submit" disabled={searching} style={{backgroundColor:searching?"#1d4ed8":"#3b82f6",color:"white",border:"none",borderRadius:"8px",padding:"8px 16px",cursor:"pointer",fontSize:"14px"}}^>{searching?"...":"Search"}^</button^>
echo       ^</form^>
echo       ^<div style={{display:"flex",gap:"20px"}}^>
echo         ^<Link to="/" style={{color:"#9ca3af",textDecoration:"none",fontSize:"14px"}}^>Home^</Link^>
echo         ^<Link to="/compare" style={{color:"#9ca3af",textDecoration:"none",fontSize:"14px"}}^>Compare^</Link^>
echo         ^<Link to="/watchlist" style={{color:"#9ca3af",textDecoration:"none",fontSize:"14px"}}^>Watchlist^</Link^>
echo         ^<Link to="/news" style={{color:"#9ca3af",textDecoration:"none",fontSize:"14px"}}^>News^</Link^>
echo       ^</div^>
echo     ^</nav^>
echo   ^);
echo }
) > Navbar.jsx

echo.
echo ============================================
echo   ALL FEATURES ADDED SUCCESSFULLY!
echo ============================================
echo.
echo Now run: npm run dev
echo.
pause