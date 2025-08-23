import apiClient from './api';

// Token parameter dihilangkan
export const fetchCompanyBySlug = async (slug) => {
  const response = await apiClient.get(`/companies/${slug}`);
  return response.data;
}