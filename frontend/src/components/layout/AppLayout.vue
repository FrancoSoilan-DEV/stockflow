<template>
  <div class="flex h-screen bg-gray-950 text-gray-100 font-mono overflow-hidden">
    <!-- Sidebar -->
    <aside
      class="w-64 bg-gray-900 border-r border-gray-800 flex flex-col shrink-0"
    >
      <!-- Logo -->
      <div class="h-16 flex items-center px-6 border-b border-gray-800">
        <span class="text-emerald-400 font-bold text-xl tracking-widest uppercase">Stock</span>
        <span class="text-white font-bold text-xl tracking-widest uppercase">flow</span>
      </div>

      <!-- Nav -->
      <nav class="flex-1 px-3 py-4 space-y-1 overflow-y-auto">
        <RouterLink
          v-for="item in navItems"
          :key="item.to"
          :to="item.to"
          class="flex items-center gap-3 px-3 py-2 rounded-lg text-sm text-gray-400 hover:text-white hover:bg-gray-800 transition-all"
          active-class="bg-emerald-500/10 text-emerald-400 border border-emerald-500/20"
        >
          <span class="text-lg">{{ item.icon }}</span>
          {{ item.label }}
        </RouterLink>
      </nav>

      <!-- User info -->
      <div class="border-t border-gray-800 p-4">
        <div class="flex items-center gap-3">
          <div class="w-8 h-8 rounded-full bg-emerald-500/20 flex items-center justify-center text-emerald-400 text-sm font-bold">
            {{ userInitial }}
          </div>
          <div class="flex-1 min-w-0">
            <p class="text-sm font-medium text-white truncate">{{ auth.user?.username }}</p>
            <p class="text-xs text-gray-500 capitalize">{{ auth.user?.role }}</p>
          </div>
          <button
            @click="auth.logout(); $router.push('/login')"
            class="text-gray-500 hover:text-red-400 transition-colors text-sm"
            title="Salir"
          >⏻</button>
        </div>
      </div>
    </aside>

    <!-- Main content -->
    <main class="flex-1 flex flex-col overflow-hidden">
      <!-- Topbar -->
      <header class="h-16 bg-gray-900 border-b border-gray-800 flex items-center px-6 shrink-0">
        <h1 class="text-sm font-medium text-gray-400 uppercase tracking-widest">
          {{ currentTitle }}
        </h1>
        <!-- Online indicator -->
        <div class="ml-auto flex items-center gap-2 text-xs text-gray-500">
          <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
          En línea
        </div>
      </header>

      <div class="flex-1 overflow-y-auto p-6">
        <RouterView />
      </div>
    </main>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()
const route = useRoute()

const allNavItems = [
  { to: '/', label: 'Dashboard', icon: '▦', adminOnly: false },
  { to: '/branches', label: 'Sucursales', icon: '🏪', adminOnly: false },
  { to: '/users', label: 'Usuarios', icon: '👥', adminOnly: true },
  { to: '/products', label: 'Productos', icon: '📦', adminOnly: false },
  { to: '/stock', label: 'Stock', icon: '🗃', adminOnly: false },
  { to: '/sales', label: 'Ventas', icon: '🧾', adminOnly: false },
  { to: '/stock-requests', label: 'Pedidos', icon: '🔄', adminOnly: false },
  { to: '/chat', label: 'Chat', icon: '💬', adminOnly: false },
]

const navItems = computed(() =>
  allNavItems.filter((i) => !i.adminOnly || auth.isAdmin),
)

const titles = {
  dashboard: 'Dashboard',
  branches: 'Sucursales',
  users: 'Usuarios',
  products: 'Productos',
  stock: 'Stock',
  sales: 'Ventas',
  'stock-requests': 'Pedidos de Stock',
  chat: 'Chat',
}

const currentTitle = computed(() => titles[route.name] || 'Stockflow')
const userInitial = computed(() => auth.user?.username?.[0]?.toUpperCase() || '?')
</script>