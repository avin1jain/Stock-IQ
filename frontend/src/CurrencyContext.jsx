import { createContext, useContext, useState, useEffect } from "react";
import axios from "axios";

const CurrencyContext = createContext();

export function CurrencyProvider({ children }) {
  const [currency, setCurrency] = useState("USD");
  const [rates, setRates] = useState({ usd_to_inr: 83.50, inr_to_usd: 0.011976 });

  useEffect(() => {
    axios.get("http://localhost:8000/api/currency/rates")
      .then(r => setRates(r.data))
      .catch(() => {});
  }, []);

  function convert(amount, isIndianStock) {
    if (!amount) return 0;
    if (currency === "INR") {
      // Show everything in INR
      if (isIndianStock) return amount; // already in INR
      return amount * rates.usd_to_inr; // convert USD to INR
    } else {
      // Show everything in USD
      if (!isIndianStock) return amount; // already in USD
      return amount * rates.inr_to_usd; // convert INR to USD
    }
  }

  function symbol() {
    return currency === "INR" ? "₹" : "$";
  }

  function formatPrice(amount, isIndianStock) {
    const converted = convert(amount, isIndianStock);
    if (!converted) return symbol() + "0";
    return symbol() + converted.toLocaleString("en-IN", { maximumFractionDigits: 2 });
  }

  function formatCap(amount, isIndianStock) {
    const converted = convert(amount, isIndianStock);
    if (!converted) return "—";
    if (converted >= 1e12) return symbol() + (converted / 1e12).toFixed(2) + "T";
    if (converted >= 1e9)  return symbol() + (converted / 1e9).toFixed(1) + "B";
    if (converted >= 1e7)  return symbol() + (converted / 1e7).toFixed(1) + "Cr";
    return symbol() + converted.toLocaleString("en-IN", { maximumFractionDigits: 0 });
  }

  return (
    <CurrencyContext.Provider value={{ currency, setCurrency, rates, convert, symbol, formatPrice, formatCap }}>
      {children}
    </CurrencyContext.Provider>
  );
}

export function useCurrency() {
  return useContext(CurrencyContext);
}
