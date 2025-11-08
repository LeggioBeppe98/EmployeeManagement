<template>
  <div class="employees-page">
    <div class="page-header">
      <h1>👥 Gestione Dipendenti</h1>
      <p>Gestisci tutti i dipendenti dell'azienda</p>
    </div>

    <!-- Filtri e Ricerca -->
    <div class="filters-section">
      <div class="search-box">
        <input 
          v-model="employeesStore.filters.search"
          type="text" 
          placeholder="Cerca per nome, cognome, email o posizione..."
          class="search-input"
        >
      </div>

      <div class="filter-controls">
        <select v-model="employeesStore.filters.department" class="filter-select">
          <option value="">Tutti i dipartimenti</option>
          <option v-for="dept in departments" :key="dept.id" :value="dept.id">
            {{ dept.name }}
          </option>
        </select>

        <select v-model="employeesStore.filters.position" class="filter-select">
          <option value="">Tutte le posizioni</option>
          <option v-for="position in employeesStore.uniquePositions" :key="position" :value="position">
            {{ position }}
          </option>
        </select>

        <select v-model="employeesStore.filters.isActive" class="filter-select">
          <option :value="null">Tutti gli stati</option>
          <option :value="true">Solo attivi</option>
          <option :value="false">Solo non attivi</option>
        </select>

        <button @click="employeesStore.clearFilters" class="clear-filters-btn">
          Pulisci filtri
        </button>

        <button @click="showCreateModal = true" class="add-employee-btn">
          + Nuovo Dipendente
        </button>
      </div>
    </div>

    <!-- Tabella Dipendenti -->
    <div class="employees-table-container">
      <div v-if="employeesStore.isLoading" class="loading-state">
        <p>Caricamento dipendenti...</p>
      </div>

      <div v-else-if="employeesStore.error" class="error-state">
        <p>{{ employeesStore.error }}</p>
        <button @click="loadEmployees" class="retry-btn">Riprova</button>
      </div>

      <div v-else class="table-wrapper">
        <table class="data-table">
          <thead>
            <tr>
              <th>
                <input 
                  type="checkbox" 
                  :checked="allSelected"
                  @change="toggleSelectAll"
                >
              </th>
              <th>Nome</th>
              <th>Email</th>
              <th>Posizione</th>
              <th>Dipartimento</th>
              <th>Stipendio</th>
              <th>Data Assunzione</th>
              <th>Stato</th>
              <th>Azioni</th>
            </tr>
          </thead>
          <tbody>
            <tr 
              v-for="employee in employeesStore.filteredEmployees" 
              :key="employee.id"
              :class="{ 'selected': selectedEmployees.includes(employee.id) }"
            >
              <td>
                <input 
                  type="checkbox" 
                  :checked="selectedEmployees.includes(employee.id)"
                  @change="toggleEmployeeSelection(employee.id)"
                >
              </td>
              <td>
                <strong>{{ employee.first_name }} {{ employee.last_name }}</strong>
              </td>
              <td>{{ employee.email }}</td>
              <td>{{ employee.position }}</td>
              <td>
                <span class="dept-badge">{{ getDepartmentName(employee.department) }}</span>
              </td>
              <td>€{{ formatCurrency(employee.salary) }}</td>
              <td>{{ formatDate(employee.hire_date) }}</td>
              <td>
                <span :class="['status-badge', employee.is_active ? 'active' : 'inactive']">
                  {{ employee.is_active ? 'Attivo' : 'Non attivo' }}
                </span>
              </td>
              <td class="actions">
                <button @click="editEmployee(employee)" class="edit-btn" title="Modifica">
                  ✏️
                </button>
                <button @click="confirmDelete(employee)" class="delete-btn" title="Elimina">
                  🗑️
                </button>
              </td>
            </tr>
          </tbody>
        </table>

        <!-- Definizione Overlay -->

        <!-- Messaggio nessun risultato -->
        <div v-if="employeesStore.filteredEmployees.length === 0" class="no-results">
          <p>Nessun dipendente trovato con i filtri attuali.</p>
        </div>
      </div>
    </div>

    <!-- Azioni Batch (se selezionati) -->
    <div v-if="selectedEmployees.length > 0" class="batch-actions">
      <span>{{ selectedEmployees.length }} dipendenti selezionati</span>
      <button @click="bulkActivate" class="batch-btn activate">Attiva Selezionati</button>
      <button @click="bulkDeactivate" class="batch-btn deactivate">Disattiva Selezionati</button>
      <button @click="bulkDelete" class="batch-btn delete">Elimina Selezionati</button>
      <button @click="clearSelection" class="batch-btn clear">Deseleziona Tutti</button>
    </div>

    <!-- Modal Creazione/Modifica -->
    <div v-if="showCreateModal || editingEmployee" class="modal-overlay">
      <div class="modal">
        <h3>{{ editingEmployee ? 'Modifica Dipendente' : 'Nuovo Dipendente' }}</h3>
        
        <form @submit.prevent="submitEmployeeForm" class="form-base">
          <div class="form-row">
            <div class="form-group">
              <label>Nome *</label>
              <input v-model="employeeForm.first_name" type="text" required>
            </div>
            <div class="form-group">
              <label>Cognome *</label>
              <input v-model="employeeForm.last_name" type="text" required>
            </div>
          </div>

          <div class="form-group">
            <label>Email *</label>
            <input v-model="employeeForm.email" type="email" required>
          </div>

          <div class="form-group">
            <label>Telefono</label>
            <input v-model="employeeForm.phone" type="tel">
          </div>

          <div class="form-row">
            <div class="form-group">
              <label>Posizione *</label>
              <input v-model="employeeForm.position" type="text" required>
            </div>
            <div class="form-group">
              <label>Stipendio *</label>
              <input v-model="employeeForm.salary" type="number" step="0.01" required>
            </div>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label>Data Assunzione *</label>
              <input v-model="employeeForm.hire_date" type="date" required>
            </div>
            <div class="form-group">
              <label>Dipartimento *</label>
              <select v-model="employeeForm.department" required>
                <option value="">Seleziona dipartimento</option>
                <option v-for="dept in departments" :key="dept.id" :value="dept.id">
                  {{ dept.name }}
                </option>
              </select>
            </div>
          </div>

          <div class="form-group">
            <label>
              <input v-model="employeeForm.is_active" type="checkbox">
              Dipendente attivo
            </label>
          </div>

          <div class="form-actions">
            <button type="button" @click="closeModal" class="cancel-btn">Annulla</button>
            <button type="submit" :disabled="isSubmitting" class="submit-btn">
              {{ isSubmitting ? 'Salvataggio...' : (editingEmployee ? 'Aggiorna' : 'Crea') }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Modal Conferma Eliminazione -->
    <div v-if="showDeleteModal" class="modal-overlay">
      <div class="modal confirm-modal">
        <h3>Conferma Eliminazione</h3>
        <p>Sei sicuro di voler eliminare il dipendente <strong>{{ employeeToDelete?.first_name }} {{ employeeToDelete?.last_name }}</strong>?</p>
        <div class="confirm-actions">
          <button @click="showDeleteModal = false" class="cancel-btn">Annulla</button>
          <button @click="deleteEmployee" class="delete-confirm-btn">Elimina</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useEmployeesStore } from '../stores/employees'
