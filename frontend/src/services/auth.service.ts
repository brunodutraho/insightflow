import api from "./api";

type LoginProps = {
  email: string;
  password: string;
};

export async function login({ email, password }: LoginProps) {
  const formData = new URLSearchParams();

  // ⚠️ FastAPI OAuth2 exige "username"
  formData.append("username", email);
  formData.append("password", password);

  const res = await api.post("/auth/login", formData, {
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
  });

  return res.data;
}