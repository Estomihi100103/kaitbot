import apiClient from './api'; // Import instance Axios kita

export const registerUser = async (userData) => {
  // Axios otomatis menangani JSON.stringify
  const response = await apiClient.post('/auth/register', userData);
  return response.data; // Data respons ada di `response.data`
};

export const loginUser = async ({ email, password }) => {
  const formBody = new URLSearchParams();
  formBody.append('username', email);
  formBody.append('password', password);

  // Untuk form-urlencoded, kita tetap perlu membuat formBody
  const response = await apiClient.post('/auth/token', formBody, {
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
  });
  return response.data;
};

// Lihat betapa bersihnya ini! Tidak perlu parameter token lagi.
export const fetchCurrentUser = async () => {
  const response = await apiClient.get('/auth/me');
  return response.data;
};