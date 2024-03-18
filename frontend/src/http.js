// http.js
import axios from 'axios';

const instance = axios.create({
  baseURL: 'http://localhost:8000/',
});

// Immediately try to set the auth token if it exists in localStorage
const token = localStorage.getItem('token');
if (token) {
  instance.defaults.headers.common['Authorization'] = `Bearer ${token}`;
}

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
