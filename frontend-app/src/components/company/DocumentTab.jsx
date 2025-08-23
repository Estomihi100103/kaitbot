import { useState, useMemo } from 'react';
import FolderModal from './FolderModal';
import DocumentModal from './DocumentModal';
import FolderList from './FolderList';
import DocumentList from './DocumentList';
import Notification from '../common/Notification';

export default function DocumentTab({ companySlug, folders, setFolders }) {
  const [isFolderModalOpen, setIsFolderModalOpen] = useState(false);
  const [isDocumentModalOpen, setIsDocumentModalOpen] = useState(false);
  const [showFolderSuccess, setShowFolderSuccess] = useState(false);
  const [showDocSuccess, setShowDocSuccess] = useState(false);
  const [selectedFolder, setSelectedFolder] = useState('All');
  const [searchQuery, setSearchQuery] = useState('');

  const filteredDocuments = useMemo(() => {
    let docs = [];
    if (selectedFolder === 'All') {
      docs = folders.flatMap(f => f.documents.map(d => ({ ...d, folder: f.name })));
    } else {
      const folder = folders.find(f => f.name === selectedFolder);
      docs = folder ? folder.documents.map(d => ({ ...d, folder: folder.name })) : [];
    }
    return docs.filter(doc => doc.title.toLowerCase().includes(searchQuery.toLowerCase()));
  }, [folders, selectedFolder, searchQuery]);

  return (
    <div className="space-y-6">
      {showFolderSuccess && (
        <Notification message="Folder berhasil dibuat." type="success" onClose={() => setShowFolderSuccess(false)} />
      )}
      {showDocSuccess && (
        <Notification message="Dokumen berhasil ditambahkan." type="success" onClose={() => setShowDocSuccess(false)} />
      )}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <FolderList
          folders={folders}
          selectedFolder={selectedFolder}
          setSelectedFolder={setSelectedFolder}
          setIsFolderModalOpen={setIsFolderModalOpen}
          setIsDocumentModalOpen={setIsDocumentModalOpen}
        />
        <DocumentList
          searchQuery={searchQuery}
          setSearchQuery={setSearchQuery}
          filteredDocuments={filteredDocuments}
        />
      </div>
      <FolderModal
        isOpen={isFolderModalOpen}
        onClose={() => setIsFolderModalOpen(false)}
        companySlug={companySlug}
        setFolders={setFolders}
        folders={folders}
        setShowSuccess={setShowFolderSuccess}
      />
      <DocumentModal
        isOpen={isDocumentModalOpen}
        onClose={() => setIsDocumentModalOpen(false)}
        companySlug={companySlug}
        folders={folders}
        setFolders={setFolders}
        setShowSuccess={setShowDocSuccess}
      />
    </div>
  );
}