import { useDashboardStore } from '../stores/dashboard'
import { useDepartmentsStore } from '../stores/departments' 

const employeesStore = useEmployeesStore()
const dashboardStore = useDashboardStore()
const departmentsStore = useDepartmentsStore()

// Stato componente
const showCreateModal = ref(false)
const editingEmployee = ref(null)
const showDeleteModal = ref(false)
const employeeToDelete = ref(null)
const selectedEmployees = ref([])
const isSubmitting = ref(false)

// Form dati
const employeeForm = ref({
  first_name: '',
  last_name: '',
  email: '',
  phone: '',
  position: '',
  salary: '',
  hire_date: '',
  department: '',
  is_active: true
})

// Computed
const allSelected = computed(() => {
  return employeesStore.filteredEmployees.length > 0 && 
        selectedEmployees.value.length === employeesStore.filteredEmployees.length
})

const departments = computed(() => {
  return departmentsStore.departmentsForSelect
})

// Metodi
const loadEmployees = () => {
  employeesStore.fetchEmployees()
}

const loadDepartments = () => {
  departmentsStore.fetchDepartments()
}

const getDepartmentName = (deptId) => {
  const dept = departments.value.find(d => d.id == deptId)
  return dept ? dept.name : 'N/A'
}

const formatCurrency = (amount) => {
  return new Intl.NumberFormat('it-IT', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  }).format(amount)
}

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('it-IT')
}

