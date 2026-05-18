import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login',
      name: 'login',
      component: () => import('@/views/auth/LoginView.vue'),
      meta: { public: true },
    },
    {
      path: '/',
      component: () => import('@/components/layout/AppLayout.vue'),
      meta: { requiresAuth: true },
      children: [
        {
          path: '',
          name: 'dashboard',
          component: () => import('@/views/DashboardView.vue'),
        },
        {
          path: 'branches',
          name: 'branches',
          component: () => import('@/views/branches/BranchesView.vue'),
        },
        {
          path: 'users',
          name: 'users',
          component: () => import('@/views/users/UsersView.vue'),
          meta: { adminOnly: true },
        },
        {
          path: 'products',
          name: 'products',
          component: () => import('@/views/products/ProductsView.vue'),
        },
        {
          path: 'stock',
          name: 'stock',
          component: () => import('@/views/stock/StockView.vue'),
        },
        {
          path: 'sales',
          name: 'sales',
          component: () => import('@/views/sales/SalesView.vue'),
        },
        {
          path: 'stock-requests',
          name: 'stock-requests',
          component: () => import('@/views/stock-requests/StockRequestsView.vue'),
        },
        {
          path: 'chat',
          name: 'chat',
          component: () => import('@/views/chat/ChatView.vue'),
        },
      ],
    },
  ],
})

router.beforeEach(async (to) => {
  const auth = useAuthStore()

  if (!to.meta.public && !auth.isAuthenticated) return '/login'
  if (to.path === '/login' && auth.isAuthenticated) return '/'
  if (to.meta.adminOnly && !auth.isAdmin) return '/'

  if (auth.isAuthenticated && !auth.user) {
    try { await auth.fetchMe() } catch { auth.logout(); return '/login' }
  }
})

export default router