import DocumentUploadForm from "../components/DocumentUploadForm";
import DocumentList from "../components/DocumentList";

const Upload = () => {
  return (
    <div className="container mx-auto p-6">
      <h1 className="text-2xl font-bold mb-4">Gestión de Documentos</h1>
      <DocumentUploadForm />
      <div className="mt-6">
        <DocumentList />
      </div>
    </div>
  );
};

export default Upload;