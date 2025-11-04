<template>
  <div class="dashboard">
    <div class="dashboard-header">
      <h1>📊 Dashboard</h1>
      <p>Panoramica completa del personale aziendale</p>
    </div>

    <!-- Loading State -->
    <div v-if="dashboardStore.isLoading" class="loading">
      <p>Caricamento dati in corso...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="dashboardStore.error" class="error">
      <p>{{ dashboardStore.error }}</p>
      <button @click="loadData" class="retry-button">Riprova</button>
    </div>

    <!-- Main Content -->
    <div v-else class="dashboard-content">
      
      <!-- Metric Cards -->
      <div class="metrics-grid">
        <div class="metric-card">
          <div class="metric-icon">👥</div>
          <div class="metric-info">
            <h3>Dipendenti Totali</h3>
            <p class="metric-value">{{ dashboardStore.stats.totalEmployees }}</p>
          </div>
        </div>

        <div class="metric-card">
          <div class="metric-icon">✅</div>
          <div class="metric-info">
            <h3>Dipendenti Attivi</h3>
            <p class="metric-value">{{ dashboardStore.stats.activeEmployees }}</p>
          </div>
        </div>

        <div class="metric-card">
          <div class="metric-icon">💰</div>
          <div class="metric-info">
            <h3>Stipendio Medio</h3>
            <p class="metric-value">€{{ formatCurrency(dashboardStore.stats.averageSalary) }}</p>
          </div>
        </div>

        <div class="metric-card">
          <div class="metric-icon">🏢</div>
          <div class="metric-info">
            <h3>Dipartimenti</h3>
            <p class="metric-value">{{ dashboardStore.stats.totalDepartments }}</p>
          </div>
        </div>
      </div>

      <!-- Charts Section -->
      <div class="charts-section">
        <div class="chart-container">
          <h3>Distribuzione per Dipartimento</h3>
          <div class="chart-placeholder">
            <p>📊 Grafico dipartimenti (Chart.js coming soon)</p>
            <div class="distribution-list">
              <div v-for="dept in dashboardStore.departmentDistribution" 
                   :key="dept.name" 
                   class="distribution-item">
                <span class="dept-name">{{ dept.name }}</span>
                <span class="dept-count">{{ dept.employee_count }} dipendenti</span>
              </div>
            </div>
          </div>
        </div>

        <div class="chart-container">
          <h3>Distribuzione Stipendi</h3>
          <div class="chart-placeholder">
            <p>📈 Grafico stipendi (Chart.js coming soon)</p>
            <div class="distribution-list">
              <div v-for="salary in dashboardStore.salaryDistribution" 
                   :key="salary.range" 
                   class="distribution-item">
                <span class="salary-range">{{ salary.range }}</span>
                <span class="salary-count">{{ salary.count }} dipendenti</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Recent Hires -->
      <div class="recent-hires">
        <h3>Ultime Assunzioni</h3>
        <div class="hires-list">
          <div v-for="hire in dashboardStore.recentHires" 
               :key="hire.id" 
               class="hire-item">
            <div class="hire-info">
              <strong>{{ hire.first_name }} {{ hire.last_name }}</strong>
              <span>{{ hire.position }}</span>
            </div>
            <div class="hire-details">
              <span class="dept-badge">{{ hire.department__name }}</span>
              <span class="hire-date">{{ formatDate(hire.hire_date) }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useDashboardStore } from '../stores/dashboard'

const dashboardStore = useDashboardStore()

const loadData = () => {
  dashboardStore.fetchDashboardData()
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

// Carica i dati quando il componente viene montato
onMounted(() => {
  loadData()
})
</script>

<style scoped>
.dashboard {
  padding: 1rem;
}

.dashboard-header {
  margin-bottom: 2rem;
}

.dashboard-header h1 {
  color: #2c3e50;
  margin-bottom: 0.5rem;
}

.dashboard-header p {
  color: #7f8c8d;
  font-size: 1.1rem;
}

/* Metrics Grid */
.metrics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 3rem;
}

.metric-card {
  background: white;
  padding: 1.5rem;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  display: flex;
  align-items: center;
  gap: 1rem;
  transition: transform 0.2s;
}

.metric-card:hover {
  transform: translateY(-2px);
}

.metric-icon {
  font-size: 2rem;
}

.metric-info h3 {
  margin: 0 0 0.5rem 0;
  color: #7f8c8d;
  font-size: 0.9rem;
  font-weight: 500;
}

.metric-value {
  margin: 0;
  font-size: 2rem;
  font-weight: bold;
  color: #2c3e50;
}

/* Charts Section */
.charts-section {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
  margin-bottom: 3rem;
}

.chart-container {
  background: white;
  padding: 1.5rem;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.chart-container h3 {
  margin: 0 0 1rem 0;
  color: #2c3e50;
}

.chart-placeholder {
  text-align: center;
  color: #7f8c8d;
  padding: 2rem;
}

.distribution-list {
  margin-top: 1rem;
}

.distribution-item {
  display: flex;
  justify-content: space-between;
  padding: 0.5rem 0;
  border-bottom: 1px solid #ecf0f1;
}

.distribution-item:last-child {
  border-bottom: none;
}

/* Recent Hires */
.recent-hires {
  background: white;
  padding: 1.5rem;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.recent-hires h3 {
  margin: 0 0 1rem 0;
  color: #2c3e50;
}

.hires-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.hire-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 8px;
}

.hire-info {
  display: flex;
  flex-direction: column;
}

.hire-details {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.dept-badge {
  background: #3498db;
  color: white;
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.8rem;
}

.hire-date {
  color: #7f8c8d;
  font-size: 0.9rem;
}

/* Loading and Error States */
.loading, .error {
  text-align: center;
  padding: 3rem;
  background: white;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.retry-button {
  background: #3498db;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 5px;
  cursor: pointer;
  margin-top: 1rem;
}

.retry-button:hover {
  background: #2980b9;
}
</style>