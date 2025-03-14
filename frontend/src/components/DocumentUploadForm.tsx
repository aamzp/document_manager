import React, { useState } from 'react';
import axios from 'axios';
import { Button } from "../components/ui/button";
import { Input } from "../components/ui/input";

const DocumentUploadForm = () => {
    const [title, setTitle] = useState('');
    const [file, setFile] = useState<File | null>(null);

    const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();

        if (!file || !title) {
            alert('Por favor completa todos los campos.');
            return;
        }

        const formData = new FormData();
        formData.append('title', title);
        formData.append('file', file);

        try {
            const token = localStorage.getItem('token');
            await axios.post(
                'http://127.0.0.1:8000/api/documents/upload/',  // confirma la URL correcta
                formData,
                {
                    headers: {
                        'Content-Type': 'multipart/form-data',
                        'Authorization': `Bearer ${token}`,
                    },
                }
            );

            alert('Documento subido correctamente.');
            setTitle('');
            setFile(null);
        } catch (error) {
            console.error('Error al subir el documento:', error);
            alert('Ocurrió un error al subir el documento.');
        }
    };

    return (
        <div className="p-6 bg-gray-50 rounded-2xl shadow">
            <h2 className="text-xl font-semibold mb-4">Subir nuevo documento</h2>
            <form onSubmit={handleSubmit} className="space-y-4">
                <Input
                    type="text"
                    placeholder="Título del documento"
                    value={title}
                    onChange={(e) => setTitle(e.target.value)}
                    required
                />
                <Input
                    type="file"
                    onChange={(e) => setFile(e.target.files ? e.target.files[0] : null)}
                    required
                />
                <Button type="submit">
                    Subir Documento
                </Button>
            </form>
        </div>
    );
};

export default DocumentUploadForm;
