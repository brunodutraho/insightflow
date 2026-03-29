import { useUser } from "./useUser";

export function useAuth() {
  const { user } = useUser();

  return {
    user,
    isAuthenticated: user.isLoggedIn,
  };
}