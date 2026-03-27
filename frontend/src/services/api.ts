import axios from "axios";

const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL,
});

// Este interceptor anexa o token em TODA requisição automaticamente
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token"); // Onde vamos salvar o token
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default api;
