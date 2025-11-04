import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import axios from 'axios'

export const useDashboardStore = defineStore('dashboard', () => {
  const stats = ref({
    totalEmployees: 0,
    activeEmployees: 0,
    averageSalary: 0,
    totalDepartments: 0,
    totalSalaryBudget: 0
  })
  
  const departmentDistribution = ref([])
  const salaryDistribution = ref([])
  const recentHires = ref([])
  
  const isLoading = ref(false)
  const error = ref(null)

  const fetchDashboardData = async () => {
    isLoading.value = true
    error.value = null
    
    try {
      // ⭐ CHIAMATA API REALE!
      const response = await axios.get('http://localhost:8000/api/dashboard/stats/')
      const data = response.data
      
      // Aggiorna i dati con la response reale
      stats.value = {
        totalEmployees: data.stats.total_employees,
        activeEmployees: data.stats.active_employees,
        averageSalary: data.stats.average_salary,
        totalDepartments: data.stats.total_departments,
        totalSalaryBudget: data.stats.total_salary_budget
      }
      
      departmentDistribution.value = data.department_distribution
      salaryDistribution.value = data.salary_distribution
      recentHires.value = data.recent_hires
      
      console.log('Dashboard data loaded:', data)
      
    } catch (err) {
      error.value = 'Errore nel caricamento dati dashboard'
      console.error('Dashboard fetch error:', err)
    } finally {
      isLoading.value = false
    }
  }

  return {
    stats,
    departmentDistribution,
    salaryDistribution,
    recentHires,
    isLoading,
    error,
    fetchDashboardData
  }
})