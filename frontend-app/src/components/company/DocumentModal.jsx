import { useState } from 'react';
import { XMarkIcon } from '@heroicons/react/24/outline';
import { useDropzone } from 'react-dropzone';
import { uploadDocument } from '../../services/document';
import LoadingSpinner from '../common/LoadingSpinner';

export default function DocumentModal({ isOpen, onClose, companySlug, folders, setFolders, setShowSuccess }) {
  const [selectedFile, setSelectedFile] = useState(null);
  const [selectedFolderForDoc, setSelectedFolderForDoc] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop: (acceptedFiles) => {
      if (acceptedFiles && acceptedFiles.length > 0) {
        setSelectedFile(acceptedFiles[0]);
      }
    },
    multiple: false,
  });

  const handleAddDocument = async () => {
    if (!selectedFile || !selectedFolderForDoc) return;

    setIsLoading(true);
    try {
      const title = selectedFile.name;
      const newDocFromAPI = await uploadDocument(companySlug, title, selectedFolderForDoc, selectedFile);

      const updatedFolders = folders.map(f =>
        f.id === parseInt(selectedFolderForDoc)
          ? { ...f, document_count: f.document_count + 1, documents: [...f.documents, newDocFromAPI] }
          : f
      );
      setFolders(updatedFolders);
      setSelectedFile(null);
      setSelectedFolderForDoc('');
      setShowSuccess(true);
      setTimeout(() => setShowSuccess(false), 3000);
      onClose();
    } catch (err) {
      console.error(err);
      alert('Gagal upload dokumen');
    } finally {
      setIsLoading(false);
    }
  };
  
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center">
      {isLoading && <LoadingSpinner />}
      <div className="absolute inset-0 backdrop-blur-sm bg-white/30 transition-all duration-200"></div>
      <div className="bg-white rounded-lg shadow-xl w-full max-w-md p-6 relative z-10">
        <button onClick={onClose} className="absolute top-2 right-2 text-gray-400 hover:text-gray-600 cursor-pointer">
          <XMarkIcon className="h-5 w-5" />
        </button>
        <h2 className="text-xl font-semibold text-gray-800 mb-4">Tambah Dokumen</h2>
        <label className="block mb-2 text-sm font-medium text-gray-700">Pilih File</label>
        <div
          {...getRootProps()}
          className={`w-full p-4 mb-4 border-2 border-dashed rounded-md cursor-pointer transition-colors ${isDragActive ? 'border-indigo-500 bg-indigo-50' : 'border-gray-300 bg-white'
            }`}
        >
          <input {...getInputProps()} />
          {selectedFile ? (
            <p className="text-sm text-gray-700">File terpilih: <strong>{selectedFile.name}</strong></p>
          ) : (
            <p className="text-sm text-gray-500 text-center">Seret dan lepas file di sini, atau klik untuk memilih file</p>
          )}
        </div>
        <label className="block mb-2 text-sm font-medium text-gray-700">Pilih Folder</label>
        <select
          value={selectedFolderForDoc}
          onChange={(e) => setSelectedFolderForDoc(e.target.value)}
          className="w-full px-3 py-2 border border-gray-300 rounded-md"
        >
          <option value="">-- Pilih Folder --</option>
          {folders.map((folder) => (
            <option key={folder.id} value={folder.id}>{folder.name}</option>
          ))}
        </select>
        <div className="mt-4 flex justify-end space-x-2">
          <button
            onClick={onClose}
            className="px-4 py-2 bg-gray-300 text-gray-700 text-sm font-medium rounded-md hover:bg-gray-400 cursor-pointer"
          >
            Batal
          </button>
          <button
            onClick={handleAddDocument}
            className="px-4 py-2 bg-indigo-600 text-white text-sm font-medium rounded-md hover:bg-indigo-700 disabled:bg-indigo-300 disabled:cursor-not-allowed cursor-pointer"
            disabled={isLoading}
          >
            {isLoading ? 'Mengunggah...' : 'Upload'}
          </button>
        </div>
      </div>
    </div>
  );
}