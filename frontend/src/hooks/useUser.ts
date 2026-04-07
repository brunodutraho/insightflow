// src/hooks/useUser.ts
import { useMemo } from "react";
import { jwtDecode } from "jwt-decode";
import Cookies from "js-cookie";

// 1. Atualizado: Lista completa de cargos do seu novo Enum
export type UserRole = 

  | "admin_master" 
  | "gerente" 
  | "administrativo" 

  | "suporte" 
  | "marketing" 
  | "gestor_interno" 

  | "gestor_assinante" 
  | "cliente_final";

interface JWTPayload {
  sub: string;        // ID do usuário (UUID)
  role: UserRole;     // Novo padrão de cargos
  tenant_id: string;  // Mudamos de client_id (number) para tenant_id (string/UUID)
  email: string;
  exp: number;
}

interface UserState {
  id: string | null;
  role: UserRole | null;
  tenant_id: string | null;
  email: string | null;
  isLoggedIn: boolean;
}

export function useUser() {
  const user: UserState = useMemo(() => {
    const token = Cookies.get("token");

    if (!token) {
      return { id: null, role: null, tenant_id: null, email: null, isLoggedIn: false };
    }

    try {
      const decoded = jwtDecode<JWTPayload>(token);

      return {
        id: decoded.sub,
        role: decoded.role,
        tenant_id: decoded.tenant_id, // Sincronizado com o token_service do backend
        email: decoded.email,
        isLoggedIn: true,
      };
    } catch (error) {
      console.error("Token inválido ou expirado:", error);
      // Opcional: Cookies.remove("token"); // Remove se o token estiver corrompido
      return { id: null, role: null, tenant_id: null, email: null, isLoggedIn: false };
    }
  }, []); // Dependência vazia para rodar apenas na montagem ou quando o token mudar (se usar estado)

  return { user };
}
