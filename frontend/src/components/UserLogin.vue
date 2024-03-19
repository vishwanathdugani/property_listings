<template>
  <div class="login-container">
    <div class="login-form">
      <h1>Login</h1>
      <input v-model="credentials.username" type="text" placeholder="Username" />
      <input v-model="credentials.password" type="password" placeholder="Password" />
      <button @click="login">Login</button>
      <span v-if="errorMessage" class="error-message">{{ errorMessage }}</span>   
    </div>
  </div>
</template>

<script>
import { setAuthToken } from '@/http'; // Import setAuthToken

export default {
  data() {
    return {
      credentials: {
        username: '',
        password: '',
      },
      errorMessage: '',
    };
  },
  methods: {
    async login() {
  const token = btoa(`${this.credentials.username}:${this.credentials.password}`);
  try {
    const response = await fetch('http://localhost:8000/token', {
      method: 'POST',
      headers: {
        'Authorization': `Basic ${token}`,
      },
    });
    if (response.ok) {
      const data = await response.json();
      console.log('Login successful', data);
      setAuthToken(data.access_token); // Use setAuthToken
      localStorage.setItem('token', data.access_token); // Optionally store the token for page reloads
      this.$router.push('/home');
    } else {
      this.errorMessage = 'Login failed. Please check your credentials.';
      console.error('Login failed');
    }
  } catch (error) {
    this.errorMessage = 'An error occurred. Please try again.';
    console.error('Login error', error);
  }
},


    logout() {
    localStorage.removeItem('token'); // Assuming the token is stored in localStorage
    this.$router.push('/login'); // Redirect to login page
  }
  },
};
</script>


<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh; /* Full viewport height */
  background-color: #f0f2f5; /* Light grey background */
}

.login-form {
  padding: 40px;
  background: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  gap: 20px; /* Space between form elements */
  max-width: 400px;
  width: 100%;
}

input {
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  font-size: 16px;
}

button {
  padding: 10px 20px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
  font-weight: bold;
}

button:hover {
  background-color: #0056b3;
}

.error-message {
  color: red;
  margin-top: 10px;
  font-size: 14px;
}

</style>
