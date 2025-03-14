import { useUsers } from "../api/useUsers";
import { useState } from "react";

const Users = () => {
  const { users, loading, error, createUser, deleteUser } = useUsers();
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState(""); // Agregar estado para la contraseña
  const [role, setRole] = useState("User"); // Por defecto "User"

  const handleCreateUser = async (e: React.FormEvent) => {
    e.preventDefault();
    if (password.length < 6) {
      alert("La contraseña debe tener al menos 6 caracteres.");
      return;
    }

    const result = await createUser(username, email, password, role);
    if (result.success) {
      setUsername("");
      setEmail("");
      setPassword(""); // Resetear el password después de crear usuario
      setRole("User"); 
    } else {
      alert(result.message);
    }
  };

  if (loading) return <p>Cargando usuarios...</p>;
  if (error) return <p>{error}</p>;

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Gestión de Usuarios</h1>

      {/* Formulario de Creación */}
      <form onSubmit={handleCreateUser} className="mb-4">
        <input
          type="text"
          placeholder="Usuario"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          className="p-2 border rounded mr-2"
        />
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          className="p-2 border rounded mr-2"
        />
        <input
          type="password"
          placeholder="Contraseña"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="p-2 border rounded mr-2"
        />

        <select value={role} onChange={(e) => setRole(e.target.value)} className="p-2 border rounded mr-2">
          <option value="User">Usuario</option>
          <option value="Admin">Administrador</option>
          <option value="Editor">Editor</option>
        </select>

        <button type="submit" className="bg-green-500 text-white p-2 rounded">Crear</button>
      </form>

      {/* Tabla de Usuarios */}
      <table className="w-full border-collapse border border-gray-300">
        <thead>
          <tr className="bg-gray-200">
            <th className="border p-2">ID</th>
            <th className="border p-2">Usuario</th>
            <th className="border p-2">Email</th>
            <th className="border p-2">Rol</th>
            <th className="border p-2">Acciones</th>
          </tr>
        </thead>
        <tbody>
          {users.map((user) => (
            <tr key={user.id} className="border">
              <td className="border p-2">{user.id}</td>
              <td className="border p-2">{user.username}</td>
              <td className="border p-2">{user.email}</td>
              <td className="border p-2">{user.role === "admin" ? "Administrador" : user.role === "editor" ? "Editor" : "Usuario"}</td>
              <td className="border p-2">
                <button onClick={() => deleteUser(user.id)} className="bg-red-500 text-white p-2 rounded">Eliminar</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default Users;
