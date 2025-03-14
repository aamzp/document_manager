import { useState } from "react";
import { api } from "./api";

export const useAuth = () => {
  const [token, setToken] = useState<string | null>(localStorage.getItem("token"));

  const login = async (username: string, password: string) => {
    try {
      const response = await api.post("/token/", { username, password });
      const accessToken = response.data.access;

      // Guardar token en localStorage
      localStorage.setItem("token", accessToken);
      setToken(accessToken);

      return { success: true };
    } catch (error) {
      return { success: false, message: "Credenciales incorrectas" };
    }
  };

  const logout = () => {
    localStorage.removeItem("token");
    setToken(null);
  };

  return { token, login, logout };
};
