// frontend/src/main.js
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import PrimeVue from 'primevue/config'
import './assets/tailwind.css'

// ⭐ Import Preset (Tema)
import Lara from '@primevue/themes/lara';

// ⭐ Icone (obbligatorie)
import 'primeicons/primeicons.css';

import App from './App.vue'
import router from './router'

const app = createApp(App);

app.use(createPinia());
app.use(PrimeVue, {
    theme: {
        preset: Lara,
        options: {
        }
    },
    ripple: true
});

app.use(router);
app.mount('#app');
