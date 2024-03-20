import axios from 'axios';
import router from './router'; // Import your router

const instance = axios.create({
  baseURL: 'http://localhost:8000/',
});

// Immediately try to set the auth token if it exists in localStorage
const token = localStorage.getItem('token');
if (token) {
  instance.defaults.headers.common['Authorization'] = `Bearer ${token}`;
}

// Response interceptor
instance.interceptors.response.use(
  response => response,
  error => {
    if (error.response && error.response.status === 401) {
      // If 401 received, redirect to login page
      router.push('/');
    }
    return Promise.reject(error);
  }
);

export function setAuthToken(token) {
  if (token) {
    localStorage.setItem('token', token); // Store the new token
    instance.defaults.headers.common['Authorization'] = `Bearer ${token}`;
  } else {
    localStorage.removeItem('token'); // Clear the token if logging out or it's invalid
    delete instance.defaults.headers.common['Authorization'];
  }
}

export default instance;
