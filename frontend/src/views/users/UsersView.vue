<template>
  <div class="space-y-6">
    <div class="flex items-center justify-between">
      <h2 class="text-xl font-bold text-white">Usuarios</h2>
      <button @click="openModal()" class="bg-emerald-500 hover:bg-emerald-400 text-gray-950 font-bold text-sm px-4 py-2 rounded-lg uppercase tracking-widest transition-colors">+ Nuevo</button>
    </div>

    <div class="bg-gray-900 border border-gray-800 rounded-xl overflow-hidden">
      <table class="w-full text-sm">
        <thead>
          <tr class="border-b border-gray-800 text-gray-500 uppercase tracking-widest text-xs">
            <th class="text-left px-6 py-4">Usuario</th>
            <th class="text-left px-6 py-4">Email</th>
            <th class="text-left px-6 py-4">Rol</th>
            <th class="text-left px-6 py-4">Sucursal</th>
            <th class="px-6 py-4"></th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="loading"><td colspan="5" class="px-6 py-8 text-center text-gray-500">Cargando...</td></tr>
          <tr v-for="user in users" :key="user.id" class="border-b border-gray-800/50 hover:bg-gray-800/30 transition-colors">
            <td class="px-6 py-4 font-medium text-white">{{ user.username }}</td>
            <td class="px-6 py-4 text-gray-400">{{ user.email }}</td>
            <td class="px-6 py-4">
              <span class="text-xs px-2 py-1 rounded-full capitalize"
                :class="user.role === 'admin' ? 'bg-emerald-500/10 text-emerald-400' : 'bg-gray-700 text-gray-300'">
                {{ user.role }}
              </span>
            </td>
            <td class="px-6 py-4 text-gray-400 text-xs font-mono">{{ branchName(user.branch_id) }}</td>
            <td class="px-6 py-4 text-right space-x-2">
              <button @click="openModal(user)" class="text-gray-500 hover:text-white text-xs transition-colors">Editar</button>
              <button @click="confirmDelete(user)" class="text-gray-500 hover:text-red-400 text-xs transition-colors">Eliminar</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Modal -->
    <div v-if="showModal" class="fixed inset-0 bg-black/60 flex items-center justify-center z-50 p-4">
      <div class="bg-gray-900 border border-gray-800 rounded-2xl p-6 w-full max-w-md">
        <h3 class="text-white font-semibold mb-5">{{ editing ? 'Editar' : 'Nuevo' }} Usuario</h3>
        <form @submit.prevent="save" class="space-y-4">
          <div>
            <label class="label">Username</label>
            <input v-model="form.username" :required="!editing" class="input-field" />
          </div>
          <div>
            <label class="label">Email</label>
            <input v-model="form.email" type="email" :required="!editing" class="input-field" />
          </div>
          <div>
            <label class="label">Contraseña {{ editing ? '(dejar vacío para no cambiar)' : '' }}</label>
            <input v-model="form.password" type="password" :required="!editing" class="input-field" />
          </div>
          <div>
            <label class="label">Rol</label>
            <select v-model="form.role" class="input-field">
              <option value="staff">Staff</option>
              <option value="admin">Admin</option>
            </select>
          </div>
          <div>
            <label class="label">Sucursal</label>
            <select v-model="form.branch_id" :required="!editing" class="input-field">
              <option v-for="b in branches" :key="b.id" :value="b.id">{{ b.name }}</option>
            </select>
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
import { usersApi, branchesApi } from '@/api'

const users = ref([])
const branches = ref([])
const loading = ref(true)
const showModal = ref(false)
const editing = ref(null)
const saving = ref(false)
const formError = ref('')
const form = ref({ username: '', email: '', password: '', role: 'staff', branch_id: '' })

const branchName = (id) => branches.value.find((b) => b.id === id)?.name || id?.slice(0, 8)

async function load() {
  loading.value = true
  try {
    const [u, b] = await Promise.all([usersApi.list(), branchesApi.list()])
    users.value = u.data; branches.value = b.data
  } finally { loading.value = false }
}

function openModal(user = null) {
  editing.value = user
  form.value = { username: user?.username || '', email: user?.email || '', password: '', role: user?.role || 'staff', branch_id: user?.branch_id || '' }
  formError.value = ''; showModal.value = true
}

async function save() {
  saving.value = true
  try {
    const payload = { ...form.value }
    if (!payload.password) delete payload.password
    if (editing.value) await usersApi.update(editing.value.id, payload)
    else await usersApi.create(payload)
    showModal.value = false; await load()
  } catch (e) {
    formError.value = e.response?.data?.detail || 'Error al guardar'
  } finally { saving.value = false }
}

async function confirmDelete(user) {
  if (!confirm(`¿Eliminar usuario "${user.username}"?`)) return
  try { await usersApi.delete(user.id); await load() } catch { alert('Error al eliminar') }
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