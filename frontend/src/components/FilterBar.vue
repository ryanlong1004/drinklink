<template>
  <div class="space-y-5">
    <!-- Search Bar - Large and prominent -->
    <div class="relative">
      <input v-model="searchQuery" @input="debouncedSearch" type="search" placeholder="🔍 Search drinks..."
        class="w-full px-5 py-4 text-lg border-2 border-gray-300 rounded-xl focus:outline-none focus:ring-4 focus:ring-primary-200 focus:border-primary-500 pl-14 shadow-sm" />
      <svg class="absolute left-5 top-5 h-6 w-6 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"
        stroke-width="2">
        <path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
      </svg>
    </div>

    <!-- Categories - Horizontal scroll on mobile -->
    <div v-if="menuStore.categories.length > 0">
      <h3 class="font-bold text-lg mb-3 text-gray-900">Categories</h3>
      <div class="flex gap-2 overflow-x-auto pb-2 -mx-1 px-1 scrollbar-hide">
        <button @click="menuStore.setFilter('categoryId', null)" :class="[
          'flex-shrink-0 px-5 py-3 rounded-xl font-semibold text-base transition-all shadow-sm border-2',
          menuStore.filters.categoryId === null
            ? 'bg-primary-600 text-white border-primary-600 shadow-md'
            : 'bg-white text-gray-700 border-gray-300 hover:border-primary-300 active:scale-95'
        ]">
          All
        </button>
        <button v-for="category in menuStore.categories" :key="category.id"
          @click="menuStore.setFilter('categoryId', category.id)" :class="[
            'flex-shrink-0 px-5 py-3 rounded-xl font-semibold text-base transition-all shadow-sm border-2',
            menuStore.filters.categoryId === category.id
              ? 'bg-primary-600 text-white border-primary-600 shadow-md'
              : 'bg-white text-gray-700 border-gray-300 hover:border-primary-300 active:scale-95'
          ]">
          {{ category.icon }} {{ category.name }}
        </button>
      </div>
    </div>

    <!-- Tags - Horizontal scroll on mobile -->
    <div v-if="menuStore.tags.length > 0">
      <h3 class="font-bold text-lg mb-3 text-gray-900">Filter by Taste</h3>
      <div class="flex gap-2 overflow-x-auto pb-2 -mx-1 px-1 scrollbar-hide">
        <button v-for="tag in menuStore.tags" :key="tag.id" @click="menuStore.toggleTag(tag.id)" :class="[
          'flex-shrink-0 px-5 py-3 rounded-xl font-semibold text-base transition-all shadow-sm border-2',
          menuStore.filters.tagIds.includes(tag.id) ? 'shadow-md' : 'active:scale-95'
        ]" :style="menuStore.filters.tagIds.includes(tag.id) ? {
            backgroundColor: tag.color + '30',
            borderColor: tag.color,
            color: tag.color
          } : {
            backgroundColor: 'white',
            borderColor: '#D1D5DB',
            color: '#374151'
          }">
          {{ tag.name }}
        </button>
      </div>
    </div>

    <!-- Origins - Horizontal scroll on mobile -->
    <div v-if="menuStore.origins.length > 0">
      <h3 class="font-bold text-lg mb-3 text-gray-900">Filter by Origin</h3>
      <div class="flex gap-2 overflow-x-auto pb-2 -mx-1 px-1 scrollbar-hide">
        <button @click="menuStore.setFilter('origin', null)" :class="[
          'flex-shrink-0 px-5 py-3 rounded-xl font-semibold text-base transition-all shadow-sm border-2',
          menuStore.filters.origin === null
            ? 'bg-primary-600 text-white border-primary-600 shadow-md'
            : 'bg-white text-gray-700 border-gray-300 hover:border-primary-300 active:scale-95'
        ]">
          All
        </button>
        <button v-for="origin in menuStore.origins" :key="origin" @click="menuStore.setFilter('origin', origin)" :class="[
          'flex-shrink-0 px-5 py-3 rounded-xl font-semibold text-base transition-all shadow-sm border-2',
          menuStore.filters.origin === origin
            ? 'bg-primary-600 text-white border-primary-600 shadow-md'
            : 'bg-white text-gray-700 border-gray-300 hover:border-primary-300 active:scale-95'
        ]">
          🌍 {{ origin }}
        </button>
      </div>
    </div>

    <!-- Sort Options - Mobile friendly -->
    <div class="bg-gray-50 rounded-xl p-4 space-y-3">
      <div class="grid grid-cols-2 gap-3">
        <div>
          <label class="block text-sm font-bold text-gray-700 mb-2">Sort by</label>
          <select v-model="menuStore.filters.sortBy" @change="menuStore.fetchItems()"
            class="w-full px-4 py-3 text-base border-2 border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500">
            <option value="name">Name</option>
            <option value="price">Price</option>
            <option value="abv">ABV</option>
            <option value="created_at">Newest</option>
          </select>
        </div>

        <div>
          <label class="block text-sm font-bold text-gray-700 mb-2">Order</label>
          <button @click="toggleSortOrder"
            class="w-full px-4 py-3 text-base bg-white border-2 border-gray-300 rounded-lg font-semibold hover:border-primary-300 active:scale-95 transition-all">
            {{ menuStore.filters.sortOrder === 'asc' ? '↑ A-Z' : '↓ Z-A' }}
          </button>
        </div>
      </div>

      <button v-if="hasActiveFilters" @click="menuStore.clearFilters()"
        class="w-full px-4 py-3 text-base bg-red-500 text-white rounded-lg font-bold hover:bg-red-600 active:scale-95 transition-all shadow-sm">
        ✕ Clear All Filters
      </button>
    </div>

    <!-- Active Filters Summary -->
    <div v-if="hasActiveFilters" class="text-center">
      <span class="inline-block bg-primary-100 text-primary-800 px-4 py-2 rounded-full text-sm font-bold">
        {{ menuStore.pagination.total }} result{{ menuStore.pagination.total !== 1 ? 's' : '' }}
      </span>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useMenuStore } from '../stores/menu'

const menuStore = useMenuStore()
const searchQuery = ref(menuStore.filters.search)

let searchTimeout
const debouncedSearch = () => {
  clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => {
    menuStore.setFilter('search', searchQuery.value)
  }, 300)
}

const toggleSortOrder = () => {
  const newOrder = menuStore.filters.sortOrder === 'asc' ? 'desc' : 'asc'
  menuStore.setFilter('sortOrder', newOrder)
}

const hasActiveFilters = computed(() => {
  return (
    menuStore.filters.categoryId !== null ||
    menuStore.filters.tagIds.length > 0 ||
    menuStore.filters.origin !== null ||
    menuStore.filters.search !== ''
  )
})
</script>

<style scoped>
/* Hide scrollbar for horizontal scroll on mobile */
.scrollbar-hide {
  -ms-overflow-style: none;
  scrollbar-width: none;
}

.scrollbar-hide::-webkit-scrollbar {
  display: none;
}
</style>
