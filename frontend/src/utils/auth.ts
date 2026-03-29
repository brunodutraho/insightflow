export function getUserFromToken() {
  if (typeof window === "undefined") return null;

  const token = localStorage.getItem("token");
  if (!token) return null;

  try {
    const payload = JSON.parse(atob(token.split(".")[1]));

    return {
      id: payload.sub,
      role: payload.role,
    };
  } catch {
    return null;
  }
}