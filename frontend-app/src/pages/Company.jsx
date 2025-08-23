import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import Layout from '../components/layout/Layout';
import EmbedCode from '../components/company/EmbedCode';
import WebsiteTab from '../components/company/WebsiteTab';
import DocumentTab from '../components/company/DocumentTab';
import { fetchCompanyBySlug } from '../services/company';
import { getFoldersForCompany } from '../services/folder';

export default function Company() {
  const [activeTab, setActiveTab] = useState('website');
  const { companySlug } = useParams();
  const [companyData, setCompanyData] = useState(null);
  const [folders, setFolders] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      try {
        const [companyResult, foldersResult] = await Promise.all([
          fetchCompanyBySlug(companySlug),
          getFoldersForCompany(companySlug)
        ]);
        setCompanyData(companyResult);
        setFolders(foldersResult);
      } catch (err) {
        console.error("Failed to fetch company data:", err);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [companySlug]);

  if (loading) {
    return <Layout title="Loading..."><div>Loading company details...</div></Layout>;
  }

  return (
    <Layout title={companyData ? companyData.name : 'Loading...'}>
      <EmbedCode companySlug={companySlug} />
      <div className="mb-8 border-b border-gray-200">
        <nav className="-mb-px flex space-x-8">
          <button
            className={`px-3 py-2 font-medium text-sm cursor-pointer ${activeTab === 'website'
                ? 'border-b-2 border-blue-500 text-blue-600'
                : 'text-gray-500 hover:text-gray-700'
              }`}
            onClick={() => setActiveTab('website')}
          >
            Website
          </button>
          <button
            className={`px-3 py-2 font-medium text-sm cursor-pointer ${activeTab === 'document'
                ? 'border-b-2 border-blue-500 text-blue-600'
                : 'text-gray-500 hover:text-gray-700'
              }`}
            onClick={() => setActiveTab('document')}
          >
            Document
          </button>
        </nav>
      </div>
      {activeTab === 'website' && <WebsiteTab />}
      {activeTab === 'document' && (
        <DocumentTab
          companySlug={companySlug}
          folders={folders}
          setFolders={setFolders}
        />
      )}
    </Layout>
  );
}