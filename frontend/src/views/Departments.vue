<template>
  <div class="departments-page">
    <!-- Header -->
    <div class="page-header">
      <h1>🏢 Gestione Dipartimenti</h1>
      <p>Gestisci i dipartimenti aziendali e i budget</p>
    </div>

    <!-- Filtri e Azioni -->
    <div class="filters-section">
      <div class="search-box">
        <input v-model="departmentsStore.filters.search" type="text"
          placeholder="Cerca per nome, descrizione o budget..." class="search-input">
      </div>

      <div class="filter-controls">
        <select v-model="departmentsStore.filters.departmentName" class="filter-select">
          <option value="">Tutti i dipartimenti</option>
          <option v-for="dept in departments" :key="dept.id" :value="dept.name">
            {{ dept.name }}
          </option>
        </select>

        <button @click="departmentsStore.clearFilters" class="clear-filters-btn">
          Pulisci filtri
        </button>

        <button @click="showCreateModal = true" class="add-employee-btn">
          + Nuovo Dipartimento
        </button>
      </div>
    </div>

    <!-- Tabella Dipartimenti -->
    <div class="employees-table-container">
      <!-- Tabella con: Nome, Budget, N° Dipendenti, Azioni -->
      <div v-if="departmentsStore.isLoading" class="loading-state">
        <p>Caricamento dipendenti...</p>
      </div>

      <div v-else-if="departmentsStore.error" class="error-state">
        <p>{{ departmentsStore.error }}</p>
        <button @click="loadDepartments" class="retry-btn">Riprova</button>
      </div>

      <div v-else class="table-wrapper">
        <table class="data-table">
          <thead>
            <tr>
              <th>
                <input type="checkbox" :checked="allSelected" @change="toggleSelectAll">
              </th>
              <th>Nome</th>
              <th>Descrizione</th>
              <th>Budget</th>
              <th>N. Dipendenti</th>
              <th>Azioni</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="dept in departmentsStore.filteredDepartments"
              :class="{ 'selected': selectedDepartments.includes(dept.id) }">
              <td>
                <input type="checkbox" :checked="selectedDepartments.includes(dept.id)"
                  @change="toggleDepartmentSelection(dept.id)">
              </td>
              <td>
                <strong>{{ dept.name }}</strong>
              </td>
              <td>
                <span class="description">{{ dept.description || 'Nessuna descrizione' }}</span>
              </td>
              <td>
                <span class="budget">€{{ formatCurrency(dept.budget) }}</span>
              </td>
              <td>
                <span class="employee-count">{{ getEmployeeCount(dept.id) }} dipendenti</span>
              </td>
              <td class="actions">
                <button @click="editDepartment(dept)" class="edit-btn" title="Modifica">
                  ✏️
                </button>
                <button @click="confirmDelete(dept)" class="delete-btn" title="Elimina">
                  🗑️
                </button>
              </td>
            </tr>
          </tbody>
        </table>

        <!-- Messaggio nessun risultato -->
        <div v-if="departmentsStore.filteredDepartments.length === 0" class="no-results">
          <p>Nessun dipendente trovato con i filtri attuali.</p>
        </div>
      </div>
    </div>

    <!-- Definizione Overlay -->
    <div v-if="selectedDepartments.length > 0" class="batch-actions">
      <span>{{ selectedDepartments.length }} dipartimenti selezionati</span>
      <button @click="bulkDelete" class="batch-btn delete">Elimina Selezionati</button>
      <button @click="clearSelection" class="batch-btn clear">Deseleziona Tutti</button>
    </div>
    <!-- Modal Creazione/Modifica -->
    <div v-if="showCreateModal || editingDepartment" class="modal-overlay">
      <div class="modal">
        <h3>{{ editingDepartment ? 'Modifica Dipartimento' : 'Nuovo Dipartimento' }}</h3>

        <form @submit.prevent="submitDepartmentForm" class="form-base">
          <div class="form-group">
            <label>Nome Dipartimento *</label>
            <input v-model="departmentForm.name" type="text" placeholder="Es: IT, Marketing, Risorse Umane..." required
              :disabled="isSubmitting">
          </div>

          <div class="form-group">
            <label>Descrizione</label>
            <textarea v-model="departmentForm.description" placeholder="Descrizione del dipartimento..." rows="3"
              :disabled="isSubmitting"></textarea>
          </div>

          <div class="form-group">
            <label>Budget Annuale (€) *</label>
            <input v-model="departmentForm.budget" type="number" step="0.01" min="0" placeholder="50000.00" required
              :disabled="isSubmitting">
          </div>

          <div class="form-actions">
            <button type="button" @click="closeModal" class="cancel-btn" :disabled="isSubmitting">
              Annulla
            </button>
            <button type="submit" :disabled="isSubmitting" class="submit-btn">
              {{ isSubmitting ? 'Salvataggio...' : (editingDepartment ? 'Aggiorna' : 'Crea') }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Modal Conferma Eliminazione -->
    <div v-if="showDeleteModal" class="modal-overlay">
      <div class="modal confirm-modal">
        <h3>Conferma Eliminazione</h3>
        <p>
          Sei sicuro di voler eliminare il dipartimento
          <strong>"{{ departmentToDelete?.name }}"</strong>?
        </p>
        <p class="warning-text">
          ⚠️ Attenzione: Questa azione non può essere annullata!
        </p>
        <div class="confirm-actions">
          <button @click="showDeleteModal = false" class="btn-secondary">Annulla</button>
          <button @click="deleteDepartment" class="btn-danger">
            {{ isSubmitting ? 'Eliminazione...' : 'Elimina' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useDepartmentsStore } from '../stores/departments'
import { useEmployeesStore } from '../stores/employees' 

const departmentsStore = useDepartmentsStore()
const employeesStore = useEmployeesStore()

// Stato componente
const showCreateModal = ref(false)
const editingDepartment = ref(null)
const showDeleteModal = ref(false)
const departmentToDelete = ref(null)
const selectedDepartments = ref([])
const isSubmitting = ref(false)

// Form dati
const departmentForm = ref({
  name: '',
  description: '',
  budget: ''
})

const departments = computed(() => {
  return departmentsStore.departments
})

// Computed
const allSelected = computed(() => {
  return departmentsStore.filteredDepartments.length > 0 &&
    selectedDepartments.value.length === departmentsStore.filteredDepartments.length
})

// Metodi
const loadDepartments = () => {
  departmentsStore.fetchDepartments()
}

// Metodo per contare i dipendenti
const getEmployeeCount = (deptId) => {
  if (!employeesStore.employees.length) return 0
  
  return employeesStore.employees.filter(emp => 
    emp.department === deptId || emp.department?.id === deptId
  ).length
}

const toggleSelectAll = () => {
  if (allSelected.value) {
    selectedDepartments.value = []
  } else {
    selectedDepartments.value = departmentsStore.filteredDepartments.map(dept => dept.id)  // ⭐ "dept"
  }
}

const clearSelection = () => {
  selectedDepartments.value = []
}

const editDepartment = (department) => {
  editingDepartment.value = department
  departmentForm.value = { ...department }
}

// Correggi la funzione confirmDelete
const confirmDelete = (department) => {
  departmentToDelete.value = department  
  showDeleteModal.value = true
}

const formatCurrency = (amount) => {
  return new Intl.NumberFormat('it-IT', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  }).format(amount)
}

const toggleDepartmentSelection = (deptId) => {
  const index = selectedDepartments.value.indexOf(deptId)
  if (index > -1) {
    selectedDepartments.value.splice(index, 1)
  } else {
    selectedDepartments.value.push(deptId)
  }
}

const submitDepartmentForm = async () => {
  isSubmitting.value = true
  try {
    // Prepara i dati per il backend
    const formData = {
      name: departmentForm.value.name,
      description: departmentForm.value.description || '', // Se vuoto, stringa vuota
      budget: parseFloat(departmentForm.value.budget) // Converti in numero
    }

    console.log('🔄 Dati per il backend:', formData)

    if (editingDepartment.value) {
      await departmentsStore.updateDepartment(editingDepartment.value.id, formData)
    } else {
      await departmentsStore.createDepartment(formData)
    }
    closeModal()
  } catch (error) {
    console.error('❌ Error saving department:', error)
    console.error('📋 Dettaglio errore backend:', error.response?.data)
  } finally {
    isSubmitting.value = false
  }
}

// Correggi la funzione deleteDepartment
const deleteDepartment = async () => {
  isSubmitting.value = true
  try {
    await departmentsStore.deleteDepartment(departmentToDelete.value.id)
    showDeleteModal.value = false
    departmentToDelete.value = null
  } catch (error) {
    console.error('Error deleting department:', error)
  } finally {
    isSubmitting.value = false
  }
}

const bulkDelete = async () => {
  if (confirm(`Sei sicuro di voler eliminare ${selectedDepartments.value.length} dipartimenti?`)) {
    try {
      for (const id of selectedDepartments.value) {
        await departmentsStore.deleteDepartment(id)
      }
      clearSelection()
    } catch (error) {
      console.error('Error bulk deleting:', error)
    }
  }
}

const closeModal = () => {
  showCreateModal.value = false
  editingDepartment.value = null
  departmentForm.value = {
    name: '',
    description: '',
    budget: ''
  }
}

// Lifecycle
onMounted(() => {
  loadDepartments()
  employeesStore.fetchEmployees()
})
</script>

<style>
/* Import condiviso */
@import '../assets/css/shared.css';
</style>