import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { useUserStore } from './stores/user'

// PRIMEVUE IMPORTS
import PrimeVue from 'primevue/config'
import Aura from '@primevue/themes/aura'
import 'primeicons/primeicons.css'  

import App from './App.vue'
import router from './router'


const app = createApp(App)

app.use(createPinia())

const userStore = useUserStore()
userStore.setupAxiosInterceptors(userStore)

app.use(PrimeVue, {
    theme: {
        preset: Aura
    },
    ripple: true  // Effetti di click
})

app.use(router)

app.mount('#app')
