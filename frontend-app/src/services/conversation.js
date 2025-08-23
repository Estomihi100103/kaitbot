import apiClient from './api'; 

export const fetchConversationsByCompany = async (companySlug) => {
  const response = await apiClient.get(`/conversations/by-company/${companySlug}`);
  return response.data;
};

export const fetchConversationDetail = async (threadId) => {
  const response = await apiClient.get(`/conversations/${threadId}`);
  return response.data;
};