<template>
  <div class="flex justify-center items-center gap-2 mt-8">
    <button
      @click="menuStore.setPage(1)"
      :disabled="menuStore.pagination.page === 1"
      class="px-3 py-2 rounded-lg border border-gray-300 disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50"
    >
      ««
    </button>
    
    <button
      @click="menuStore.setPage(menuStore.pagination.page - 1)"
      :disabled="menuStore.pagination.page === 1"
      class="px-3 py-2 rounded-lg border border-gray-300 disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50"
    >
      Previous
    </button>

    <div class="flex gap-1">
      <button
        v-for="page in visiblePages"
        :key="page"
        @click="menuStore.setPage(page)"
        :class="[
          'px-3 py-2 rounded-lg border',
          page === menuStore.pagination.page
            ? 'bg-primary-600 text-white border-primary-600'
            : 'border-gray-300 hover:bg-gray-50'
        ]"
      >
        {{ page }}
      </button>
    </div>

    <button
      @click="menuStore.setPage(menuStore.pagination.page + 1)"
      :disabled="menuStore.pagination.page === menuStore.pagination.pages"
      class="px-3 py-2 rounded-lg border border-gray-300 disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50"
    >
      Next
    </button>
    
    <button
      @click="menuStore.setPage(menuStore.pagination.pages)"
      :disabled="menuStore.pagination.page === menuStore.pagination.pages"
      class="px-3 py-2 rounded-lg border border-gray-300 disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50"
    >
      »»
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
