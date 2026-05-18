<template>
  <div class="space-y-6">
    <div class="flex items-center justify-between">
      <h2 class="text-xl font-bold text-white">Sucursales</h2>
      <button
        v-if="auth.isAdmin"
        @click="openModal()"
        class="bg-emerald-500 hover:bg-emerald-400 text-gray-950 font-bold text-sm px-4 py-2 rounded-lg uppercase tracking-widest transition-colors"
      >+ Nueva</button>
    </div>

    <!-- Table -->
    <div class="bg-gray-900 border border-gray-800 rounded-xl overflow-hidden">
      <table class="w-full text-sm">
        <thead>
          <tr class="border-b border-gray-800 text-gray-500 uppercase tracking-widest text-xs">
            <th class="text-left px-6 py-4">Nombre</th>
            <th class="text-left px-6 py-4">Dirección</th>
            <th v-if="auth.isAdmin" class="px-6 py-4"></th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="loading">
            <td colspan="3" class="px-6 py-8 text-center text-gray-500">Cargando...</td>
          </tr>
          <tr
            v-for="branch in branches"
            :key="branch.id"
            class="border-b border-gray-800/50 hover:bg-gray-800/30 transition-colors"
          >
            <td class="px-6 py-4 font-medium text-white">{{ branch.name }}</td>
            <td class="px-6 py-4 text-gray-400">{{ branch.address || '—' }}</td>
            <td v-if="auth.isAdmin" class="px-6 py-4 text-right space-x-2">
              <button @click="openModal(branch)" class="text-gray-500 hover:text-white text-xs transition-colors">Editar</button>
              <button @click="confirmDelete(branch)" class="text-gray-500 hover:text-red-400 text-xs transition-colors">Eliminar</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Modal -->
    <div v-if="showModal" class="fixed inset-0 bg-black/60 flex items-center justify-center z-50 p-4">
      <div class="bg-gray-900 border border-gray-800 rounded-2xl p-6 w-full max-w-md">
        <h3 class="text-white font-semibold mb-5">{{ editing ? 'Editar' : 'Nueva' }} Sucursal</h3>
        <form @submit.prevent="save" class="space-y-4">
          <div>
            <label class="block text-xs text-gray-500 uppercase tracking-widest mb-2">Nombre</label>
            <input v-model="form.name" required class="input-field" placeholder="Sucursal Centro" />
          </div>
          <div>
            <label class="block text-xs text-gray-500 uppercase tracking-widest mb-2">Dirección</label>
            <input v-model="form.address" class="input-field" placeholder="Av. Principal 123" />
          </div>
          <p v-if="formError" class="text-red-400 text-xs">{{ formError }}</p>
          <div class="flex gap-3 pt-2">
            <button type="button" @click="showModal = false" class="flex-1 bg-gray-800 hover:bg-gray-700 text-gray-300 rounded-lg py-2 text-sm transition-colors">Cancelar</button>
            <button type="submit" :disabled="saving" class="flex-1 bg-emerald-500 hover:bg-emerald-400 disabled:opacity-50 text-gray-950 font-bold rounded-lg py-2 text-sm transition-colors">
              {{ saving ? 'Guardando...' : 'Guardar' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { branchesApi } from '@/api'

const auth = useAuthStore()
const branches = ref([])
const loading = ref(true)
const showModal = ref(false)
const editing = ref(null)
const saving = ref(false)
const formError = ref('')
const form = ref({ name: '', address: '' })

async function load() {
  loading.value = true
  try { branches.value = (await branchesApi.list()).data } finally { loading.value = false }
}

function openModal(branch = null) {
  editing.value = branch
  form.value = { name: branch?.name || '', address: branch?.address || '' }
  formError.value = ''
  showModal.value = true
}

async function save() {
  saving.value = true
  formError.value = ''
  try {
    if (editing.value) await branchesApi.update(editing.value.id, form.value)
    else await branchesApi.create(form.value)
    showModal.value = false
    await load()
  } catch { formError.value = 'Error al guardar' } finally { saving.value = false }
}

async function confirmDelete(branch) {
  if (!confirm(`¿Eliminar "${branch.name}"?`)) return
  try { await branchesApi.delete(branch.id); await load() } catch { alert('Error al eliminar') }
}

onMounted(load)
</script>

<style scoped>
@reference "@/assets/main.css";

.input-field {
  @apply w-full bg-gray-800 border border-gray-700 text-white rounded-lg px-4 py-3 text-sm focus:outline-none focus:border-emerald-500 transition-colors;
}
.label {
  @apply block text-xs text-gray-500 uppercase tracking-widest mb-2;
}
</style>