<template>
  <div class="space-y-6">
    <div class="flex items-center justify-between flex-wrap gap-3">
      <h2 class="text-xl font-bold text-white">Stock</h2>
      <select v-model="selectedBranch" class="bg-gray-800 border border-gray-700 text-white rounded-lg px-4 py-2 text-sm focus:outline-none focus:border-emerald-500">
        <option v-for="b in branches" :key="b.id" :value="b.id">{{ b.name }}</option>
      </select>
    </div>

    <div class="bg-gray-900 border border-gray-800 rounded-xl overflow-hidden">
      <table class="w-full text-sm">
        <thead>
          <tr class="border-b border-gray-800 text-gray-500 uppercase tracking-widest text-xs">
            <th class="text-left px-6 py-4">Producto</th>
            <th class="text-left px-6 py-4">Categoría</th>
            <th class="text-left px-6 py-4">Cantidad</th>
            <th class="px-6 py-4"></th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="loading"><td colspan="4" class="px-6 py-8 text-center text-gray-500">Cargando...</td></tr>
          <tr v-for="item in stock" :key="item.id" class="border-b border-gray-800/50 hover:bg-gray-800/30 transition-colors">
            <td class="px-6 py-4">
              <p class="font-medium text-white">{{ item.product.name }}</p>
              <p class="text-gray-500 text-xs">${{ item.product.price.toFixed(2) }}</p>
            </td>
            <td class="px-6 py-4">
              <span class="text-xs bg-gray-800 text-gray-300 px-2 py-1 rounded-full">{{ item.product.category || '—' }}</span>
            </td>
            <td class="px-6 py-4">
              <span class="font-mono font-bold text-lg" :class="item.quantity === 0 ? 'text-red-400' : item.quantity < 5 ? 'text-yellow-400' : 'text-emerald-400'">
                {{ item.quantity }}
              </span>
            </td>
            <td class="px-6 py-4 text-right">
              <button @click="openEdit(item)" class="text-gray-500 hover:text-white text-xs transition-colors">Ajustar</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Modal ajuste -->
    <div v-if="editItem" class="fixed inset-0 bg-black/60 flex items-center justify-center z-50 p-4">
      <div class="bg-gray-900 border border-gray-800 rounded-2xl p-6 w-full max-w-sm">
        <h3 class="text-white font-semibold mb-1">Ajustar Stock</h3>
        <p class="text-gray-500 text-sm mb-5">{{ editItem.product.name }}</p>
        <div>
          <label class="block text-xs text-gray-500 uppercase tracking-widest mb-2">Nueva cantidad</label>
          <input v-model.number="newQty" type="number" min="0" class="w-full bg-gray-800 border border-gray-700 text-white rounded-lg px-4 py-3 text-sm focus:outline-none focus:border-emerald-500" />
        </div>
        <div class="flex gap-3 mt-4">
          <button @click="editItem = null" class="flex-1 bg-gray-800 hover:bg-gray-700 text-gray-300 rounded-lg py-2 text-sm transition-colors">Cancelar</button>
          <button @click="saveStock" :disabled="saving" class="flex-1 bg-emerald-500 hover:bg-emerald-400 disabled:opacity-50 text-gray-950 font-bold rounded-lg py-2 text-sm transition-colors">
            {{ saving ? 'Guardando...' : 'Guardar' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { branchesApi, stockApi } from '@/api'

const auth = useAuthStore()
const branches = ref([])
const selectedBranch = ref(null)
const stock = ref([])
const loading = ref(false)
const editItem = ref(null)
const newQty = ref(0)
const saving = ref(false)

async function loadBranches() {
  const res = await branchesApi.list()
  branches.value = res.data
  selectedBranch.value = auth.user?.branch_id || res.data[0]?.id
}

async function loadStock() {
  if (!selectedBranch.value) return
  loading.value = true
  try { stock.value = (await stockApi.byBranch(selectedBranch.value)).data } finally { loading.value = false }
}

function openEdit(item) {
  editItem.value = item
  newQty.value = item.quantity
}

async function saveStock() {
  saving.value = true
  try {
    await stockApi.update(selectedBranch.value, editItem.value.product_id, { quantity: newQty.value })
    editItem.value = null
    await loadStock()
  } finally { saving.value = false }
}

watch(selectedBranch, loadStock)
onMounted(async () => { await loadBranches() })
</script>