import { useState } from 'react';
import { XMarkIcon } from '@heroicons/react/24/outline';
import { createFolder } from '../../services/folder';

export default function FolderModal({ isOpen, onClose, companySlug, setFolders, folders, setShowSuccess }) {
  const [newFolderName, setNewFolderName] = useState('');

  const handleAddFolder = async () => {
    if (!newFolderName.trim()) return;

    try {
      const newFolder = await createFolder(companySlug, newFolderName);
      setFolders([...folders, { ...newFolder, document_count: 0, documents: [] }]);
      setNewFolderName('');
      onClose();
      setShowSuccess(true);
      setTimeout(() => setShowSuccess(false), 3000);
    } catch (err) {
      console.error(err);
      alert(err.message || 'Gagal membuat folder');
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center">
      <div className="absolute inset-0 backdrop-blur-sm bg-white/30 transition-all duration-200"></div>
      <div className="bg-white rounded-lg shadow-xl w-full max-w-md p-6 relative z-10">
        <button onClick={onClose} className="absolute top-2 right-2 text-gray-400 hover:text-gray-600 cursor-pointer">
          <XMarkIcon className="h-5 w-5" />
        </button>
        <h2 className="text-xl font-semibold text-gray-800 mb-4">Buat Folder Baru</h2>
        <label className="block mb-2 text-sm font-medium text-gray-700">Nama Folder</label>
        <input
          type="text"
          value={newFolderName}
          onChange={(e) => setNewFolderName(e.target.value)}
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring focus:ring-indigo-200"
          placeholder="Masukkan nama folder"
        />
        <div className="mt-4 flex justify-end space-x-2">
          <button
            onClick={onClose}
            className="px-4 py-2 bg-gray-300 text-gray-700 text-sm font-medium rounded-md hover:bg-gray-400 cursor-pointer"
          >
            Batal
          </button>
          <button
            onClick={handleAddFolder}
            className="px-4 py-2 bg-indigo-600 text-white text-sm font-medium rounded-md hover:bg-indigo-700 cursor-pointer"
          >
            Simpan
          </button>
        </div>
      </div>
    </div>
  );
}