<template>
  <div class="space-y-6">
    <!-- Search Bar - ULTRA Large and prominent -->
    <div class="relative">
      <input v-model="searchQuery" @input="debouncedSearch" type="search" placeholder="🔍 Search drinks..."
        class="w-full px-8 py-6 text-2xl font-bold border-3 border-gray-400 rounded-2xl focus:outline-none focus:ring-4 focus:ring-primary-300 focus:border-primary-600 pl-20 shadow-md" />
      <svg class="absolute left-7 top-7 h-9 w-9 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"
        stroke-width="2.5">
        <path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
      </svg>
    </div>

    <!-- Categories - Horizontal scroll on mobile -->
    <div v-if="menuStore.categories.length > 0">
      <h3 class="font-black text-3xl mb-5 text-gray-900">Categories</h3>
      <div class="flex gap-4 overflow-x-auto pb-3 -mx-1 px-1 scrollbar-hide">
        <button @click="menuStore.setFilter('categoryId', null)" :class="[
          'flex-shrink-0 px-8 py-5 rounded-2xl font-black text-2xl transition-all shadow-md border-3',
          menuStore.filters.categoryId === null
            ? 'bg-primary-600 text-white border-primary-700 shadow-lg scale-105'
            : 'bg-white text-gray-800 border-gray-400 hover:border-primary-400 active:scale-95'
        ]">
          All
        </button>
        <button v-for="category in menuStore.categories" :key="category.id"
          @click="menuStore.setFilter('categoryId', category.id)" :class="[
            'flex-shrink-0 px-8 py-5 rounded-2xl font-black text-2xl transition-all shadow-md border-3 whitespace-nowrap',
            menuStore.filters.categoryId === category.id
              ? 'bg-primary-600 text-white border-primary-700 shadow-lg scale-105'
              : 'bg-white text-gray-800 border-gray-400 hover:border-primary-400 active:scale-95'
          ]">
          <span class="text-3xl mr-3">{{ category.icon }}</span>{{ category.name }}
        </button>
      </div>
    </div>

    <!-- Tags - Horizontal scroll on mobile -->
    <div v-if="menuStore.tags.length > 0">
      <h3 class="font-black text-3xl mb-5 text-gray-900">Filter by Taste</h3>
      <div class="flex gap-4 overflow-x-auto pb-3 -mx-1 px-1 scrollbar-hide">
        <button v-for="tag in menuStore.tags" :key="tag.id" @click="menuStore.toggleTag(tag.id)" :class="[
          'flex-shrink-0 px-8 py-5 rounded-2xl font-black text-2xl transition-all shadow-md border-3 whitespace-nowrap',
          menuStore.filters.tagIds.includes(tag.id) ? 'shadow-lg scale-105' : 'active:scale-95'
        ]" :style="menuStore.filters.tagIds.includes(tag.id) ? {
          backgroundColor: tag.color + '40',
          borderColor: tag.color,
          color: tag.color
        } : {
          backgroundColor: 'white',
          borderColor: '#9CA3AF',
          color: '#1F2937'
        }">
          {{ tag.name }}
        </button>
      </div>
    </div>

    <!-- Origins - Horizontal scroll on mobile -->
    <div v-if="menuStore.origins.length > 0">
      <h3 class="font-black text-3xl mb-5 text-gray-900">Filter by Origin</h3>
      <div class="flex gap-4 overflow-x-auto pb-3 -mx-1 px-1 scrollbar-hide">
        <button @click="menuStore.setFilter('origin', null)" :class="[
          'flex-shrink-0 px-8 py-5 rounded-2xl font-black text-2xl transition-all shadow-md border-3',
          menuStore.filters.origin === null
            ? 'bg-primary-600 text-white border-primary-700 shadow-lg scale-105'
            : 'bg-white text-gray-800 border-gray-400 hover:border-primary-400 active:scale-95'
        ]">
          All
        </button>
        <button v-for="origin in menuStore.origins" :key="origin" @click="menuStore.setFilter('origin', origin)" :class="[
          'flex-shrink-0 px-8 py-5 rounded-2xl font-black text-2xl transition-all shadow-md border-3 whitespace-nowrap',
          menuStore.filters.origin === origin
            ? 'bg-primary-600 text-white border-primary-700 shadow-lg scale-105'
            : 'bg-white text-gray-800 border-gray-400 hover:border-primary-400 active:scale-95'
        ]">
          <span class="text-3xl mr-3">🌍</span>{{ origin }}
        </button>
      </div>
    </div>

    <!-- Sort Options - Mobile friendly with larger text -->
    <div class="bg-gray-100 rounded-2xl p-6 space-y-5 border-2 border-gray-300">
      <div class="grid grid-cols-2 gap-5">
        <div>
          <label class="block text-xl font-black text-gray-900 mb-3">Sort by</label>
          <select v-model="menuStore.filters.sortBy" @change="menuStore.fetchItems()"
            class="w-full px-6 py-5 text-2xl font-black border-3 border-gray-400 rounded-xl focus:outline-none focus:ring-4 focus:ring-primary-300 focus:border-primary-600 shadow-sm">
            <option value="name">Name</option>
            <option value="price">Price</option>
            <option value="abv">ABV</option>
            <option value="created_at">Newest</option>
          </select>
        </div>

        <div>
          <label class="block text-xl font-black text-gray-900 mb-3">Order</label>
          <button @click="toggleSortOrder"
            class="w-full px-6 py-5 text-2xl bg-white border-3 border-gray-400 rounded-xl font-black hover:border-primary-400 active:scale-95 transition-all shadow-sm">
            {{ menuStore.filters.sortOrder === 'asc' ? '↑ A-Z' : '↓ Z-A' }}
          </button>
        </div>
      </div>

      <button v-if="hasActiveFilters" @click="menuStore.clearFilters()"
        class="w-full px-8 py-5 text-2xl bg-red-500 text-white rounded-xl font-black hover:bg-red-600 active:scale-95 transition-all shadow-md border-2 border-red-600">
        ✕ Clear All Filters
      </button>
    </div>

    <!-- Active Filters Summary -->
    <div v-if="hasActiveFilters" class="text-center">
      <span
        class="inline-block bg-primary-100 text-primary-900 px-8 py-4 rounded-full text-2xl font-black border-2 border-primary-300 shadow-sm">
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
