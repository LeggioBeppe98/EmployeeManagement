<template>
  <div class="dashboard">
    <h1>📊 Dashboard</h1>
    <p>Benvenuto, {{ userStore.user?.username }}!</p>
    <div class="welcome-message">
      <h3>Dashboard in costruzione</h3>
      <p>Presto qui troverai metriche e grafici sui dipendenti</p>
    </div>
  </div>
</template>

<script setup>
import { useUserStore } from '../stores/user'

const userStore = useUserStore()
</script>

<style scoped>
.dashboard {
  padding: 2rem;
}

.welcome-message {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  margin-top: 2rem;
  text-align: center;
}
</style>