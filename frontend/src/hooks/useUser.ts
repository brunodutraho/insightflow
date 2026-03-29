// src/hooks/useUser.ts
import { useMemo } from "react";
import { jwtDecode } from "jwt-decode";
import Cookies from "js-cookie";

interface JWTPayload {
  sub: string;
  role: "admin" | "gestor" | "cliente";
  client_id: number;
  exp: number;
}

interface UserState {
  id: string | null;
  role: "admin" | "gestor" | "cliente" | null;
  client_id: number | null;
  isLoggedIn: boolean;
}

export function useUser() {
  const user: UserState = useMemo(() => {
    const token = Cookies.get("token");

    if (!token) {
      return { id: null, role: null, client_id: null, isLoggedIn: false };
    }

    try {
      const decoded = jwtDecode<JWTPayload>(token);

      return {
        id: decoded.sub,
        role: decoded.role,
        client_id: decoded.client_id,
        isLoggedIn: true,
      };
    } catch (error) {
      console.error("Token inválido:", error);
      return { id: null, role: null, client_id: null, isLoggedIn: false };
    }
  }, []);

  return { user };
}