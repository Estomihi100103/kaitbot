import axios from 'axios';

// Membuat instance Axios dengan konfigurasi default
const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1',
});

// Interceptor untuk menambahkan token otentikasi ke setiap request
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      // Menambahkan header Authorization jika token ada
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    // Menangani error pada request
    return Promise.reject(error);
  }
);

export default apiClient;