<template>
  <div class="space-y-6">
    <!-- Search Bar -->
    <div class="relative">
      <input
        v-model="searchQuery"
        @input="debouncedSearch"
        type="text"
        placeholder="Search drinks..."
        class="input pl-10"
      />
      <svg
        class="absolute left-3 top-3 h-5 w-5 text-gray-400"
        fill="none"
        stroke="currentColor"
        viewBox="0 0 24 24"
      >
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          stroke-width="2"
          d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
        />
      </svg>
    </div>

    <!-- Categories -->
    <div v-if="menuStore.categories.length > 0">
      <h3 class="font-semibold mb-3">Categories</h3>
      <div class="flex flex-wrap gap-2">
        <button
          @click="menuStore.setFilter('categoryId', null)"
          :class="[
            'tag-chip',
            menuStore.filters.categoryId === null
              ? 'tag-chip-active'
              : 'tag-chip-inactive'
          ]"
        >
          All
        </button>
        <button
          v-for="category in menuStore.categories"
          :key="category.id"
          @click="menuStore.setFilter('categoryId', category.id)"
          :class="[
            'tag-chip',
            menuStore.filters.categoryId === category.id
              ? 'tag-chip-active'
              : 'tag-chip-inactive'
          ]"
        >
          {{ category.name }}
        </button>
      </div>
    </div>

    <!-- Tags -->
    <div v-if="menuStore.tags.length > 0">
      <h3 class="font-semibold mb-3">Filter by Taste</h3>
      <div class="flex flex-wrap gap-2">
        <button
          v-for="tag in menuStore.tags"
          :key="tag.id"
          @click="menuStore.toggleTag(tag.id)"
          :class="[
            'tag-chip',
            menuStore.filters.tagIds.includes(tag.id)
              ? 'tag-chip-active'
              : 'tag-chip-inactive'
          ]"
          :style="menuStore.filters.tagIds.includes(tag.id) ? {
            backgroundColor: tag.color + '20',
            borderColor: tag.color,
            color: tag.color
          } : {}"
        >
          {{ tag.name }}
        </button>
      </div>
    </div>

    <!-- Origins -->
    <div v-if="menuStore.origins.length > 0">
      <h3 class="font-semibold mb-3">Filter by Origin</h3>
      <div class="flex flex-wrap gap-2">
        <button
          @click="menuStore.setFilter('origin', null)"
          :class="[
            'tag-chip',
            menuStore.filters.origin === null
              ? 'tag-chip-active'
              : 'tag-chip-inactive'
          ]"
        >
          All
        </button>
        <button
          v-for="origin in menuStore.origins"
          :key="origin"
          @click="menuStore.setFilter('origin', origin)"
          :class="[
            'tag-chip',
            menuStore.filters.origin === origin
              ? 'tag-chip-active'
              : 'tag-chip-inactive'
          ]"
        >
          {{ origin }}
        </button>
      </div>
    </div>

    <!-- Sort Options -->
    <div class="flex items-center gap-4 flex-wrap">
      <div class="flex items-center gap-2">
        <label class="text-sm font-medium">Sort by:</label>
        <select
          v-model="menuStore.filters.sortBy"
          @change="menuStore.fetchItems()"
          class="input py-2"
        >
          <option value="name">Name</option>
          <option value="price">Price</option>
          <option value="abv">ABV</option>
          <option value="created_at">Newest</option>
        </select>
      </div>
      
      <button
        @click="toggleSortOrder"
        class="btn btn-secondary"
      >
        {{ menuStore.filters.sortOrder === 'asc' ? '↑ Ascending' : '↓ Descending' }}
      </button>

      <button
        v-if="hasActiveFilters"
        @click="menuStore.clearFilters()"
        class="btn btn-secondary ml-auto"
      >
        Clear Filters
      </button>
    </div>

    <!-- Active Filters Summary -->
    <div v-if="hasActiveFilters" class="text-sm text-gray-600">
      Showing {{ menuStore.pagination.total }} result{{ menuStore.pagination.total !== 1 ? 's' : '' }}
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
