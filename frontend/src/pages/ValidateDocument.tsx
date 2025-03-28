import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { api } from "../api/api";

interface DocumentData {
  title: string;
  file_url: string;
  qr_code_url: string;
  uploaded_at: string;
  signature_valid: boolean;
}

const ValidateDocument = () => {
  const { id } = useParams();
  const [data, setData] = useState<DocumentData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchDocument = async () => {
      try {
        const response = await api.get(`/documents/validate/${id}/`);
        setData(response.data);
      } catch (err) {
        setError("No se pudo validar el documento.");
      } finally {
        setLoading(false);
      }
    };

    fetchDocument();
  }, [id]);

  if (loading) return <p>Validando documento...</p>;
  if (error) return <p className="text-red-600">{error}</p>;

  return (
    <div className="p-4 max-w-xl mx-auto">
      <h1 className="text-2xl font-bold mb-4">Resultado de Validación</h1>
      <p><strong>Título:</strong> {data?.title}</p>
      <p><strong>Subido el:</strong> {new Date(data!.uploaded_at).toLocaleString()}</p>
      <p>
        <strong>Firma digital:</strong>{" "}
        <span className={data!.signature_valid ? "text-green-600" : "text-red-600"}>
          {data!.signature_valid ? "VÁLIDA ✅" : "INVÁLIDA ❌"}
        </span>
      </p>
      <div className="mt-4">
        <a href={data!.file_url} download className="text-blue-600 underline">
            Descargar documento
        </a>
      </div>
      <div className="mt-4">
        <img src={data!.qr_code_url} alt="Código QR" />
      </div>
    </div>
  );
};

export default ValidateDocument;
