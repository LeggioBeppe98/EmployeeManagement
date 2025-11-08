import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import axios from 'axios'

export const useDepartmentsStore = defineStore('departments', () => {
  // Stato
  const departments = ref([])
  const isLoading = ref(false)
  const error = ref(null)
  const filters = ref({
    search: '',
    departmentName: ''
  })

  const filteredDepartments = computed(() => {
    let filtered = departments.value

    // Filtro ricerca
    if (filters.value.search) {
      const searchLower = filters.value.search.toLowerCase()
      filtered = filtered.filter(dept =>
        dept.name.toLowerCase().includes(searchLower) ||
        (dept.description && dept.description.toLowerCase().includes(searchLower)) ||
        dept.budget.toString().includes(filters.value.search)
      )
    }

    // Filtro per ID dipartimento
    if (filters.value.departmentName) {
      filtered = filtered.filter(dept =>
        dept.name == filters.value.departmentName
      )
    }

    return filtered
  })

  // Getter - dipartimenti per select
  const departmentsForSelect = computed(() => {
    return departments.value.map(dept => ({
      id: dept.id,
      name: dept.name,
      value: dept.id  // Per compatibilità con i select
    }))
  })

  // Getter - dipartimenti per nome (per il debug)
  const departmentNames = computed(() => {
    return departments.value.map(dept => dept.name)
  })

  // Azioni

  const clearFilters = () => {
    filters.value = {
      search: '',
      departmentName: ''
    }
  }

  const fetchDepartments = async () => {
    isLoading.value = true
    error.value = null
    try {
      const response = await axios.get('http://localhost:8000/api/departments/')
      departments.value = response.data
      console.log('🏢 Dipartimenti caricati:', departments.value)
    } catch (err) {
      error.value = 'Errore nel caricamento dipartimenti'
      console.error('Fetch departments error:', err)
    } finally {
      isLoading.value = false
    }
  }

  const getDepartmentById = (id) => {
    return departments.value.find(dept => dept.id === id)
  }

  const getDepartmentByName = (name) => {
    return departments.value.find(dept => dept.name === name)
  }


  // Azioni CRUD - AGGIUNGI QUESTE
  const createDepartment = async (departmentData) => {
    try {
      const response = await axios.post('http://localhost:8000/api/departments/', departmentData)
      departments.value.push(response.data)
      return response.data
    } catch (err) {
      error.value = 'Errore nella creazione dipartimento'
      throw err
    }
  }

  const updateDepartment = async (id, departmentData) => {
    try {
      const response = await axios.put(`http://localhost:8000/api/departments/${id}/`, departmentData)
      const index = departments.value.findIndex(dept => dept.id === id)
      if (index !== -1) {
        departments.value[index] = response.data
      }
      return response.data
    } catch (err) {
      error.value = 'Errore nell\'aggiornamento dipartimento'
      throw err
    }
  }

  const deleteDepartment = async (id) => {
    try {
      await axios.delete(`http://localhost:8000/api/departments/${id}/`)
      departments.value = departments.value.filter(dept => dept.id !== id)
    } catch (err) {
      error.value = 'Errore nell\'eliminazione dipartimento'
      throw err
    }
  }

  return {
    // Stato
    departments,
    isLoading,
    error,
    filters,

    // Getter
    departmentsForSelect,
    departmentNames,
    filteredDepartments,

    // Azioni
    clearFilters,
    fetchDepartments,
    getDepartmentById,
    getDepartmentByName,
    createDepartment,   
    updateDepartment,    
    deleteDepartment
  }
})