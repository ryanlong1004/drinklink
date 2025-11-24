<template>
  <!-- Mobile-First Pagination -->
  <div class="flex justify-center items-center gap-2 flex-wrap">
    <!-- First page button -->
    <button
      :disabled="menuStore.pagination.page === 1"
      class="w-10 h-10 md:w-auto md:px-4 md:py-2 rounded-lg border-2 border-gray-300 font-bold text-sm disabled:opacity-30 disabled:cursor-not-allowed hover:bg-gray-50 active:scale-95 transition-all"
      @click="menuStore.setPage(1)"
    >
      <span class="hidden md:inline">First</span>
      <span class="md:hidden">««</span>
    </button>

    <!-- Previous button -->
    <button
      :disabled="menuStore.pagination.page === 1"
      class="px-4 py-2 rounded-lg border-2 border-gray-300 font-bold text-sm disabled:opacity-30 disabled:cursor-not-allowed hover:bg-gray-50 active:scale-95 transition-all"
      @click="menuStore.setPage(menuStore.pagination.page - 1)"
    >
      ← Prev
    </button>

    <!-- Page numbers - simplified on mobile -->
    <div class="hidden md:flex gap-2">
      <button
        v-for="page in visiblePages"
        :key="page"
        :disabled="page === '...'"
        :class="[
          'w-10 h-10 rounded-lg border-2 font-bold text-sm transition-all',
          page === menuStore.pagination.page
            ? 'bg-primary-600 text-white border-primary-600 shadow-md'
            : page === '...'
              ? 'border-transparent cursor-default'
              : 'border-gray-300 hover:bg-gray-50 active:scale-95'
        ]"
        @click="page !== '...' && menuStore.setPage(page)"
      >
        {{ page }}
      </button>
    </div>

    <!-- Mobile: Show current page info -->
    <div
      class="md:hidden px-4 py-2 bg-primary-100 text-primary-900 rounded-lg font-bold text-sm border border-primary-300"
    >
      {{ menuStore.pagination.page }} / {{ menuStore.pagination.pages }}
    </div>

    <!-- Next button -->
    <button
      :disabled="menuStore.pagination.page === menuStore.pagination.pages"
      class="px-4 py-2 rounded-lg border-2 border-gray-300 font-bold text-sm disabled:opacity-30 disabled:cursor-not-allowed hover:bg-gray-50 active:scale-95 transition-all"
      @click="menuStore.setPage(menuStore.pagination.page + 1)"
    >
      Next →
    </button>

    <!-- Last page button -->
    <button
      :disabled="menuStore.pagination.page === menuStore.pagination.pages"
      class="w-10 h-10 md:w-auto md:px-4 md:py-2 rounded-lg border-2 border-gray-300 font-bold text-sm disabled:opacity-30 disabled:cursor-not-allowed hover:bg-gray-50 active:scale-95 transition-all"
      @click="menuStore.setPage(menuStore.pagination.pages)"
    >
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
