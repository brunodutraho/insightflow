import api from "./api";

// =========================
// REGISTER
// =========================
export async function register(data: { email: string; password: string }) {
  const res = await api.post("/auth/register", data);

  // ✅ salva email para fluxo de verificação
  if (typeof window !== "undefined") {
    localStorage.setItem("email", data.email);
  }

  return res.data;
}

// =========================
// LOGIN (PADRÃO JSON)
// =========================
export async function login(data: { email: string; password: string }) {
  const res = await api.post("/auth/login", {
    email: data.email,
    password: data.password,
  });

  // ✅ salva token corretamente
  if (typeof window !== "undefined") {
    localStorage.setItem("token", res.data.access_token);
  }

  return res.data;
}

// =========================
// TOKEN VALIDATION (CLIENT SIDE)
// =========================
export function isTokenValid(): boolean {
  if (typeof window === "undefined") return false;

  const token = localStorage.getItem("token");
  if (!token) return false;

  try {
    const payload = JSON.parse(atob(token.split(".")[1]));
    const exp = payload.exp;
    const now = Math.floor(Date.now() / 1000);

    return exp > now;
  } catch {
    return false;
  }
}

// =========================
// GET TOKEN PAYLOAD
// =========================
export function getTokenPayload(): any | null {
  if (typeof window === "undefined") return null;

  const token = localStorage.getItem("token");
  if (!token) return null;

  try {
    return JSON.parse(atob(token.split(".")[1]));
  } catch {
    return null;
  }
}

// =========================
// VERIFY TOKEN (BACKEND)
// =========================
export async function verifyToken() {
  try {
    const res = await api.get("/auth/verify-token");
    return res.data;
  } catch {
    return null;
  }
}

// =========================
// LOGOUT
// =========================
export function logout() {
  if (typeof window !== "undefined") {
    localStorage.removeItem("token");

    // limpa cookie também (caso exista)
    document.cookie =
      "token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
  }
}

// =========================
// VERIFY EMAIL (COM AUTO LOGIN)
// =========================
// =========================
export async function verifyEmail(data: { token?: string; code?: string }) {
  // Se o componente enviou 'token' (os 6 dígitos), mandamos como 'code' para o backend
  const payload = {
    code: data.code || data.token,
    token: data.token // Mantemos o token caso a rota aceite os dois
  };

  const res = await api.post("/auth/verify-email", payload);

  // AUTO LOGIN
  if (res.data?.access_token && typeof window !== "undefined") {
    localStorage.setItem("token", res.data.access_token);
  }

  return res.data;
}


// =========================
// RESEND CODE
// =========================
export async function resendCode(email: string) {
  const res = await api.post("/auth/resend-verification", { email });
  return res.data;
}

// =========================
// SOCIAL LOGIN HELPER
// =========================
export function handleOAuthSuccess(token: string) {
  if (typeof window !== "undefined" && token) {
    localStorage.setItem("token", token);
    return true;
  }
  return false;
}
