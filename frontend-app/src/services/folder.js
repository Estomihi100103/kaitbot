import apiClient from './api';

// Token parameter dihilangkan
export const getFoldersForCompany = async (slug) => {
  const response = await apiClient.get(`/companies/${slug}/folders`);
  return response.data;
};

// Token parameter dihilangkan
export const createFolder = async (slug, folderName) => {
  const response = await apiClient.post(`/companies/${slug}/folders`, { name: folderName });
  return response.data;
};