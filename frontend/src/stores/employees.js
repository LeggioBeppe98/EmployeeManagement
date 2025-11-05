import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import axios from 'axios'

export const useEmployeesStore = defineStore('employees', () => {
  // Stato
  const employees = ref([])
  const currentEmployee = ref(null)
  const isLoading = ref(false)
  const error = ref(null)
  
  // Filtri e ricerca
  const filters = ref({
    search: '',
    department: '',
    position: '',
    isActive: true
  })

  // Getter computati
  const filteredEmployees = computed(() => {
    let filtered = employees.value

    // Filtro ricerca
    if (filters.value.search) {
      const searchLower = filters.value.search.toLowerCase()
      filtered = filtered.filter(emp => 
        emp.first_name.toLowerCase().includes(searchLower) ||
        emp.last_name.toLowerCase().includes(searchLower) ||
        emp.email.toLowerCase().includes(searchLower) ||
        emp.position.toLowerCase().includes(searchLower)
      )
    }

    // Filtro dipartimento
    if (filters.value.department) {
      filtered = filtered.filter(emp => 
        emp.department == filters.value.department
      )
    }

    // Filtro posizione
    if (filters.value.position) {
      filtered = filtered.filter(emp => 
        emp.position === filters.value.position
      )
    }

    // Filtro stato attivo
    if (filters.value.isActive !== null) {
      filtered = filtered.filter(emp => 
        emp.is_active === filters.value.isActive
      )
    }

    return filtered
  })

  const uniquePositions = computed(() => {
    return [...new Set(employees.value.map(emp => emp.position))].filter(Boolean)
  })

  // Azioni
  const fetchEmployees = async () => {
    isLoading.value = true
    error.value = null
    try {
      const response = await axios.get('http://localhost:8000/api/employees/')
      employees.value = response.data
    } catch (err) {
      error.value = 'Errore nel caricamento dipendenti'
      console.error('Fetch employees error:', err)
    } finally {
      isLoading.value = false
    }
  }

  const fetchEmployee = async (id) => {
    isLoading.value = true
    try {
      const response = await axios.get(`http://localhost:8000/api/employees/${id}/`)
      currentEmployee.value = response.data
      return response.data
    } catch (err) {
      error.value = 'Errore nel caricamento dipendente'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  const createEmployee = async (employeeData) => {
    try {
      const response = await axios.post('http://localhost:8000/api/employees/', employeeData)
      employees.value.push(response.data)
      return response.data
    } catch (err) {
      error.value = 'Errore nella creazione dipendente'
      throw err
    }
  }

  const updateEmployee = async (id, employeeData) => {
    try {
      const response = await axios.put(`http://localhost:8000/api/employees/${id}/`, employeeData)
      const index = employees.value.findIndex(emp => emp.id === id)
      if (index !== -1) {
        employees.value[index] = response.data
      }
      return response.data
    } catch (err) {
      error.value = 'Errore nell\'aggiornamento dipendente'
      throw err
    }
  }

  const deleteEmployee = async (id) => {
    try {
      await axios.delete(`http://localhost:8000/api/employees/${id}/`)
      employees.value = employees.value.filter(emp => emp.id !== id)
    } catch (err) {
      error.value = 'Errore nell\'eliminazione dipendente'
      throw err
    }
  }

  const bulkUpdateStatus = async (ids, isActive) => {
    try {
      const promises = ids.map(id => 
        axios.patch(`http://localhost:8000/api/employees/${id}/`, { is_active: isActive })
      )
      await Promise.all(promises)
      
      // Aggiorna lo stato locale
      employees.value = employees.value.map(emp => 
        ids.includes(emp.id) ? { ...emp, is_active: isActive } : emp
      )
    } catch (err) {
      error.value = 'Errore nell\'aggiornamento multiplo'
      throw err
    }
  }

  const clearFilters = () => {
    filters.value = {
      search: '',
      department: '',
      position: '',
      isActive: true
    }
  }

  return {
    // Stato
    employees,
    currentEmployee,
    isLoading,
    error,
    filters,
    
    // Getter
    filteredEmployees,
    uniquePositions,
    
    // Azioni
    fetchEmployees,
    fetchEmployee,
    createEmployee,
    updateEmployee,
    deleteEmployee,
    bulkUpdateStatus,
    clearFilters
  }
})