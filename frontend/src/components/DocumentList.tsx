import { useEffect, useState } from "react";
import axios from "axios";
import { Button } from "../components/ui/button";

interface Document {
    id: number;
    title: string;
    file: string;
    uploaded_at: string;
    qr_code_url?: string;
    signature?: string;
    signature_valid: boolean;
}

const DocumentList = () => {
    const [documents, setDocuments] = useState<Document[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [selectedDocument, setSelectedDocument] = useState<number | null>(null);

    useEffect(() => {
        const fetchDocuments = async () => {
            try {
                const token = localStorage.getItem("token");
                const response = await axios.get("http://127.0.0.1:8000/api/documents/", {
                    headers: { Authorization: `Bearer ${token}` },
                });
                setDocuments(response.data);
            } catch (err) {
                setError("Error al cargar documentos");
            } finally {
                setLoading(false);
            }
        };

        fetchDocuments();
    }, []);

    const toggleDetails = async (docId: number) => {
        if (selectedDocument === docId) {
            setSelectedDocument(null);
            return;
        }

        try {
            const token = localStorage.getItem("token");
            const response = await axios.get(`http://127.0.0.1:8000/api/documents/${docId}/`, {
                headers: { Authorization: `Bearer ${token}` },
            });

            setDocuments((prevDocs) =>
                prevDocs.map((doc) =>
                    doc.id === docId ? { ...doc, ...response.data } : doc
                )
            );
            setSelectedDocument(docId);
        } catch (err) {
            console.error("Error al obtener detalles del documento", err);
        }
    };

    if (loading) return <p>Cargando documentos...</p>;
    if (error) return <p className="text-red-500">{error}</p>;
    if (documents.length === 0) return <p>No hay documentos disponibles.</p>;

    return (
        <div className="p-6 bg-white shadow-lg rounded-xl w-full max-w-md">
            <h2 className="text-xl font-bold mb-4">Documentos Subidos</h2>
            <ul className="space-y-4">
                {documents.map((doc) => (
                    <li key={doc.id} className="border p-4 rounded-lg shadow-sm">
                        <h3 className="text-lg font-semibold">{doc.title}</h3>
                        <p className="text-sm text-gray-500">
                            Subido el: {new Date(doc.uploaded_at).toLocaleDateString()}
                        </p>
                        <a
                            href={doc.file}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="text-blue-500 underline"
                        >
                            📄 Descargar Documento
                        </a>
                        <Button onClick={() => toggleDetails(doc.id)} className="mt-2 w-full">
                            {selectedDocument === doc.id ? "Ocultar Detalles" : "Ver Detalles"}
                        </Button>
                        {selectedDocument === doc.id && (
                            <div className="mt-3 p-3 border rounded-lg bg-gray-100">
                                <p><strong>Firma válida:</strong> {doc.signature_valid ? "✅ Sí" : "❌ No"}</p>
                                <p><strong>Fecha de subida:</strong> {new Date(doc.uploaded_at).toLocaleDateString()}</p>

                                {doc.qr_code_url && (
                                    <div className="mt-2">
                                        <p><strong>Código QR:</strong></p>
                                        <img src={doc.qr_code_url} alt="QR Code" className="w-24 h-24" />
                                    </div>
                                )}
                            </div>
                        )}
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default DocumentList;
