<template>
  <div id="app">
    <nav class="navbar" v-if="userStore.isAuthenticated">
      <div class="navbar-brand">
        <h1>🏢 Employee Dashboard</h1>
      </div>
      <div class="navbar-user" v-if="userStore.isAuthenticated">
        <span>Ciao, {{ userStore.user?.username }}</span>
        <button @click="userStore.logout">Logout</button>
      </div>
    </nav>

    <div class="app-container" v-if="userStore.isAuthenticated">
      <aside class="sidebar" v-if="userStore.isAuthenticated">
        <nav class="sidebar-nav">
          <router-link to="/dashboard" class="nav-item">📊 Dashboard</router-link>
          <router-link to="/employees" class="nav-item">👥 Dipendenti</router-link>
          <router-link to="/departments" class="nav-item">🏢 Dipartimenti</router-link>
        </nav>
      </aside>

      <main class="main-content">
        <router-view />
      </main>
    </div>

    <!-- Mostra le pagine pubbliche (login) se non autenticato -->
    <router-view v-else />

  </div>
</template>

<script setup>
import { useUserStore } from './stores/user'

const userStore = useUserStore()
</script>

<style>
:root {
  /* Primari */
  --color-primary: #2660A4;
  --color-primary-dark: #1C4778;
  --color-primary-light: #4B86C8;

  /* Secondario */
  --color-secondary: #E86A33;

    /* Terziario */
  --color-third: #3a93f9;

  /*MAin background */
    --color-main-background:#f1f5f9;

  /* Sfondi & Testo */
  --color-background-light: #F9F9F9;
  --color-background-dark: #333333;
  --color-text-dark: #1A1A1A;
  --color-text-light: #FFFFFF;

  /* Sistema/Stati */
  --color-success: #4CAF50;
  --color-warning: #FFC107;
  --color-error: #F44336;
  --color-border: #CCCCCC;
}


* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.navbar {
  background: var(--color-primary-dark);
  color: white;
  padding: 1rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.app-container {
  display: flex;
  min-height: calc(100vh - 60px);
}

.sidebar {
  width: 250px;
  background: var(--color-primary-light);
  padding: 1rem;
}

.sidebar-nav {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.nav-item {
  color: white;
  text-decoration: none;
  padding: 0.75rem 1rem;
  border-radius: 4px;
  transition: background 0.3s;
}

.nav-item:hover,
.nav-item.router-link-active {
  background: var(--color-third);
}

.main-content {
  flex: 1;
  padding: 2rem;
  background: var(--color-main-background);
}
</style>