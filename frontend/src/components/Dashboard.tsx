import React, { useEffect, useState } from "react";
import axios from "axios";
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";

interface Document {
  id: number;
  uploaded_at: string;
  signature_valid: boolean;
}

const Dashboard = () => {
  const [documents, setDocuments] = useState<Document[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [weeklyData, setWeeklyData] = useState<{ day: string; count: number }[]>([]);
  const [validDocs, setValidDocs] = useState(0);
  const [invalidDocs, setInvalidDocs] = useState(0);

  useEffect(() => {
    const fetchDocuments = async () => {
      try {
        const token = localStorage.getItem("token");
        const response = await axios.get("http://127.0.0.1:8000/api/documents/", {
          headers: { Authorization: `Bearer ${token}` },
        });

        const docs = response.data;
        setDocuments(docs);

        // Procesar datos para el gráfico de la semana
        const counts: { [key: string]: number } = {};
        const validCount = docs.filter((doc: Document) => doc.signature_valid).length;
        const invalidCount = docs.length - validCount;

        setValidDocs(validCount);
        setInvalidDocs(invalidCount);

        // Obtener fechas de la última semana
        const days = ["Dom", "Lun", "Mar", "Mié", "Jue", "Vie", "Sáb"];
        const today = new Date();
        for (let i = 6; i >= 0; i--) {
          const date = new Date();
          date.setDate(today.getDate() - i);
          const dayKey = days[date.getDay()];
          counts[dayKey] = 0;
        }

        docs.forEach((doc: Document) => {
          const date = new Date(doc.uploaded_at);
          const dayKey = days[date.getDay()];
          if (counts[dayKey] !== undefined) {
            counts[dayKey]++;
          }
        });

        setWeeklyData(Object.keys(counts).map(day => ({ day, count: counts[day] })));
      } catch (err) {
        setError("Error al cargar datos.");
      } finally {
        setLoading(false);
      }
    };

    fetchDocuments();
  }, []);

  if (loading) return <p>Cargando datos...</p>;
  if (error) return <p className="text-red-500">{error}</p>;

  return (
    <div className="p-6 bg-white shadow-lg rounded-xl w-full max-w-lg">
      <h2 className="text-xl font-bold mb-4">Resumen de Documentos</h2>
      
      {/* Contadores de documentos válidos e inválidos */}
      <div className="flex justify-between mb-6">
        <div className="p-4 bg-green-100 rounded-lg text-center">
          <p className="text-lg font-semibold">{validDocs}</p>
          <p className="text-sm text-green-700">Documentos Válidos</p>
        </div>
        <div className="p-4 bg-red-100 rounded-lg text-center">
          <p className="text-lg font-semibold">{invalidDocs}</p>
          <p className="text-sm text-red-700">Documentos Inválidos</p>
        </div>
      </div>

      {/* Gráfico de documentos subidos en la semana */}
      <h3 className="text-md font-semibold mb-2">Documentos subidos en la última semana</h3>
      <ResponsiveContainer width="100%" height={250}>
        <BarChart data={weeklyData}>
          <XAxis dataKey="day" />
          <YAxis />
          <Tooltip />
          <Bar dataKey="count" fill="#4F46E5" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};

export default Dashboard;
