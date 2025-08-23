import apiClient from './api';

// Semua parameter token dihilangkan
export async function createUrls(companySlug, urls) {
  const response = await apiClient.post(`/companies/${companySlug}/urls`, { urls });
  return response.data;
}

export async function getUrls(companySlug) {
  const response = await apiClient.get(`/companies/${companySlug}/urls`);
  return response.data;
}

export async function deleteUrl(companySlug, urlId) {
  const response = await apiClient.delete(`/companies/${companySlug}/urls/${urlId}`);
  return response.data;
}