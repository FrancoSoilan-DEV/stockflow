<template>
  <div class="space-y-6">
    <!-- Bienvenida -->
    <div>
      <h2 class="text-2xl font-bold text-white">
        Bienvenido, <span class="text-emerald-400">{{ auth.user?.username }}</span>
      </h2>
      <p class="text-gray-500 text-sm mt-1">{{ auth.user?.role === 'admin' ? 'Administrador' : 'Staff' }} · Sucursal {{ auth.user?.branch_id }}</p>
    </div>

    <!-- Stats cards -->
    <div class="grid grid-cols-2 lg:grid-cols-4 gap-4">
      <StatCard label="Sucursales" :value="stats.branches" icon="🏪" color="emerald" />
      <StatCard label="Productos" :value="stats.products" icon="📦" color="blue" />
      <StatCard label="Usuarios" :value="stats.users" icon="👥" color="purple" />
      <StatCard label="Pedidos pendientes" :value="stats.pendingRequests" icon="🔄" color="yellow" />
    </div>

    <!-- Quick access -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
      <div class="bg-gray-900 border border-gray-800 rounded-xl p-5">
        <h3 class="text-sm font-semibold text-gray-400 uppercase tracking-widest mb-4">Acceso rápido</h3>
        <div class="grid grid-cols-2 gap-3">
          <RouterLink
            v-for="item in quickLinks"
            :key="item.to"
            :to="item.to"
            class="flex items-center gap-3 bg-gray-800 hover:bg-gray-700 rounded-lg p-3 transition-colors"
          >
            <span class="text-xl">{{ item.icon }}</span>
            <span class="text-sm text-gray-300">{{ item.label }}</span>
          </RouterLink>
        </div>
      </div>

      <div class="bg-gray-900 border border-gray-800 rounded-xl p-5">
        <h3 class="text-sm font-semibold text-gray-400 uppercase tracking-widest mb-4">Tu cuenta</h3>
        <div class="space-y-3 text-sm">
          <div class="flex justify-between">
            <span class="text-gray-500">Usuario</span>
            <span class="text-white">{{ auth.user?.username }}</span>
          </div>
          <div class="flex justify-between">
            <span class="text-gray-500">Email</span>
            <span class="text-white">{{ auth.user?.email }}</span>
          </div>
          <div class="flex justify-between">
            <span class="text-gray-500">Rol</span>
            <span class="capitalize text-emerald-400">{{ auth.user?.role }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { branchesApi, productsApi, usersApi, stockRequestsApi } from '@/api'
import StatCard from '@/components/StatCard.vue'

const auth = useAuthStore()

const stats = ref({ branches: '—', products: '—', users: '—', pendingRequests: '—' })

const quickLinks = [
  { to: '/stock', label: 'Ver Stock', icon: '🗃' },
  { to: '/sales', label: 'Nueva Venta', icon: '🧾' },
  { to: '/stock-requests', label: 'Pedidos', icon: '🔄' },
  { to: '/chat', label: 'Chat', icon: '💬' },
]

onMounted(async () => {
  try {
    const [b, p, u] = await Promise.all([
      branchesApi.list(),
      productsApi.list(),
      usersApi.list(),
    ])
    stats.value.branches = b.data.length
    stats.value.products = p.data.length
    stats.value.users = u.data.length

    if (auth.isAdmin) {
      const r = await stockRequestsApi.list()
      stats.value.pendingRequests = r.data.filter((x) => x.status === 'pending').length
    } else {
      const r = await stockRequestsApi.byBranch(auth.user.branch_id)
      stats.value.pendingRequests = r.data.filter((x) => x.status === 'pending').length
    }
  } catch (e) {
    console.error(e)
  }
})
</script>