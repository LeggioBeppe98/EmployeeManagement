<!-- frontend/src/components/shared/DataTableComponent.vue -->
<template>
    <div class="data-table-wrapper shadow-xl/30">

        <!-- FILTRI -->
        <div v-if="showFilters" class="mb-3 mt-6">
            <div class="flex justify-end items-center gap-3">

                <!-- Dropdown filter -->
                <Dropdown v-if="dropdownFilter && dropdownOptions" v-model="filters.dropdown" :options="dropdownOptions"
                    :optionLabel="dropdownLabel || 'name' || 'description' || 'price'"
                    :placeholder="dropdownPlaceholder || 'Filtra...'" showClear class="w-20rem" />

                <!-- Search box -->
                <div class="flex justify-between align-items-center gap-3 w-full mac-w-100">
                    <div class="align-left">
                        <IconField>
                            <InputIcon class="pi pi-search" />
                            <InputText v-model="filters.search" placeholder="Cerca" />
                        </IconField>
                    </div>
                    <div class="align-right">
                        <div class="flex justify-end gap-3">
                            <div>
                                <Button label="Nuovo" icon="pi pi-plus" @click="$emit('add-new')" />
                            </div>
                            <div>
                                <Button icon="pi pi-download" @click="exportSelected"
                                    :disabled="selectedItems.length === 0" severity="secondary" />
                            </div>
                            <div>
                                <Button icon="pi pi-trash"
                                    @click="$emit('delete-selected', selectedItems)"
                                    :disabled="selectedItems.length === 0" severity="secondary" />
                            </div>
                        </div>

                    </div>
                </div>
            </div>
        </div>

        <!-- DATATABLE -->
        <div>
            <DataTable :value="filteredData" :loading="loading" :paginator="true" :rows="10" class="p-datatable-sm"
                v-model:selection="selectedItems" dataKey="id"
                paginatorTemplate="FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink "
                currentPageReportTemplate="Mostrando {first} a {last} di {totalRecords} record">

                <!-- Colonna select all -->
                <Column selectionMode="multiple" headerStyle="width: 3rem"></Column>

                <!-- Colonne dinamiche -->
                <Column v-for="col in columns" :key="col.field" :field="col.field" :header="col.header"
                    :sortable="col.sortable">
                    <template #body="slotProps">
                        <span v-if="col.computed">
                            {{ col.computed(slotProps.data) }}
                        </span>
                        <span v-else>
                            {{ formatCell(slotProps.data, col) }}
                        </span>
                    </template>
                </Column>

                <!-- Colonna azioni -->
                <Column header="Azioni" style="width: 150px">
                    <template #body="slotProps">
                        <div class="flex gap-2">

                            <Button @click="$emit('edit', slotProps.data)" icon="pi pi-pencil" severity="info" outlined
                                rounded />

                            <Button @click="$emit('delete', slotProps.data)" icon="pi pi-trash" severity="danger"
                                outlined rounded />

                        </div>
                    </template>
                </Column>

            </DataTable>
        </div>

    </div>
</template>


<script setup>
import { ref, computed } from 'vue'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import InputText from 'primevue/inputtext'
import Button from 'primevue/button'
import Dropdown from 'primevue/dropdown'
import IconField from 'primevue/iconfield'
import InputIcon from 'primevue/inputicon'

const selectedItems = ref([])


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
        default: () => ['name', 'description', 'budget']
    },
    dropdownFilter: String,
    dropdownOptions: Array,
    dropdownLabel: String,
    dropdownPlaceholder: String
})

const emit = defineEmits(['add-new', 'edit', 'delete', 'selection-change', 'export'])

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

const exportSelected = () => {
    if (selectedItems.value.length === 0) {
        // Nessuna riga selezionata
        return
    }

    // Crea CSV
    const headers = props.columns.map(col => col.header).join(',')
    const csvData = selectedItems.value.map(item => {
        return props.columns.map(col => {
            const value = item[col.field]
            // Gestisci valori speciali
            if (col.format === 'currency') {
                return new Intl.NumberFormat('it-IT', { style: 'currency', currency: 'EUR' }).format(value)
            }
            if (col.format === 'date') {
                return new Date(value).toLocaleDateString('it-IT')
            }
            return `"${value}"` // Metti tra virgolette per CSV
        }).join(',')
    }).join('\n')

    const csv = `${headers}\n${csvData}`

    // Download
    const blob = new Blob([csv], { type: 'text/csv' })
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = 'dati_selezionati.csv'
    a.click()
    window.URL.revokeObjectURL(url)

    // Emetti evento per il componente padre
    emit('export', selectedItems.value)
}
</script>

<style scoped>
.data-table-wrapper {
    padding: 1rem;
    border-radius: 10px;
    background-color: white;
}
</style>
