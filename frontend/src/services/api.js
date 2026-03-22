import axios from "axios";

const api = axios.create({ baseURL: "http://localhost:8000/api" });

export const getStock      = (s)    => api.get(`/stocks/${s}`);
export const getHistory    = (s, p) => api.get(`/stocks/${s}/history?period=${p}`);
export const getMarket     = ()     => api.get("/stocks/market/overview");
export const getNews       = (s)    => api.get(`/news/${s}`);
export const getPrediction = (s)    => api.get(`/predict/${s}`);
export const getInsights   = (s)    => api.get(`/insights/${s}`);