import { DocumentIcon, MagnifyingGlassIcon } from '@heroicons/react/24/solid';

export default function DocumentList({ searchQuery, setSearchQuery, filteredDocuments }) {
  const getFileIcon = () => {
    return <DocumentIcon className="h-5 w-5 text-gray-400" />;
  };

  return (
    <div className="lg:col-span-2">
      <div className="mb-6">
        <div className="relative">
          <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            <MagnifyingGlassIcon className="h-5 w-5 text-gray-400" />
          </div>
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md leading-5 bg-white placeholder-gray-500 focus:outline-none focus:placeholder-gray-400 focus:ring-1 focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
            placeholder="Cari dokumen..."
          />
        </div>
      </div>
      <div className="bg-white shadow overflow-hidden sm:rounded-md">
        <ul
          className="divide-y divide-gray-200 overflow-y-auto max-h-96"
          style={{ scrollbarWidth: 'none', msOverflowStyle: 'none' }}
        >
          {filteredDocuments.map((doc) => (
            <li key={doc.id}>
              <div className="px-4 py-4 flex items-center justify-between hover:bg-gray-50">
                <div className="flex items-center min-w-0 flex-1">
                  <div className="flex-shrink-0">{getFileIcon()}</div>
                  <div className="ml-4 min-w-0 flex-1">
                    <p className="font-medium text-gray-900 truncate">{doc.title}</p>
                  </div>
                </div>
              </div>
            </li>
          ))}
        </ul>
        {filteredDocuments.length === 0 && (
          <div className="text-center py-12">
            <DocumentIcon className="mx-auto h-12 w-12 text-gray-400" />
            <h3 className="mt-2 text-sm font-medium text-gray-900">Tidak ada dokumen</h3>
            <p className="mt-1 text-sm text-gray-500">
              {searchQuery ? 'Tidak ada dokumen yang sesuai dengan pencarian.' : 'Mulai dengan menambahkan dokumen baru.'}
            </p>
          </div>
        )}
      </div>
    </div>
  );
}