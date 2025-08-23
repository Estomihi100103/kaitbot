import apiClient from './api';

// Token parameter dihilangkan
export const createCompany = async (companyName) => {
  const response = await apiClient.post('/companies/', { name: companyName });
  return response.data;
};

// Token parameter dihilangkan
export const fetchCompanies = async () => {
  const response = await apiClient.get('/companies/');
  return response.data;
};