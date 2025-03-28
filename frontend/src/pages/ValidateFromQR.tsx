import { useNavigate } from "react-router-dom";
import QRScanner from "../components/QRScanner";

const ValidateFromQR = () => {
  const navigate = useNavigate();

  const handleScan = (result: string) => {
    try {
      const url = new URL(result);
      const pathSegments = url.pathname.split("/");
      const documentId = pathSegments[pathSegments.length - 1];

      // Redirigir a la vista de validación
      navigate(`/validate/${documentId}`);
    } catch (err) {
      alert("El código QR no contiene una URL válida.");
    }
  };

  return (
    <div className="p-4">
      <h1 className="text-xl font-bold mb-4">Escanea un documento</h1>
      <QRScanner onScan={handleScan} />
    </div>
  );
};

export default ValidateFromQR;
