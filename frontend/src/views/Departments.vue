<template>
  <div class="departments-page">
    <!-- Header -->
    <div class="page-header">
      <h1>🏢 Gestione Dipartimenti</h1>
      <p>Gestisci i dipartimenti aziendali e i budget</p>
    </div>

    <!-- Tabella Dipartimenti -->
    <DataTableComponent
      :data="departmentsStore.departments"
      :columns="tableColumns"
      :loading="departmentsStore.isLoading"
      @add-new="showCreateModal = true"
      @edit="editDepartment"
      @delete="confirmDelete"
    />

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
import DataTableComponent from '../components/shared/DataTableComponent.vue'

const departmentsStore = useDepartmentsStore()
const employeesStore = useEmployeesStore()

// Stato componente
const showCreateModal = ref(false)
const editingDepartment = ref(null)
const showDeleteModal = ref(false)
const departmentToDelete = ref(null)
const selectedDepartments = ref([])
const isSubmitting = ref(false)

// DEFINIZIONE COLONNE
const tableColumns = ref([
  { field: 'name', header: 'Nome', sortable: true },
  { field: 'description', header: 'Descrizione', sortable: true },
  { field: 'budget', header: 'Budget', sortable: true, format: 'currency' },
  { 
    field: 'employeeCount', 
    header: 'Dipendenti', 
    sortable: true,
    computed: (dept) => {
      if (!employeesStore.employees.length) return '0 dipendenti'
      const count = employeesStore.employees.filter(emp => 
        emp.department === dept.id || emp.department?.id === dept.id
      ).length
      return `${count} dipendenti`
    }
  }
])

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

// METODI PER GESTIRE GLI EVENTI DEL COMPONENTE
const editDepartment = (department) => {
  console.log('Modifica dipartimento:', department)
  editingDepartment.value = department
  departmentForm.value = { ...department }
  showCreateModal.value = true
}

const confirmDelete = (department) => {
  console.log('Elimina dipartimento:', department)
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