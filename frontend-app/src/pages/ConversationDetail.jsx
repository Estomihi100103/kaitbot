import { useState, useEffect } from 'react'
import { useParams } from 'react-router-dom'
import Layout from '../components/layout/Layout'
import {
    ChatBubbleLeftRightIcon,
    UserIcon,
    ClockIcon
} from '@heroicons/react/24/outline'
import { fetchConversationsByCompany, fetchConversationDetail } from '../services/conversation'
import { formatDistanceToNow } from 'date-fns';
import { id } from 'date-fns/locale';

export default function Conversation() {
    const [conversations, setConversations] = useState([])
    const [selectedConversation, setSelectedConversation] = useState(null)
    const [isLoading, setIsLoading] = useState(true)
    const [error, setError] = useState(null)
    const { companySlug } = useParams()

    useEffect(() => {
        const getConversations = async () => {
            try {
                const data = await fetchConversationsByCompany(companySlug);
                setConversations(data);
            } catch (err) {
                setError(err.message);
            } finally {
                setIsLoading(false);
            }
        };
        getConversations();
    }, [companySlug]);

    const handleConversationClick = async (conversation) => {
        setSelectedConversation(conversation);
        try {
            const detailData = await fetchConversationDetail(conversation.thread_id);
            setSelectedConversation(detailData);
        } catch (err) {
            console.error("Gagal mengambil detail:", err);
            setSelectedConversation(conversation);
        }
    };

    if (isLoading) return <Layout title="Memuat..."><p>Loading...</p></Layout>
    if (error) return <Layout title="Error"><p>Error: {error}</p></Layout>

    return (
        <Layout title="Riwayat Percakapan">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                {/* Conversations List */}
                <div className="md:col-span-1">
                    <div className="bg-white shadow overflow-hidden sm:rounded-md h-[70vh] flex flex-col">
                        <div className="p-4 border-b border-gray-200 font-semibold">Daftar Sesi</div>
                        <div className="flex-1 overflow-y-auto">
                            {conversations.length > 0 ? (
                                conversations.map((conv) => (
                                    <div
                                        key={conv.id}
                                        className={`p-4 border-b border-gray-200 hover:bg-gray-50 cursor-pointer transition-colors ${selectedConversation?.id === conv.id ? 'bg-indigo-50 border-l-4 border-l-indigo-500' : ''
                                            }`}
                                        onClick={() => handleConversationClick(conv)}
                                    >
                                        <h3 className="text-sm font-medium text-gray-900 truncate">
                                            {conv.first_user_message}
                                        </h3>
                                        <p className="text-xs text-gray-500 mt-1 truncate">
                                            {conv.last_message_preview}
                                        </p>
                                        <div className="flex items-center text-xs text-gray-400 mt-2">
                                            <ClockIcon className="h-3 w-3 mr-1" />
                                            <span>{formatDistanceToNow(new Date(conv.created_at), { addSuffix: true, locale: id })}</span>
                                        </div>
                                    </div>
                                ))
                            ) : (
                                <div className="text-center py-12 px-4">
                                    <ChatBubbleLeftRightIcon className="mx-auto h-12 w-12 text-gray-400" />
                                    <h3 className="mt-2 text-sm font-medium text-gray-900">Belum ada percakapan</h3>
                                </div>
                            )}
                        </div>
                    </div>
                </div>

                {/* Conversation Detail/Preview */}
                <div className="md:col-span-2">
                    <div className="bg-white shadow rounded-lg sticky top-24">
                        <ConversationDetail conversation={selectedConversation} />
                    </div>
                </div>
            </div>
        </Layout>
    )
}

const ConversationDetail = ({ conversation }) => {
    if (!conversation) {
        return (
            <div className="text-center">
                <ChatBubbleLeftRightIcon className="mx-auto h-12 w-12 text-gray-400" />
                <h3 className="mt-2 text-sm font-medium text-gray-900">Pilih Percakapan</h3>
                <p className="mt-1 text-sm text-gray-500">
                    Klik pada salah satu percakapan untuk melihat detailnya.
                </p>
            </div>
        );
    }

    return (
        <div className="flex flex-col h-[70vh]">
            <div className="p-4 border-b border-gray-200 bg-white flex items-center gap-4">
                <h3 className="text-lg font-medium text-gray-900 truncate" title={conversation.thread_id}>
                    Percakapan #{conversation.id}
                </h3>
                <p className="text-sm text-gray-500 mt-1">
                    {conversation.message_count || conversation.messages?.length || 0} pesan
                </p>
            </div>
            <div className="flex-1 space-y-4 p-4 overflow-y-auto bg-gray-50">
                {conversation.messages?.map(message => (
                    <div key={message.id} className={`flex items-start gap-3 ${message.sender === 'user' ? 'justify-end' : ''}`}>
                        {message.sender === 'bot' && <div className="h-8 w-8 bg-gray-200 rounded-full flex items-center justify-center text-lg">🤖</div>}
                        <div className={`max-w-[70%] p-3 rounded-lg ${message.sender === 'user' ? 'bg-indigo-500 text-white' : 'bg-white shadow-sm'
                            }`}>
                            <p className="text-sm">{message.content}</p>
                        </div>
                        {message.sender === 'user' && <div className="h-8 w-8 bg-indigo-200 rounded-full flex items-center justify-center text-lg">👤</div>}
                    </div>
                ))}
            </div>
        </div>
    );
};


