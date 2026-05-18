<template>
  <div class="min-h-screen bg-gray-950 flex items-center justify-center p-4 font-mono">
    <div class="w-full max-w-md">
      <!-- Logo -->
      <div class="text-center mb-10">
        <h1 class="text-4xl font-bold tracking-widest uppercase">
          <span class="text-emerald-400">Stock</span><span class="text-white">flow</span>
        </h1>
        <p class="text-gray-500 text-sm mt-2 tracking-widest">GESTIÓN DE INVENTARIO</p>
      </div>

      <!-- Card -->
      <div class="bg-gray-900 border border-gray-800 rounded-2xl p-8">
        <h2 class="text-white font-semibold text-lg mb-6">Iniciar sesión</h2>

        <form @submit.prevent="handleLogin" class="space-y-4">
          <div>
            <label class="block text-xs text-gray-500 uppercase tracking-widest mb-2">Email</label>
            <input
              v-model="email"
              type="email"
              required
              placeholder="admin@stockflow.com"
              class="w-full bg-gray-800 border border-gray-700 text-white rounded-lg px-4 py-3 text-sm focus:outline-none focus:border-emerald-500 transition-colors placeholder-gray-600"
            />
          </div>

          <div>
            <label class="block text-xs text-gray-500 uppercase tracking-widest mb-2">Contraseña</label>
            <input
              v-model="password"
              type="password"
              required
              placeholder="••••••••"
              class="w-full bg-gray-800 border border-gray-700 text-white rounded-lg px-4 py-3 text-sm focus:outline-none focus:border-emerald-500 transition-colors placeholder-gray-600"
            />
          </div>

          <p v-if="error" class="text-red-400 text-xs">{{ error }}</p>

          <button
            type="submit"
            :disabled="loading"
            class="w-full bg-emerald-500 hover:bg-emerald-400 disabled:opacity-50 text-gray-950 font-bold rounded-lg py-3 text-sm uppercase tracking-widest transition-colors mt-2"
          >
            {{ loading ? 'Ingresando...' : 'Ingresar' }}
          </button>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()
const router = useRouter()

const email = ref('')
const password = ref('')
const loading = ref(false)
const error = ref('')

async function handleLogin() {
  loading.value = true
  error.value = ''
  try {
    await auth.login(email.value, password.value)
    router.push('/')
  } catch {
    error.value = 'Email o contraseña incorrectos'
  } finally {
    loading.value = false
  }
}
</script>