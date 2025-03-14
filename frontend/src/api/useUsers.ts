import { useState, useEffect } from "react";
import { api } from "./api";

export interface User {
  id: number;
  username: string;
  email: string;
  is_staff: boolean;
  role: string;
}

export const useUsers = () => {
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchUsers = async () => {
      try {
        const response = await api.get<User[]>("/users/");
        console.log("Usuarios obtenidos desde la API:", response.data); // ← Debug aquí
        setUsers(response.data);
        response.data.forEach(user => {
            console.log(`Usuario: ${user.username}, Role: ${user.role}`);
        });
      } catch (err) {
        setError("Error al obtener usuarios");
      } finally {
        setLoading(false);
      }
    };

    fetchUsers();
  }, []);

  const createUser = async (username: string, email: string, password: string, role: string) => {
    try {
      let userData: any = { username, email, password, role }; // Agregar `role`
  
      const response = await api.post("/users/", userData);
      setUsers([...users, response.data]); // Agregar el nuevo usuario a la lista
      return { success: true };
    } catch (error) {
      return { success: false, message: "Error al crear usuario" };
    }
  };

  const deleteUser = async (userId: number) => {
    try {
      await api.delete(`/users/${userId}/`);
      setUsers(users.filter(user => user.id !== userId)); // Remover usuario de la lista
      return { success: true };
    } catch (error) {
      return { success: false, message: "Error al eliminar usuario" };
    }
  };

  return { users, loading, error, createUser, deleteUser };
  
};
