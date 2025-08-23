import { FolderPlusIcon, DocumentPlusIcon } from '@heroicons/react/24/outline';

export default function FolderList({ folders, selectedFolder, setSelectedFolder, setIsFolderModalOpen, setIsDocumentModalOpen }) {
  return (
    <div className="lg:col-span-1">
      <div className="flex space-x-4">
        <button
          onClick={() => setIsFolderModalOpen(true)}
          className="inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 cursor-pointer"
        >
          <FolderPlusIcon className="-ml-1 mr-2 h-5 w-5" />
          Buat Folder
        </button>
        <button
          onClick={() => setIsDocumentModalOpen(true)}
          className="inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 cursor-pointer"
        >
          <DocumentPlusIcon className="-ml-1 mr-2 h-5 w-5" />
          Tambah Dokumen
        </button>
      </div>
      <div className="bg-white shadow-lg rounded-lg p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Folders</h3>
        <ul className="space-y-2">
          <li>
            <button
              onClick={() => setSelectedFolder('All')}
              className={`w-full text-left px-4 py-2 rounded-lg text-sm font-medium transition-colors duration-200 ${selectedFolder === 'All' ? 'bg-indigo-100 text-indigo-700' : 'text-gray-700 hover:bg-indigo-50 cursor-pointer'
                }`}
            >
              Semua Dokumen
            </button>
          </li>
          {folders.map((folder) => (
            <li key={folder.name}>
              <button
                onClick={() => setSelectedFolder(folder.name)}
                className={`w-full text-left px-4 py-2 rounded-lg text-sm font-medium flex justify-between items-center transition-colors duration-200 ${selectedFolder === folder.name ? 'bg-indigo-100 text-indigo-700' : 'text-gray-700 hover:bg-indigo-50 cursor-pointer'
                  }`}
              >
                <span>{folder.name}</span>
                <span className="bg-indigo-200 text-indigo-800 text-xs font-semibold px-2 py-1 rounded-full">
                  {folder.document_count}
                </span>
              </button>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}