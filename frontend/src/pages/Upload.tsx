import React from "react";
import DocumentUploadForm from "../components/DocumentUploadForm";
import DocumentList from "../components/DocumentList";
import Dashboard from "../components/Dashboard"; // ✅ Importar el Dashboard

const Upload = () => {
  return (
    <div className="container mx-auto p-6">
      <h1 className="text-2xl font-bold mb-4">Gestión de Documentos</h1>
      
      {/* Panel de métricas */}
      <Dashboard />

      {/* Formulario de subida */}
      <DocumentUploadForm />

      {/* Lista de documentos */}
      <div className="mt-6">
        <DocumentList />
      </div>
    </div>
  );
};

export default Upload;