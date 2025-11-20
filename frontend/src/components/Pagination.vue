<template>
  <!-- Mobile-First Pagination: ULTRA large buttons for easy tapping -->
  <div class="flex justify-center items-center gap-3 flex-wrap">
    <!-- First page button -->
    <button @click="menuStore.setPage(1)" :disabled="menuStore.pagination.page === 1"
      class="w-16 h-16 md:w-auto md:px-6 md:py-5 rounded-xl border-3 border-gray-400 font-black text-2xl disabled:opacity-30 disabled:cursor-not-allowed hover:bg-gray-50 active:scale-95 transition-all shadow-md">
      <span class="hidden md:inline">First</span>
      <span class="md:hidden">««</span>
    </button>

    <!-- Previous button -->
    <button @click="menuStore.setPage(menuStore.pagination.page - 1)" :disabled="menuStore.pagination.page === 1"
      class="px-7 py-5 rounded-xl border-3 border-gray-400 font-black text-2xl disabled:opacity-30 disabled:cursor-not-allowed hover:bg-gray-50 active:scale-95 transition-all shadow-md">
      ← Prev
    </button>

    <!-- Page numbers - simplified on mobile -->
    <div class="hidden md:flex gap-3">
      <button v-for="page in visiblePages" :key="page" @click="page !== '...' && menuStore.setPage(page)"
        :disabled="page === '...'" :class="[
          'w-16 h-16 rounded-xl border-3 font-black text-2xl transition-all shadow-md',
          page === menuStore.pagination.page
            ? 'bg-primary-600 text-white border-primary-700 shadow-lg'
            : page === '...'
              ? 'border-transparent cursor-default'
              : 'border-gray-400 hover:bg-gray-50 active:scale-95'
        ]">
        {{ page }}
      </button>
    </div>

    <!-- Mobile: Show current page info -->
    <div
      class="md:hidden px-7 py-5 bg-primary-100 text-primary-900 rounded-xl font-black text-2xl border-2 border-primary-300 shadow-sm">
      {{ menuStore.pagination.page }} / {{ menuStore.pagination.pages }}
    </div>

    <!-- Next button -->
    <button @click="menuStore.setPage(menuStore.pagination.page + 1)"
      :disabled="menuStore.pagination.page === menuStore.pagination.pages"
      class="px-7 py-5 rounded-xl border-3 border-gray-400 font-black text-2xl disabled:opacity-30 disabled:cursor-not-allowed hover:bg-gray-50 active:scale-95 transition-all shadow-md">
      Next →
    </button>

    <!-- Last page button -->
    <button @click="menuStore.setPage(menuStore.pagination.pages)"
      :disabled="menuStore.pagination.page === menuStore.pagination.pages"
      class="w-16 h-16 md:w-auto md:px-6 md:py-5 rounded-xl border-3 border-gray-400 font-black text-2xl disabled:opacity-30 disabled:cursor-not-allowed hover:bg-gray-50 active:scale-95 transition-all shadow-md">
      <span class="hidden md:inline">Last</span>
      <span class="md:hidden">»»</span>
    </button>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useMenuStore } from '../stores/menu'

const menuStore = useMenuStore()

const visiblePages = computed(() => {
  const current = menuStore.pagination.page
  const total = menuStore.pagination.pages
  const delta = 2

  const range = []
  for (
    let i = Math.max(2, current - delta);
    i <= Math.min(total - 1, current + delta);
    i++
  ) {
    range.push(i)
  }

  if (current - delta > 2) {
    range.unshift('...')
  }
  if (current + delta < total - 1) {
    range.push('...')
  }

  range.unshift(1)
  if (total > 1) {
    range.push(total)
  }

  return range.filter((v, i, a) => a.indexOf(v) === i)
})
</script>
