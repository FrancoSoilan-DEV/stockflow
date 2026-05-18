<template>
  <div class="bg-gray-900 border border-gray-800 rounded-xl p-5">
    <div class="flex items-center justify-between mb-3">
      <span class="text-2xl">{{ icon }}</span>
      <span
        class="text-xs px-2 py-1 rounded-full font-medium uppercase tracking-widest"
        :class="badgeClass"
      >{{ label }}</span>
    </div>
    <p class="text-3xl font-bold text-white">{{ value }}</p>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  label: String,
  value: [String, Number],
  icon: String,
  color: { type: String, default: 'emerald' },
})

const badgeClass = computed(() => ({
  emerald: 'bg-emerald-500/10 text-emerald-400',
  blue: 'bg-blue-500/10 text-blue-400',
  purple: 'bg-purple-500/10 text-purple-400',
  yellow: 'bg-yellow-500/10 text-yellow-400',
  red: 'bg-red-500/10 text-red-400',
}[props.color] || 'bg-gray-700 text-gray-400'))
</script>