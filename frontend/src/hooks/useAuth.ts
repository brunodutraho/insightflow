import { useState, useEffect, useCallback } from 'react';
import { useRouter } from 'next/navigation';
import { login, logout, verifyToken, isTokenValid, getTokenPayload } from '@/services/auth.service';

interface User {
  id: string;
  email: string;
  full_name: string;
  role: string;
  status: string;
  email_verified: boolean;
  tenant_id?: string;
}

interface AuthState {
  user: User | null;
  isLoading: boolean;
  isAuthenticated: boolean;
  error: string | null;
}

export function useAuth() {
  const router = useRouter();
  const [authState, setAuthState] = useState<AuthState>({
    user: null,
    isLoading: true,
    isAuthenticated: false,
    error: null,
  });

  // Check authentication on mount
  useEffect(() => {
    checkAuth();
  }, []);

  const checkAuth = useCallback(async () => {
    setAuthState(prev => ({ ...prev, isLoading: true, error: null }));

    try {
      // First check if token exists and is not expired
      if (!isTokenValid()) {
        setAuthState({
          user: null,
          isLoading: false,
          isAuthenticated: false,
          error: null,
        });
        return;
      }

      // Verify token with server
      const result = await verifyToken();

      if (result?.valid && result?.user) {
        setAuthState({
          user: result.user,
          isLoading: false,
          isAuthenticated: true,
          error: null,
        });
      } else {
        // Token invalid, clear it
        logout();
        setAuthState({
          user: null,
          isLoading: false,
          isAuthenticated: false,
          error: null,
        });
      }
    } catch (error: any) {
      console.error('Auth check failed:', error);
      logout();
      setAuthState({
        user: null,
        isLoading: false,
        isAuthenticated: false,
        error: error.message || 'Erro ao verificar autenticação',
      });
    }
  }, []);

  const signIn = useCallback(async (email: string, password: string) => {
    setAuthState(prev => ({ ...prev, isLoading: true, error: null }));

    try {
      const result = await login({ email, password });

      if (result?.access_token) {
        // Re-check auth to get user data
        await checkAuth();
        return { success: true };
      } else {
        throw new Error('Login falhou - token não recebido');
      }
    } catch (error: any) {
      const errorMessage = error.response?.data?.detail ||
                          error.message ||
                          'Erro ao fazer login';

      setAuthState(prev => ({
        ...prev,
        isLoading: false,
        error: errorMessage,
      }));

      return { success: false, error: errorMessage };
    }
  }, [checkAuth]);

  const signOut = useCallback(() => {
    logout();
    setAuthState({
      user: null,
      isLoading: false,
      isAuthenticated: false,
      error: null,
    });
    router.push('/login');
  }, [router]);

  const clearError = useCallback(() => {
    setAuthState(prev => ({ ...prev, error: null }));
  }, []);

  return {
    user: authState.user,
    isLoading: authState.isLoading,
    isAuthenticated: authState.isAuthenticated,
    error: authState.error,
    signIn,
    signOut,
    checkAuth,
    clearError,
  };
}