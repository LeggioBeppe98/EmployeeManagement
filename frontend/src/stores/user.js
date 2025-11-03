// gestore dello stato 
import { defineStore } from 'pinia' 
import { ref, computed } from 'vue'
import axios from 'axios'

export const useUserStore = defineStore('user', () => {
  const user = ref(null)
  const token = ref(localStorage.getItem('token'))

  const isAuthenticated = true// computed(() => !!token.value)

  // Configura axios per usare il token
  /*if (token.value) {
    axios.defaults.headers.common['Authorization'] = `Bearer ${token.value}`
  }*/

  const login = async (credentials) => {
    try {
      //const response = await axios.post('http://localhost:8000/api/token/', credentials)
      //token.value = response.data.access
      //localStorage.setItem('token', token.value)
      //axios.defaults.headers.common['Authorization'] = true;//`Bearer ${token.value}`
      
      // Recupera info utente
      //const userResponse = await axios.get('http://localhost:8000/api/user/')
      user.value = {
        id: 1,
        username: 'admin',
        email: 'admin@azienda.com',
        role: 'admin',
        first_name: 'Mario',
        last_name: 'Rossi'
      } 


      return true
    } catch (error) {
      logout()
      throw error
    }
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
    login,
    logout
  }
})