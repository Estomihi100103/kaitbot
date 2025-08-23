import apiClient from './api';

// Token parameter dihilangkan
export async function uploadDocument(companySlug, title, folderId, file) {
  const formData = new FormData();
  formData.append('title', title);
  formData.append('company_slug', companySlug);
  if (folderId) formData.append('folder_id', folderId);
  formData.append('file', file);

  // Axios menangani FormData dengan baik. Header Content-Type (multipart/form-data)
  // akan ditambahkan otomatis oleh browser.
  const response = await apiClient.post('/documents/', formData);
  return response.data;
}