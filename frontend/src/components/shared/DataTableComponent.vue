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
                <div class="flex justify-content-end align-items-center gap-3">

                    <IconField>
                        <InputIcon class="pi pi-search" />
                        <InputText v-model="filters.search" placeholder="Cerca" />
                    </IconField>

                    <Button label="Nuovo" icon="pi pi-plus" @click="$emit('add-new')" />

                </div>
            </div>
        </div>

        <!-- DATATABLE -->
        <DataTable :value="filteredData" :loading="loading" :paginator="true" :rows="10"
            class="p-datatable-sm"
            paginatorTemplate="FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink "
            currentPageReportTemplate="Mostrando {first} a {last} di {totalRecords} record">

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

                        <Button @click="$emit('delete', slotProps.data)" icon="pi pi-trash" severity="danger" outlined
                            rounded />

                    </div>
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
import IconField from 'primevue/iconfield';
import InputIcon from 'primevue/inputicon';


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
.data-table-wrapper {
    padding: 1rem;
    border-radius: 10px;
    background-color: white;
}


</style>
