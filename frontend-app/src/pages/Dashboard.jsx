import { useState, useEffect } from 'react';
import Layout from '../components/layout/Layout';
import { DocumentPlusIcon, XMarkIcon } from '@heroicons/react/24/outline';
import { fetchCompanies, createCompany } from '../services/dashboard';
import { Link } from 'react-router-dom';


export default function Dashboard() {
    const [isModalOpen, setIsModalOpen] = useState(false)
    const [companyName, setCompanyName] = useState('')
    const [showSuccess, setShowSuccess] = useState(false)
    const [companies, setCompanies] = useState([])
    const [loading, setLoading] = useState(false)

    useEffect(() => {
        const fetchData = async () => {
            try {
                const data = await fetchCompanies()
                setCompanies(data)
            } catch (error) {
                console.error('Error fetching companies:', error)
            } finally {
                setLoading(false)
            }
        }
        fetchData()
    }, [])


    const handleSave = async () => {
        if (companyName.trim() === '') return
        try {
             const newCompany = await createCompany(companyName);
             setCompanies((prevCompanies) => [...prevCompanies, newCompany])
             setIsModalOpen(false)
             setShowSuccess(true)
             setCompanyName('')
             setTimeout(() => setShowSuccess(false), 3000)
        } catch (error) {
            console.error('Error creating company:', error)
        }
    }

    if (loading) {
        return (
            <Layout title="Company">
                <div className="text-center py-10">Loading companies...</div>
            </Layout>
        );
    }


    return (
        <Layout title="Company">
            {/* Success Notification */}
            {showSuccess && (
                <div className="bg-green-100 border border-green-400 text-green-700 px-4 py-2 rounded text-sm relative">
                    Company berhasil dibuat.
                </div>
            )}

            {/* Add Company Button */}
            <div className="flex justify-end mb-4">
                <button
                    onClick={() => setIsModalOpen(true)}
                    className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 cursor-pointer"
                >
                    <DocumentPlusIcon className="-ml-1 mr-2 h-5 w-5" />
                    Tambah Company
                </button>
            </div>

            {/* Modal */}
            {isModalOpen && (
                <div className="fixed inset-0 z-50 flex items-center justify-center">
                    <div className="absolute inset-0 backdrop-blur-sm bg-white/30 transition-all duration-200"></div>
                    <div className="bg-white rounded-lg shadow-xl w-full max-w-md p-6 relative z-10">
                        <button onClick={() => setIsModalOpen(false)} className="absolute top-2 right-2 text-gray-400 hover:text-gray-600 cursor-pointer">
                            <XMarkIcon className="h-5 w-5" />
                        </button>
                        <h2 className="text-xl font-semibold text-gray-800 mb-4">Tambah Company</h2>
                        <label className="block mb-2 text-sm font-medium text-gray-700">Nama Company</label>
                        <input
                            type="text"
                            value={companyName}
                            onChange={(e) => setCompanyName(e.target.value)}
                            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring focus:ring-indigo-200"
                            placeholder="Masukkan nama company"
                        />
                        <div className="mt-4 flex justify-end">
                            <button
                                onClick={handleSave}
                                className="px-4 py-2 bg-indigo-600 text-white text-sm font-medium rounded-md hover:bg-indigo-700 cursor-pointer"
                            >
                                Save
                            </button>
                        </div>
                    </div>
                </div>
            )}

            {/* Company Cards */}
            <div className="space-y-6">
                {companies.map((company) => (
                    <Link to={`/dashboard/${company.slug}`} key={company.id} className="block hover:bg-gray-50">
                    <div key={company.id} className="bg-white p-6 flex items-start border border-gray-200 rounded-lg">
                        <div className="w-36 h-36 bg-gradient-to-b from-green-300 to-yellow-400 rounded-sm"></div>
                        <div className="ml-6 mt-2">
                            <h1 className="text-3xl font-bold text-gray-900">
                                {company.name}
                            </h1>
                            <p className="text-sm text-gray-600 mt-1">
                                Mulai buat chatbot untuk perusahaan Anda
                            </p>
                        </div>
                    </div>
                    </Link>
                ))}
            </div>

        </Layout>
    )
}