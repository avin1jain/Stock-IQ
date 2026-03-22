import { BrowserRouter, Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import Home from "./pages/Home";
import StockDetail from "./pages/StockDetail";
import News from "./pages/News";
import Compare from "./pages/Compare";
import Watchlist from "./pages/Watchlist";

export default function App() {
  return (
    <BrowserRouter>
      <div style={{minHeight:"100vh",backgroundColor:"#030712"}}>
        <Navbar />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/stock/:symbol" element={<StockDetail />} />
          <Route path="/news" element={<News />} />
          <Route path="/compare" element={<Compare />} />
          <Route path="/watchlist" element={<Watchlist />} />
        </Routes>
      </div>
    </BrowserRouter>
  );
}
