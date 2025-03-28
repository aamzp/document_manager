import React, { JSX } from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import "./index.css";
import Users from "./pages/Users";
import Login from "./pages/Login";
import Upload from "./pages/Upload";  // Importamos la nueva página
import { useAuth } from "./api/useAuth";
import './styles.css';
import ValidateFromQR from "./pages/ValidateFromQR";
import ValidateDocument from "./pages/ValidateDocument";


const PrivateRoute = ({ children }: { children: JSX.Element }) => {
  const { token } = useAuth();
  return token ? children : <Navigate to="/login" />;
};

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/users" element={<PrivateRoute><Users /></PrivateRoute>} />
        <Route path="/upload" element={<PrivateRoute><Upload /></PrivateRoute>} /> {/* NUEVA RUTA PROTEGIDA */}
        <Route path="/scan" element={<PrivateRoute><ValidateFromQR /></PrivateRoute>} />
        <Route path="/validate/:id" element={<ValidateDocument />} />
        <Route path="/" element={<PrivateRoute><h1>Bienvenido</h1></PrivateRoute>} />
      </Routes>
    </BrowserRouter>
  </React.StrictMode>
);