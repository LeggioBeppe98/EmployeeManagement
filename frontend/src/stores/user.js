// gestore dello stato 
import { defineStore } from 'pinia' 
import { ref, computed } from 'vue'
import axios from 'axios'

export const useUserStore = defineStore('user', () => {
  const user = ref(null)
  const token = ref(localStorage.getItem('token'))

  const isLoading = ref(false)
  const error = ref(null)

  const isAuthenticated = computed(() => !!token.value)

  // Configura axios per usare il token
  if (token.value) {
    axios.defaults.headers.common['Authorization'] = `Bearer ${token.value}`
  }

  const login = async (credentials) => {
    isLoading.value = true
    error.value = null

    try {
      const response = await axios.post('http://localhost:8000/api/token/', credentials)
      token.value = response.data.access
      localStorage.setItem('token', token.value)
      axios.defaults.headers.common['Authorization'] = `Bearer ${token.value}`
      
      // Recupera info utente
      const userResponse = await axios.get('http://localhost:8000/api/user/')
      user.value = userResponse.data


      console.log('Login successful:', user.value)
      return true
    } catch (err) {
      error.value = 'Credenziali non valide'
      console.error('Login error:', err)
      logout()
      throw err
    } finally {
      isLoading.value = false
    }
  }
/**
 * Verifica se il token di accesso è valido.
 */
  const setupAxiosInterceptors = (storeInstance) => {  
  axios.interceptors.response.use(
    (response) => response,
    (error) => {
      if (error.response?.status === 401) {
        console.log('Token non valido - logout automatico')
        storeInstance.logout()  // ⭐ USA L'ISTANZA PASSATA
        window.location.href = '/login'
      }
      return Promise.reject(error)
    }
  )
}

  const logout = () => {
    user.value = null
    token.value = null
    localStorage.removeItem('token')
    delete axios.defaults.headers.common['Authorization']
  }

  return {
    user,
    token,
    isAuthenticated,
    isLoading,
    error,
    setupAxiosInterceptors,
    login,
    logout
  }
})