<!-- frontend/src/components/shared/DataTableComponent.vue -->
<template>
    <div class="data-table-container">
        <!-- Filtri -->
        <div v-if="showFilters" class="filters-section">
            <div class="filter-controls">
                <!-- Dropdown Filtro -->
                <Dropdown v-if="dropdownFilter && dropdownOptions" v-model="filters.dropdown" :options="dropdownOptions"
                    :optionLabel="dropdownLabel || 'name'" :placeholder="dropdownPlaceholder || 'Filtra...'"
                    class="filter-dropdown" showClear />

                <!-- Search -->
                <InputText v-model="filters.search" placeholder="Cerca..." class="search-input" />

                <Button @click="$emit('add-new')" icon="pi pi-plus" label="Nuovo" class="p-button-success" />
            </div>
        </div>

        <!-- Tabella -->
        <DataTable :value="filteredData" :loading="loading" :paginator="true" :rows="10"
            paginatorTemplate="FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink CurrentPageReport RowsPerPageDropdown"
            currentPageReportTemplate="Mostrando {first} a {last} di {totalRecords} record">
            <!-- Colonne dinamiche -->
            <Column v-for="col in columns" :key="col.field" :field="col.field" :header="col.header"
                :sortable="col.sortable">
                <template #body="slotProps">
                    <!-- ⭐ GESTIONE COLONNE CALCOLATE -->
                    <span v-if="col.computed">
                        {{ col.computed(slotProps.data) }}
                    </span>
                    <span v-else>
                        {{ formatCell(slotProps.data, col) }}
                    </span>
                </template>
            </Column>

            <!-- Colonna Azioni -->
            <Column header="Azioni" style="width: 150px">
                <template #body="slotProps">
                    <Button @click="$emit('edit', slotProps.data)" icon="pi pi-pencil"
                        class="p-button-rounded p-button-outlined p-button-primary" />
                    <Button @click="$emit('delete', slotProps.data)" icon="pi pi-trash"
                        class="p-button-rounded p-button-outlined p-button-danger" />
                </template>
            </Column>
        </DataTable>
    </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import InputText from 'primevue/inputtext'
import Button from 'primevue/button'
import Dropdown from 'primevue/dropdown'

const props = defineProps({
    data: Array,
    columns: Array,
    loading: Boolean,
    showFilters: {
        type: Boolean,
        default: true
    },
    searchFields: {
        type: Array,
        default: () => ['name']
    },
    dropdownFilter: String,
    dropdownOptions: Array,
    dropdownLabel: String,
    dropdownPlaceholder: String
})

const emit = defineEmits(['add-new', 'edit', 'delete'])

const filters = ref({
    search: '',
    dropdown: null
})

const filteredData = computed(() => {
    let filtered = props.data

    // Filtro ricerca
    if (filters.value.search) {
        const searchTerm = filters.value.search.toLowerCase()
        filtered = filtered.filter(item => {
            return props.searchFields.some(field => {
                const value = item[field]
                return value && value.toString().toLowerCase().includes(searchTerm)
            })
        })
    }

    // Filtro dropdown
    if (filters.value.dropdown && props.dropdownFilter) {
        filtered = filtered.filter(item => {
            const itemValue = item[props.dropdownFilter]
            const dropdownValue = filters.value.dropdown
            return itemValue === dropdownValue ||
                itemValue === dropdownValue?.id ||
                itemValue?.id === dropdownValue
        })
    }

    return filtered
})

const formatCell = (rowData, column) => {
    const value = rowData[column.field]

    if (column.format === 'currency') {
        return new Intl.NumberFormat('it-IT', { style: 'currency', currency: 'EUR' }).format(value)
    }

    if (column.format === 'date') {
        return new Date(value).toLocaleDateString('it-IT')
    }

    return value
}
</script>

<style scoped>
.data-table-container {
    background: white;
    border-radius: 10px;
    padding: 1rem;
}

.filter-controls {
    display: flex;
    gap: 1rem;
    align-items: center;
    flex-wrap: wrap;
}

.filter-dropdown,
.search-input {
    min-width: 200px;
}

.action-btn {
  color: #6c757d !important; /* Colore visibile */
}

.action-btn:hover {
  color: white !important;
}

</style>