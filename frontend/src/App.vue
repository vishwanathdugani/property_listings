<template>
  <div id="app">
    <button @click="logout" v-if="$route.path !== '/'">Logout</button>
    <router-view></router-view>
  </div>
</template>


<script>
export default {
  name: 'App',
  methods: {
    logout() {
      localStorage.removeItem('token');
      this.$router.push('/');
    }
  }
}
</script>

<style>
#app {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

button {
  align-self: flex-end;
  margin: 20px;
  padding: 10px 20px;
  background-color: #ff4757;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-weight: bold;
  transition: background-color 0.3s ease;
}

button:hover {
  background-color: #ff6b81;
}

body {
  margin: 0;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background-color: #f4f4f4;
  color: #333;
}

</style>

