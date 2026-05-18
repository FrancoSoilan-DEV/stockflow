<template>
  <div class="space-y-6">
    <div class="flex items-center justify-between">
      <h2 class="text-xl font-bold text-white">Productos</h2>
      <button
        v-if="auth.isAdmin"
        @click="openModal()"
        class="bg-emerald-500 hover:bg-emerald-400 text-gray-950 font-bold text-sm px-4 py-2 rounded-lg uppercase tracking-widest transition-colors"
      >+ Nuevo</button>
    </div>

    <!-- Filtro categoría -->
    <div class="flex gap-2 flex-wrap">
      <button
        v-for="cat in categories"
        :key="cat"
        @click="filterCat = cat"
        class="text-xs px-3 py-1.5 rounded-full border transition-colors"
        :class="filterCat === cat ? 'bg-emerald-500 border-emerald-500 text-gray-950 font-bold' : 'border-gray-700 text-gray-400 hover:border-gray-500'"
      >{{ cat }}</button>
    </div>

    <div class="bg-gray-900 border border-gray-800 rounded-xl overflow-hidden">
      <table class="w-full text-sm">
        <thead>
          <tr class="border-b border-gray-800 text-gray-500 uppercase tracking-widest text-xs">
            <th class="text-left px-6 py-4">Nombre</th>
            <th class="text-left px-6 py-4">Categoría</th>
            <th class="text-left px-6 py-4">Precio</th>
            <th v-if="auth.isAdmin" class="px-6 py-4"></th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="loading">
            <td colspan="4" class="px-6 py-8 text-center text-gray-500">Cargando...</td>
          </tr>
          <tr
            v-for="product in filtered"
            :key="product.id"
            class="border-b border-gray-800/50 hover:bg-gray-800/30 transition-colors"
          >
            <td class="px-6 py-4">
              <p class="font-medium text-white">{{ product.name }}</p>
              <p class="text-gray-500 text-xs mt-0.5">{{ product.description }}</p>
            </td>
            <td class="px-6 py-4">
              <span class="text-xs bg-gray-800 text-gray-300 px-2 py-1 rounded-full">{{ product.category || '—' }}</span>
            </td>
            <td class="px-6 py-4 text-emerald-400 font-mono font-medium">${{ product.price.toFixed(2) }}</td>
            <td v-if="auth.isAdmin" class="px-6 py-4 text-right space-x-2">
              <button @click="openModal(product)" class="text-gray-500 hover:text-white text-xs transition-colors">Editar</button>
              <button @click="confirmDelete(product)" class="text-gray-500 hover:text-red-400 text-xs transition-colors">Eliminar</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Modal -->
    <div v-if="showModal" class="fixed inset-0 bg-black/60 flex items-center justify-center z-50 p-4">
      <div class="bg-gray-900 border border-gray-800 rounded-2xl p-6 w-full max-w-md">
        <h3 class="text-white font-semibold mb-5">{{ editing ? 'Editar' : 'Nuevo' }} Producto</h3>
        <form @submit.prevent="save" class="space-y-4">
          <div>
            <label class="label">Nombre</label>
            <input v-model="form.name" required class="input-field" />
          </div>
          <div>
            <label class="label">Descripción</label>
            <input v-model="form.description" class="input-field" />
          </div>
          <div>
            <label class="label">Categoría</label>
            <input v-model="form.category" class="input-field" />
          </div>
          <div>
            <label class="label">Precio</label>
            <input v-model.number="form.price" type="number" step="0.01" required class="input-field" />
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
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { productsApi } from '@/api'

const auth = useAuthStore()
const products = ref([])
const loading = ref(true)
const showModal = ref(false)
const editing = ref(null)
const saving = ref(false)
const formError = ref('')
const filterCat = ref('Todos')
const form = ref({ name: '', description: '', category: '', price: 0 })

const categories = computed(() => {
  const cats = [...new Set(products.value.map((p) => p.category).filter(Boolean))]
  return ['Todos', ...cats]
})

const filtered = computed(() =>
  filterCat.value === 'Todos' ? products.value : products.value.filter((p) => p.category === filterCat.value),
)

async function load() {
  loading.value = true
  try { products.value = (await productsApi.list()).data } finally { loading.value = false }
}

function openModal(product = null) {
  editing.value = product
  form.value = { name: product?.name || '', description: product?.description || '', category: product?.category || '', price: product?.price || 0 }
  formError.value = ''
  showModal.value = true
}

async function save() {
  saving.value = true
  try {
    if (editing.value) await productsApi.update(editing.value.id, form.value)
    else await productsApi.create(form.value)
    showModal.value = false; await load()
  } catch { formError.value = 'Error al guardar' } finally { saving.value = false }
}

async function confirmDelete(product) {
  if (!confirm(`¿Eliminar "${product.name}"?`)) return
  try { await productsApi.delete(product.id); await load() } catch { alert('Error al eliminar') }
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