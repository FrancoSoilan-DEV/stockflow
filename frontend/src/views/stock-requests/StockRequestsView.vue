<template>
  <div class="space-y-6">
    <div class="flex items-center justify-between">
      <h2 class="text-xl font-bold text-white">Pedidos de Stock</h2>
      <button @click="openModal()" class="bg-emerald-500 hover:bg-emerald-400 text-gray-950 font-bold text-sm px-4 py-2 rounded-lg uppercase tracking-widest transition-colors">+ Nuevo Pedido</button>
    </div>

    <!-- Filtro status -->
    <div class="flex gap-2">
      <button v-for="s in statuses" :key="s" @click="filterStatus = s"
        class="text-xs px-3 py-1.5 rounded-full border transition-colors capitalize"
        :class="filterStatus === s ? 'bg-emerald-500 border-emerald-500 text-gray-950 font-bold' : 'border-gray-700 text-gray-400 hover:border-gray-500'">
        {{ s }}
      </button>
    </div>

    <div class="bg-gray-900 border border-gray-800 rounded-xl overflow-hidden">
      <table class="w-full text-sm">
        <thead>
          <tr class="border-b border-gray-800 text-gray-500 uppercase tracking-widest text-xs">
            <th class="text-left px-6 py-4">Producto</th>
            <th class="text-left px-6 py-4">Desde → Hacia</th>
            <th class="text-left px-6 py-4">Cant.</th>
            <th class="text-left px-6 py-4">Estado</th>
            <th v-if="auth.isAdmin" class="px-6 py-4"></th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="loading"><td colspan="5" class="px-6 py-8 text-center text-gray-500">Cargando...</td></tr>
          <tr v-for="req in filtered" :key="req.id" class="border-b border-gray-800/50 hover:bg-gray-800/30 transition-colors">
            <td class="px-6 py-4 font-medium text-white">{{ req.product.name }}</td>
            <td class="px-6 py-4 text-gray-400 text-xs font-mono">
              {{ branchName(req.from_branch_id) }} → {{ branchName(req.to_branch_id) }}
            </td>
            <td class="px-6 py-4 text-white font-mono">{{ req.quantity }}</td>
            <td class="px-6 py-4">
              <span class="text-xs px-2 py-1 rounded-full capitalize" :class="statusClass(req.status)">{{ req.status }}</span>
            </td>
            <td v-if="auth.isAdmin && req.status === 'pending'" class="px-6 py-4 text-right space-x-2">
              <button @click="updateStatus(req.id, 'approved')" class="text-emerald-400 hover:text-emerald-300 text-xs transition-colors">Aprobar</button>
              <button @click="updateStatus(req.id, 'rejected')" class="text-red-400 hover:text-red-300 text-xs transition-colors">Rechazar</button>
            </td>
            <td v-else-if="auth.isAdmin" class="px-6 py-4"></td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Modal -->
    <div v-if="showModal" class="fixed inset-0 bg-black/60 flex items-center justify-center z-50 p-4">
      <div class="bg-gray-900 border border-gray-800 rounded-2xl p-6 w-full max-w-md">
        <h3 class="text-white font-semibold mb-5">Nuevo Pedido de Stock</h3>
        <form @submit.prevent="save" class="space-y-4">
          <div>
            <label class="label">Sucursal destino</label>
            <select v-model="form.to_branch_id" required class="input-field">
              <option value="">— Seleccionar —</option>
              <option v-for="b in branches" :key="b.id" :value="b.id" :disabled="b.id === auth.user?.branch_id">{{ b.name }}</option>
            </select>
          </div>
          <div>
            <label class="label">Producto</label>
            <select v-model="form.product_id" required class="input-field">
              <option value="">— Seleccionar —</option>
              <option v-for="p in products" :key="p.id" :value="p.id">{{ p.name }}</option>
            </select>
          </div>
          <div>
            <label class="label">Cantidad</label>
            <input v-model.number="form.quantity" type="number" min="1" required class="input-field" />
          </div>
          <p v-if="formError" class="text-red-400 text-xs">{{ formError }}</p>
          <div class="flex gap-3 pt-2">
            <button type="button" @click="showModal = false" class="flex-1 bg-gray-800 hover:bg-gray-700 text-gray-300 rounded-lg py-2 text-sm transition-colors">Cancelar</button>
            <button type="submit" :disabled="saving" class="flex-1 bg-emerald-500 hover:bg-emerald-400 disabled:opacity-50 text-gray-950 font-bold rounded-lg py-2 text-sm transition-colors">
              {{ saving ? 'Enviando...' : 'Enviar Pedido' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { stockRequestsApi, branchesApi, productsApi } from '@/api'

const auth = useAuthStore()
const requests = ref([])
const branches = ref([])
const products = ref([])
const loading = ref(true)
const showModal = ref(false)
const saving = ref(false)
const formError = ref('')
const filterStatus = ref('todos')
const form = ref({ to_branch_id: '', product_id: '', quantity: 1 })

const statuses = ['todos', 'pending', 'approved', 'rejected']
const filtered = computed(() =>
  filterStatus.value === 'todos' ? requests.value : requests.value.filter((r) => r.status === filterStatus.value)
)
const branchName = (id) => branches.value.find((b) => b.id === id)?.name || id?.slice(0, 8)
const statusClass = (s) => ({ pending: 'bg-yellow-500/10 text-yellow-400', approved: 'bg-emerald-500/10 text-emerald-400', rejected: 'bg-red-500/10 text-red-400' }[s])

async function load() {
  loading.value = true
  try {
    const res = auth.isAdmin ? await stockRequestsApi.list() : await stockRequestsApi.byBranch(auth.user.branch_id)
    requests.value = res.data
  } finally { loading.value = false }
}

function openModal() { form.value = { to_branch_id: '', product_id: '', quantity: 1 }; formError.value = ''; showModal.value = true }

async function save() {
  saving.value = true; formError.value = ''
  try {
    await stockRequestsApi.create(form.value)
    showModal.value = false; await load()
  } catch (e) { formError.value = e.response?.data?.detail || 'Error al enviar' } finally { saving.value = false }
}

async function updateStatus(id, status) {
  try { await stockRequestsApi.updateStatus(id, { status }); await load() } catch { alert('Error') }
}

onMounted(async () => {
  const [b, p] = await Promise.all([branchesApi.list(), productsApi.list()])
  branches.value = b.data; products.value = p.data; await load()
})
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