const toggleSelectAll = () => {
  if (allSelected.value) {
    selectedEmployees.value = []
  } else {
    selectedEmployees.value = employeesStore.filteredEmployees.map(emp => emp.id)
  }
}

const toggleEmployeeSelection = (employeeId) => {
  const index = selectedEmployees.value.indexOf(employeeId)
  if (index > -1) {
    selectedEmployees.value.splice(index, 1)
  } else {
    selectedEmployees.value.push(employeeId)
  }
}

const clearSelection = () => {
  selectedEmployees.value = []
}

const editEmployee = (employee) => {
  editingEmployee.value = employee
  employeeForm.value = { ...employee }
  // Converti la data per l'input
  if (employeeForm.value.hire_date) {
    employeeForm.value.hire_date = employeeForm.value.hire_date.split('T')[0]
  }
}

const confirmDelete = (employee) => {
  employeeToDelete.value = employee
  showDeleteModal.value = true
}

const submitEmployeeForm = async () => {
  isSubmitting.value = true
  try {
    // PREPARA I DATI - ORA DEPARTMENT È GIÀ L'ID NUMERICO
    const formData = {
      first_name: employeeForm.value.first_name,
      last_name: employeeForm.value.last_name,
      email: employeeForm.value.email,
      phone: employeeForm.value.phone || '',
      position: employeeForm.value.position,
      salary: parseFloat(employeeForm.value.salary),
      hire_date: employeeForm.value.hire_date,
      department: parseInt(employeeForm.value.department),  // ⭐ CONVERTI IN NUMERO
      is_active: employeeForm.value.is_active
    }

    console.log('🔄 Dati per il backend:', formData)

    if (editingEmployee.value) {
      await employeesStore.updateEmployee(editingEmployee.value.id, formData)
    } else {
      await employeesStore.createEmployee(formData)
    }
    closeModal()
  } catch (error) {
    console.error('❌ Error saving employee:', error)
    console.error('📋 Dettaglio errore backend:', error.response?.data)
  } finally {
    isSubmitting.value = false
  }
}

const deleteEmployee = async () => {
  try {
    await employeesStore.deleteEmployee(employeeToDelete.value.id)
    showDeleteModal.value = false
    employeeToDelete.value = null
  } catch (error) {
    console.error('Error deleting employee:', error)
  }
}

const bulkActivate = async () => {
  try {
    await employeesStore.bulkUpdateStatus(selectedEmployees.value, true)
    clearSelection()
  } catch (error) {
    console.error('Error bulk activating:', error)
  }
}

const bulkDeactivate = async () => {
  try {
    await employeesStore.bulkUpdateStatus(selectedEmployees.value, false)
    clearSelection()
  } catch (error) {
    console.error('Error bulk deactivating:', error)
  }
}

const bulkDelete = async () => {
  if (confirm(`Sei sicuro di voler eliminare ${selectedEmployees.value.length} dipendenti?`)) {
    try {
      for (const id of selectedEmployees.value) {
        await employeesStore.deleteEmployee(id)
      }
      clearSelection()
    } catch (error) {
      console.error('Error bulk deleting:', error)
    }
  }
}

const closeModal = () => {
  showCreateModal.value = false
  editingEmployee.value = null
  employeeForm.value = {
    first_name: '',
    last_name: '',
    email: '',
    phone: '',
    position: '',
    salary: '',
    hire_date: '',
    department: '',
    is_active: true
  }
}

// Lifecycle
onMounted(() => {
  loadEmployees()
  loadDepartments()
})
</script>
<style>
/* Import condiviso */
@import '../assets/css/shared.css';
</style>