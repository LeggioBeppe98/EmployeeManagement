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
        <table class="employees-table">
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
        
        <form @submit.prevent="submitEmployeeForm" class="employee-form">
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

<style scoped>
.employees-page {
  padding: 1rem;
}

.page-header {
  margin-bottom: 2rem;
}

.page-header h1 {
  color: #2c3e50;
  margin-bottom: 0.5rem;
}

.page-header p {
  color: #7f8c8d;
}

/* Filtri */
.filters-section {
  background: white;
  padding: 1.5rem;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  margin-bottom: 2rem;
}

.search-input {
  width: 100%;
  padding: 0.75rem;
  border: 2px solid #e9ecef;
  border-radius: 5px;
  font-size: 1rem;
}

.filter-controls {
  display: flex;
  gap: 1rem;
  margin-top: 1rem;
  flex-wrap: wrap;
  align-items: center;
}

.filter-select {
  padding: 0.5rem;
  border: 1px solid #e9ecef;
  border-radius: 5px;
  background: white;
}

.clear-filters-btn {
  background: #95a5a6;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 5px;
  cursor: pointer;
}

.add-employee-btn {
  background: #27ae60;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 5px;
  cursor: pointer;
  margin-left: auto;
}

/* Tabella */
.employees-table-container {
  background: white;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  overflow: hidden;
}

.employees-table {
  width: 100%;
  border-collapse: collapse;
}

.employees-table th,
.employees-table td {
  padding: 1rem;
  text-align: left;
  border-bottom: 1px solid #ecf0f1;
}

.employees-table th {
  background: #f8f9fa;
  font-weight: 600;
  color: #2c3e50;
}

.employees-table tr:hover {
  background: #f8f9fa;
}

.employees-table tr.selected {
  background: #e3f2fd;
}

/* Badges */
.dept-badge {
  background: #3498db;
  color: white;
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.8rem;
}

.status-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 500;
}

.status-badge.active {
  background: #27ae60;
  color: white;
}

.status-badge.inactive {
  background: #e74c3c;
  color: white;
}

/* Azioni */
.actions {
  display: flex;
  gap: 0.5rem;
}

.edit-btn, .delete-btn {
  background: none;
  border: none;
  cursor: pointer;
  padding: 0.25rem;
  border-radius: 3px;
}

.edit-btn:hover {
  background: #3498db;
}

.delete-btn:hover {
  background: #e74c3c;
}

/* Batch Actions */
.batch-actions {
  position: fixed;
  bottom: 2rem;
  left: 50%;
  transform: translateX(-50%);
  background: #2c3e50;
  color: white;
  padding: 1rem 2rem;
  border-radius: 10px;
  display: flex;
  gap: 1rem;
  align-items: center;
  box-shadow: 0 4px 20px rgba(0,0,0,0.3);
}

.batch-btn {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  color: white;
}

.batch-btn.activate {
  background: #27ae60;
}

.batch-btn.deactivate {
  background: #f39c12;
}

.batch-btn.delete {
  background: #e74c3c;
}

.batch-btn.clear {
  background: #95a5a6;
}

/* Modal */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0,0,0,0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal {
  background: white;
  padding: 2rem;
  border-radius: 10px;
  width: 90%;
  max-width: 600px;
  max-height: 90vh;
  overflow-y: auto;
}

.employee-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group label {
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #2c3e50;
}

.form-group input,
.form-group select {
  padding: 0.75rem;
  border: 2px solid #e9ecef;
  border-radius: 5px;
  font-size: 1rem;
}

.form-group input:focus,
.form-group select:focus {
  outline: none;
  border-color: #3498db;
}

.form-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  margin-top: 1rem;
}

.cancel-btn {
  background: #95a5a6;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 5px;
  cursor: pointer;
}

.submit-btn {
  background: #3498db;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 5px;
  cursor: pointer;
}

.submit-btn:disabled {
  background: #bdc3c7;
  cursor: not-allowed;
}

.delete-confirm-btn {
  background: #e74c3c;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 5px;
  cursor: pointer;
}

/* Stati */
.loading-state, .error-state, .no-results {
  padding: 3rem;
  text-align: center;
  color: #7f8c8d;
}

.retry-btn {
  background: #3498db;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 5px;
  cursor: pointer;
  margin-top: 1rem;
}

/* Responsive */
@media (max-width: 768px) {
  .form-row {
    grid-template-columns: 1fr;
  }
  
  .filter-controls {
    flex-direction: column;
    align-items: stretch;
  }
  
  .batch-actions {
    flex-direction: column;
    width: 90%;
  }
}
</style>