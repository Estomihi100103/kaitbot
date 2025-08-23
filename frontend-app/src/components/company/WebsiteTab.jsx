import { useState, useEffect } from 'react';
import { LinkIcon, MagnifyingGlassIcon, XMarkIcon, TrashIcon } from '@heroicons/react/24/solid';
import { useParams } from 'react-router-dom';
import { createUrls, getUrls, deleteUrl } from '../../services/url_company';

export default function WebsiteTab() {
  const { companySlug } = useParams(); 
  const [websiteURL, setWebsiteURL] = useState('');
  const [searchQuery, setSearchQuery] = useState('');
  const [urls, setUrls] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const filteredUrls = urls.filter(url =>
    url.url.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const loadUrls = async () => {
    try {
      setLoading(true);
      const data = await getUrls(companySlug);
      setUrls(data);
      setError(null);
    } catch (error) {
      console.error('Failed to load URLs:', error);
      setError('Failed to load URLs');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (companySlug) {
      loadUrls();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [companySlug]);

  const handleAddUrl = () => {
    if (websiteURL.trim() === '') return;

    const exists = urls.some(url => url.url === websiteURL.trim());
    if (exists) {
      setError('URL already exists');
      return;
    }

    handleSaveUrls([websiteURL.trim()]);
  };

  const handleSaveUrls = async (urlsToSave) => {
    try {
      setLoading(true);
      setError(null);
      await createUrls(companySlug, urlsToSave);
      await loadUrls();
      setWebsiteURL('');
    } catch (error) {
      console.error('Failed to save URLs:', error);
      setError(error.message || 'Failed to save URLs');
    } finally {
      setLoading(false);
    }
  };


  const handleRemoveUrl = async (urlId) => {
    try {
      setLoading(true);
      await deleteUrl(companySlug, urlId);
      await loadUrls(); 
    } catch (error) {
      console.error('Failed to delete URL:', error);
      setError(error.message || 'Failed to delete URL');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      {error && (
        <div className="bg-red-50 border border-red-200 rounded-md p-4">
          <p className="text-sm text-red-600">{error}</p>
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-1">
          <div className="bg-white shadow-lg rounded-lg px-4 pb-4 pt-4">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Website Settings</h3>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-semibold text-gray-700">Website URL</label>
                <input
                  type="text"
                  value={websiteURL}
                  onChange={(e) => setWebsiteURL(e.target.value)}
                  className="mt-1 block w-full border border-gray-200 rounded-lg bg-gray-50 px-4 py-3 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition duration-200"
                  placeholder="example.com"
                  disabled={loading}
                />
              </div>

              <button
                onClick={handleAddUrl}
                disabled={loading || !websiteURL.trim()}
                className="w-full bg-indigo-600 text-white px-4 py-2 rounded-lg font-semibold hover:bg-indigo-700 transition duration-200 disabled:opacity-50 disabled:cursor-not-allowed cursor-pointer"
              >
                {loading ? 'Menyimpan...' : 'Simpan URL Website'}
              </button>
            </div>
          </div>
        </div>

        {/* URL List with Search */}
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
                placeholder="Cari URL..."
                disabled={loading}
              />
            </div>
          </div>

          <div className="bg-white shadow-lg rounded-lg overflow-hidden">
            {loading && (
              <div className="text-center py-8">
                <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600"></div>
                <p className="mt-2 text-sm text-gray-500">Loading...</p>
              </div>
            )}

            {!loading && (
              <ul className="divide-y divide-gray-100 max-h-96 overflow-y-auto scrollbar-thin scrollbar-thumb-gray-300 scrollbar-track-gray-100">
                {filteredUrls.map((urlItem) => (
                  <li key={urlItem.id}>
                    <div className="px-4 py-4 flex items-center justify-between hover:bg-indigo-50 transition duration-150">
                      <div className="flex items-center min-w-0 flex-1">
                        <div className="flex-shrink-0">
                          <LinkIcon className="h-6 w-6 text-indigo-500" />
                        </div>
                        <div className="ml-4 min-w-0 flex-1">
                          <p className="font-medium text-gray-800 truncate">{urlItem.url}</p>
                          <p className="text-xs text-gray-500">
                            {new Date(urlItem.created_at).toLocaleDateString('id-ID')}
                          </p>
                        </div>
                      </div>
                      <button
                        onClick={() => handleRemoveUrl(urlItem.id)}
                        className="ml-2 text-gray-400 hover:text-red-500 transition-colors duration-200 cursor-pointer"
                        disabled={loading}
                      >
                        <TrashIcon className="h-5 w-5" />
                      </button>
                    </div>
                  </li>
                ))}
              </ul>
            )}

            {!loading && filteredUrls.length === 0 && (
              <div className="text-center py-12">
                <LinkIcon className="mx-auto h-12 w-12 text-gray-300" />
                <h3 className="mt-2 text-sm font-semibold text-gray-800">Tidak ada URL</h3>
                <p className="mt-1 text-sm text-gray-500">
                  {searchQuery
                    ? 'Tidak ada URL yang sesuai dengan pencarian.'
                    : 'Mulai dengan menambahkan URL website baru.'}
                </p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}