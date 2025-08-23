import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import Layout from '../components/layout/Layout';
import { fetchCompanies } from '../services/dashboard';
import { ChatBubbleLeftRightIcon } from '@heroicons/react/24/outline';

export default function ConversationList() {
    const [companies, setCompanies] = useState([]);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const data = await fetchCompanies();
                setCompanies(data);
            } catch (error) {
                console.error('Error fetching companies:', error);
                setError(error.message);
            } finally {
                setIsLoading(false);
            }
        };
        fetchData();
    }, []);

    if (isLoading) {
        return (
            <Layout title="Conversation">
                <div className="text-center py-10">Loading companies...</div>
            </Layout>
        );
    }
    
    if (error) return <Layout title="Error"><p>Error: {error}</p></Layout>

    return (
        <Layout title="Conversations By Company">
            <div className="space-y-6">
                {companies.length > 0 ? companies.map((company) => (
                    <Link to={`/conversations/${company.slug}`} key={company.id} className="block hover:bg-gray-50">
                        <div className="bg-white p-6 flex items-start border border-gray-200 rounded-lg">
                            <div className="w-36 h-36 bg-gradient-to-b from-green-300 to-yellow-400 rounded-sm"></div>
                            <div className="ml-6 mt-2">
                                <h3 className="text-2xl font-bold text-gray-900">
                                    {company.name}
                                </h3>
                                <p className="text-sm text-gray-500 mt-1">
                                    Lihat semua sesi percakapan untuk company ini.
                                </p>
                            </div>
                        </div>
                    </Link>
                )) : (
                    <p>Anda belum memiliki company. Silakan buat company terlebih dahulu.</p>
                )}
            </div>
        </Layout>
    );
}