import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '../stores/user'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      redirect: '/dashboard'
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/Login.vue')
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: () => import('../views/Dashboard.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/employees',
      name: 'employees', 
      component: () => import('../views/Employees.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/departments',
      name: 'departments',
      component: () => import('../views/Departments.vue'),
      meta: { requiresAuth: true }
    }
  ]
})

// ROUTE GUARD - Protegge le pagine
router.beforeEach((to, from, next) => {
  const userStore = useUserStore()
  
  if (to.meta.requiresAuth && !userStore.isAuthenticated) {
    next({ name: 'login' })
  } else if (to.name === 'login' && userStore.isAuthenticated) {
    next({ name: 'dashboard' }) // Se già loggato, vai alla dashboard
  } else {
    next()
  }
})

export default router