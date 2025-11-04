<template>
  <div class="login-container">
    <div class="login-card">
      <h1>🏢 Employee Dashboard</h1>
      <p>Accedi al sistema di gestione dipendenti</p>
      
      <form @submit.prevent="handleLogin" class="login-form">
        <div class="form-group">
          <label for="username">Username</label>
          <input 
            id="username"
            v-model="credentials.username" 
            type="text" 
            placeholder="Inserisci username"
            required
            :disabled="isLoading"
          >
        </div>
        
        <div class="form-group">
          <label for="password">Password</label>
          <input 
            id="password"
            v-model="credentials.password" 
            type="password" 
            placeholder="Inserisci password"
            required
            :disabled="isLoading"
          >
        </div>
        
        <button type="submit" :disabled="isLoading" class="login-button">
          {{ isLoading ? 'Accesso in corso...' : 'Accedi' }}
        </button>
        
        <div v-if="error" class="error-message">
          {{ error }}
        </div>
      </form>
      
      <div class="demo-credentials">
        <p><strong>Credenziali di test:</strong></p>
        <p>Username: <code>admin</code></p>
        <p>Password: <code>pw_3112_tk</code></p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '../stores/user'

const router = useRouter()
const userStore = useUserStore()

const credentials = ref({
  username: '',
  password: ''
})

const isLoading = ref(false)
const error = ref(null) 

const handleLogin = async () => {
  try {
    isLoading.value = true
    error.value = null
    await userStore.login(credentials.value)
    
    // Reindirizza alla dashboard dopo login successo
    router.push('/dashboard')
    
  } catch (error) {
    // L'errore è già gestito nello store
    console.log('Login failed')
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
.login-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.login-card {
  background: white;
  padding: 2rem;
  border-radius: 10px;
  box-shadow: 0 10px 25px rgba(0,0,0,0.1);
  width: 100%;
  max-width: 400px;
}

.login-card h1 {
  text-align: center;
  margin-bottom: 0.5rem;
  color: #2c3e50;
}

.login-card p {
  text-align: center;
  color: #7f8c8d;
  margin-bottom: 2rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  color: #2c3e50;
  font-weight: 500;
}

.form-group input {
  width: 100%;
  padding: 0.75rem;
  border: 2px solid #e9ecef;
  border-radius: 5px;
  font-size: 1rem;
  transition: border-color 0.3s;
}

.form-group input:focus {
  outline: none;
  border-color: #3498db;
}

.login-button {
  width: 100%;
  padding: 0.75rem;
  background: #3498db;
  color: white;
  border: none;
  border-radius: 5px;
  font-size: 1rem;
  cursor: pointer;
  transition: background 0.3s;
}

.login-button:hover:not(:disabled) {
  background: #2980b9;
}

.login-button:disabled {
  background: #bdc3c7;
  cursor: not-allowed;
}

.error-message {
  margin-top: 1rem;
  padding: 0.75rem;
  background: #e74c3c;
  color: white;
  border-radius: 5px;
  text-align: center;
}

.demo-credentials {
  margin-top: 2rem;
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 5px;
  border-left: 4px solid #3498db;
}

.demo-credentials p {
  margin: 0.25rem 0;
  text-align: left;
}

.demo-credentials code {
  background: #e9ecef;
  padding: 0.2rem 0.4rem;
  border-radius: 3px;
  font-family: monospace;
}
</style>