<template>
  <div class="space-y-6">
    <div class="flex items-center justify-between flex-wrap gap-3">
      <h2 class="text-xl font-bold text-white">Ventas</h2>
      <div class="flex gap-3">
        <select v-model="selectedBranch" class="bg-gray-800 border border-gray-700 text-white rounded-lg px-4 py-2 text-sm focus:outline-none focus:border-emerald-500">
          <option v-for="b in branches" :key="b.id" :value="b.id">{{ b.name }}</option>
        </select>
        <button @click="showModal = true" class="bg-emerald-500 hover:bg-emerald-400 text-gray-950 font-bold text-sm px-4 py-2 rounded-lg uppercase tracking-widest transition-colors">+ Nueva Venta</button>
      </div>
    </div>

    <div class="bg-gray-900 border border-gray-800 rounded-xl overflow-hidden">
      <table class="w-full text-sm">
        <thead>
          <tr class="border-b border-gray-800 text-gray-500 uppercase tracking-widest text-xs">
            <th class="text-left px-6 py-4">ID</th>
            <th class="text-left px-6 py-4">Fecha</th>
            <th class="text-left px-6 py-4">Items</th>
            <th class="text-left px-6 py-4">Total</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="loading"><td colspan="4" class="px-6 py-8 text-center text-gray-500">Cargando...</td></tr>
          <tr v-for="sale in sales" :key="sale.id" class="border-b border-gray-800/50 hover:bg-gray-800/30 transition-colors">
            <td class="px-6 py-4 text-gray-500 font-mono text-xs">{{ sale.id.slice(0, 8) }}...</td>
            <td class="px-6 py-4 text-gray-300">{{ formatDate(sale.created_at) }}</td>
            <td class="px-6 py-4 text-gray-400">{{ sale.items.length }} producto(s)</td>
            <td class="px-6 py-4 text-emerald-400 font-mono font-bold">${{ sale.total.toFixed(2) }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Modal nueva venta -->
    <div v-if="showModal" class="fixed inset-0 bg-black/60 flex items-center justify-center z-50 p-4">
      <div class="bg-gray-900 border border-gray-800 rounded-2xl p-6 w-full max-w-lg max-h-[90vh] overflow-y-auto">
        <h3 class="text-white font-semibold mb-5">Nueva Venta</h3>

        <!-- Items -->
        <div class="space-y-3 mb-4">
          <div v-for="(item, i) in saleItems" :key="i" class="flex gap-3 items-end">
            <div class="flex-1">
              <label class="label">Producto</label>
              <select v-model="item.product_id" class="input-field">
                <option value="">— Seleccionar —</option>
                <option v-for="p in products" :key="p.id" :value="p.id">{{ p.name }} (${{ p.price }})</option>
              </select>
            </div>
            <div class="w-24">
              <label class="label">Cant.</label>
              <input v-model.number="item.quantity" type="number" min="1" class="input-field" />
            </div>
            <button @click="saleItems.splice(i, 1)" class="text-red-400 hover:text-red-300 pb-3 text-sm">✕</button>
          </div>
        </div>

        <button @click="saleItems.push({ product_id: '', quantity: 1 })" class="text-emerald-400 hover:text-emerald-300 text-sm transition-colors mb-4">+ Agregar producto</button>

        <p v-if="formError" class="text-red-400 text-xs mb-3">{{ formError }}</p>

        <div class="flex gap-3">
          <button @click="showModal = false; saleItems = [{ product_id: '', quantity: 1 }]" class="flex-1 bg-gray-800 hover:bg-gray-700 text-gray-300 rounded-lg py-2 text-sm transition-colors">Cancelar</button>
          <button @click="createSale" :disabled="saving" class="flex-1 bg-emerald-500 hover:bg-emerald-400 disabled:opacity-50 text-gray-950 font-bold rounded-lg py-2 text-sm transition-colors">
            {{ saving ? 'Procesando...' : 'Confirmar Venta' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { branchesApi, salesApi, productsApi } from '@/api'

const auth = useAuthStore()
const branches = ref([])
const selectedBranch = ref(null)
const sales = ref([])
const products = ref([])
const loading = ref(false)
const showModal = ref(false)
const saving = ref(false)
const formError = ref('')
const saleItems = ref([{ product_id: '', quantity: 1 }])

const formatDate = (d) => new Date(d).toLocaleString('es-PY')

async function load() {
  loading.value = true
  try { sales.value = (await salesApi.byBranch(selectedBranch.value)).data } finally { loading.value = false }
}

async function createSale() {
  const items = saleItems.value.filter((i) => i.product_id && i.quantity > 0)
  if (!items.length) { formError.value = 'Agregá al menos un producto'; return }
  saving.value = true; formError.value = ''
  try {
    await salesApi.create(selectedBranch.value, { items })
    showModal.value = false
    saleItems.value = [{ product_id: '', quantity: 1 }]
    await load()
  } catch (e) {
    formError.value = e.response?.data?.detail || 'Error al procesar la venta'
  } finally { saving.value = false }
}

watch(selectedBranch, load)
onMounted(async () => {
  const [b, p] = await Promise.all([branchesApi.list(), productsApi.list()])
  branches.value = b.data; products.value = p.data
  selectedBranch.value = auth.user?.branch_id || b.data[0]?.id
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