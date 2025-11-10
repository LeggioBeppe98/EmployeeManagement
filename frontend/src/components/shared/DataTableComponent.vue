<!-- frontend/src/components/shared/DataTableComponent.vue -->
<template>
    <div class="data-table-container">
        <!-- Filtri -->
        <div v-if="showFilters" class="filters-section">
            <div class="search-box">
                <InputText v-model="filters.search" placeholder="Cerca..." class="search-input" />
            </div>



            <div class="filter-controls">
                <Button @click="$emit('add-new')" icon="pi pi-plus" label="Nuovo" class="p-button-success" />
            </div>
        </div>

        <!-- Tabella PrimeVue -->
        <DataTable :value="filteredData" :loading="loading" :paginator="true" :rows="10"
            paginatorTemplate="FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink CurrentPageReport RowsPerPageDropdown"
            currentPageReportTemplate="Mostrando {first} a {last} di {totalRecords} record">
            <!-- Colonne dinamiche -->
            <Column v-for="col in columns" :key="col.field" :field="col.field" :header="col.header"
                :sortable="col.sortable">
                <template #body="slotProps">
                    {{ formatCell(slotProps.data, col) }}
                </template>
            </Column>

            <!-- Colonna Azioni -->
            <Column header="Azioni" style="width: 150px">
                <template #body="slotProps">
                    <Button @click="$emit('edit', slotProps.data)" icon="pi pi-pencil"
                        class="p-button-rounded p-button-text p-button-primary" />
                    <Button @click="$emit('delete', slotProps.data)" icon="pi pi-trash"
                        class="p-button-rounded p-button-text p-button-danger" />
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
        default: () => ['name', 'description', 'budget']  // Default: cerca solo nel campo 'name'
    }
})

const emit = defineEmits(['add-new', 'edit', 'delete'])

const filters = ref({
    search: ''
})

const filteredData = computed(() => {
    if (!filters.value.search) {
        return props.data  // Se non c'è ricerca, restituisci tutto
    }

    const searchTerm = filters.value.search.toLowerCase()

    return props.data.filter(item => {
        // Cerca in tutti i campi specificati in searchFields
        return props.searchFields.some(field => {
            const value = item[field]
            return value && value.toString().toLowerCase().includes(searchTerm)
        })
    })
})


const formatCell = (rowData, column) => {
    const value = rowData[column.field]

    // Formattazione condizionale
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
</style>