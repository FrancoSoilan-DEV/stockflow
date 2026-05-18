<template>
  <div class="flex gap-4 h-[calc(100vh-8rem)]">
    <!-- Lista de usuarios -->
    <div class="w-64 bg-gray-900 border border-gray-800 rounded-xl flex flex-col shrink-0">
      <div class="px-4 py-3 border-b border-gray-800">
        <p class="text-xs text-gray-500 uppercase tracking-widest">Usuarios</p>
      </div>
      <div class="flex-1 overflow-y-auto p-2">
        <button
          v-for="user in otherUsers"
          :key="user.id"
          @click="selectUser(user)"
          class="w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm transition-colors text-left"
          :class="selectedUser?.id === user.id ? 'bg-emerald-500/10 text-emerald-400' : 'text-gray-400 hover:bg-gray-800 hover:text-white'"
        >
          <div class="relative">
            <div class="w-8 h-8 rounded-full bg-gray-700 flex items-center justify-center text-xs font-bold">
              {{ user.username[0].toUpperCase() }}
            </div>
            <span
              class="absolute -bottom-0.5 -right-0.5 w-2.5 h-2.5 rounded-full border-2 border-gray-900"
              :class="onlineUsers.includes(user.id) ? 'bg-emerald-400' : 'bg-gray-600'"
            ></span>
          </div>
          <div>
            <p class="font-medium">{{ user.username }}</p>
            <p class="text-xs opacity-60 capitalize">{{ user.role }}</p>
          </div>
        </button>
      </div>
    </div>

    <!-- Chat -->
    <div class="flex-1 bg-gray-900 border border-gray-800 rounded-xl flex flex-col">
      <!-- Header -->
      <div class="px-5 py-3 border-b border-gray-800 flex items-center gap-3">
        <template v-if="selectedUser">
          <div class="w-7 h-7 rounded-full bg-gray-700 flex items-center justify-center text-xs font-bold text-white">
            {{ selectedUser.username[0].toUpperCase() }}
          </div>
          <span class="text-sm font-medium text-white">{{ selectedUser.username }}</span>
          <span class="w-2 h-2 rounded-full" :class="onlineUsers.includes(selectedUser.id) ? 'bg-emerald-400' : 'bg-gray-600'"></span>
        </template>
        <span v-else class="text-sm text-gray-500">Seleccioná un usuario para chatear</span>
      </div>

      <!-- Messages -->
      <div ref="messagesEl" class="flex-1 overflow-y-auto p-5 space-y-3">
        <div v-if="!selectedUser" class="h-full flex items-center justify-center">
          <p class="text-gray-600 text-sm">💬 Elegí un contacto</p>
        </div>
        <div
          v-for="(msg, i) in messages"
          :key="i"
          class="flex"
          :class="msg.sender_id === auth.user?.id ? 'justify-end' : 'justify-start'"
        >
          <div
            class="max-w-xs px-4 py-2.5 rounded-2xl text-sm"
            :class="msg.sender_id === auth.user?.id ? 'bg-emerald-500 text-gray-950 font-medium' : 'bg-gray-800 text-gray-200'"
          >
            <p>{{ msg.content }}</p>
            <p class="text-xs mt-1 opacity-60">{{ formatTime(msg.created_at) }}</p>
          </div>
        </div>
      </div>

      <!-- Input -->
      <div v-if="selectedUser" class="px-5 py-4 border-t border-gray-800 flex gap-3">
        <input
          v-model="newMessage"
          @keyup.enter="sendMessage"
          placeholder="Escribí un mensaje..."
          class="flex-1 bg-gray-800 border border-gray-700 text-white rounded-lg px-4 py-2.5 text-sm focus:outline-none focus:border-emerald-500 transition-colors placeholder-gray-600"
        />
        <button
          @click="sendMessage"
          :disabled="!newMessage.trim()"
          class="bg-emerald-500 hover:bg-emerald-400 disabled:opacity-40 text-gray-950 font-bold px-4 py-2.5 rounded-lg text-sm transition-colors"
        >↑</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, nextTick } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { usersApi } from '@/api'

const auth = useAuthStore()
const users = ref([])
const selectedUser = ref(null)
const messages = ref([])
const newMessage = ref('')
const onlineUsers = ref([])
const messagesEl = ref(null)
let ws = null

const otherUsers = computed(() => users.value.filter((u) => u.id !== auth.user?.id))

const formatTime = (d) => new Date(d).toLocaleTimeString('es-PY', { hour: '2-digit', minute: '2-digit' })

function connectWS() {
  const token = localStorage.getItem('token')
  ws = new WebSocket(`ws://localhost:8000/ws/chat?token=${token}`)

  ws.onmessage = (e) => {
    const data = JSON.parse(e.data)
    if (data.type === 'online_users') {
      onlineUsers.value = data.users
    } else if (data.type === 'presence') {
      if (data.status === 'online' && !onlineUsers.value.includes(data.user_id)) {
        onlineUsers.value.push(data.user_id)
      } else if (data.status === 'offline') {
        onlineUsers.value = onlineUsers.value.filter((id) => id !== data.user_id)
      }
    } else if (data.type === 'message') {
      const isRelevant =
        data.sender_id === selectedUser.value?.id ||
        data.sender_id === auth.user?.id
      if (isRelevant) {
        messages.value.push(data)
        nextTick(() => { if (messagesEl.value) messagesEl.value.scrollTop = messagesEl.value.scrollHeight })
      }
    }
  }
}

function selectUser(user) {
  selectedUser.value = user
  messages.value = []
}

function sendMessage() {
  if (!newMessage.value.trim() || !selectedUser.value || !ws) return
  ws.send(JSON.stringify({ receiver_id: selectedUser.value.id, content: newMessage.value.trim() }))
  newMessage.value = ''
}

onMounted(async () => {
  const res = await usersApi.list()
  users.value = res.data
  connectWS()
})

onUnmounted(() => { ws?.close() })
</script>