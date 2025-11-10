import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { useUserStore } from './stores/user'

import App from './App.vue'
import router from './router'

const app = createApp(App)

app.use(createPinia())

const userStore = useUserStore()
userStore.setupAxiosInterceptors(userStore)

app.use(router)

app.mount('#app')
