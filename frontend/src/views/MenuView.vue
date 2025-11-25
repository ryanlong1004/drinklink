<template>
  <div class="min-h-screen bg-gray-50 pb-20">
    <!-- Mobile-First Header -->
    <header
      class="bg-gradient-to-r from-primary-600 to-primary-700 text-white shadow-lg sticky top-0 z-20"
    >
      <div class="px-6 py-6">
        <h1 class="text-4xl font-black mb-2 tracking-tight">
          🍺 DrinkLink
        </h1>
        <p class="text-primary-50 text-base font-semibold">
          Tap to explore our selection
        </p>
      </div>
    </header>

    <!-- Search and Filters - Mobile Optimized -->
    <div class="px-4 py-5 bg-white shadow-sm">
      <FilterBar />
    </div>

    <!-- Items Grid - Mobile First -->
    <main class="px-4 py-5">
      <div
        v-if="menuStore.loading"
        class="text-center py-20"
      >
        <div
          class="inline-block animate-spin rounded-full h-16 w-16 border-4 border-primary-200 border-t-primary-600"
        />
        <p class="mt-6 text-gray-700 text-xl font-bold">
          Loading menu...
        </p>
      </div>

      <div
        v-else-if="menuStore.error"
        class="text-center py-20 px-4"
      >
        <div class="text-6xl mb-6">
          😕
        </div>
        <p class="text-red-600 text-xl font-bold">
          {{ menuStore.error }}
        </p>
      </div>

      <div v-else>
        <div
          v-if="menuStore.items.length === 0"
          class="text-center py-20 px-4"
        >
          <div class="text-6xl mb-6">
            🔍
          </div>
          <p class="text-gray-700 text-xl font-bold">
            No items found
          </p>
          <p class="text-gray-500 text-base mt-2 font-semibold">
            Try adjusting your filters
          </p>
        </div>

        <!-- Single column on mobile, multiple columns on larger screens -->
        <div
          v-else
          class="flex flex-col space-y-4 lg:grid lg:grid-cols-2 lg:gap-6 lg:space-y-0 xl:grid-cols-3"
        >
          <ItemCard
            v-for="item in menuStore.items"
            :key="item.id"
            :item="item"
            @click="selectedItem = item"
          />
        </div>

        <!-- Pagination - Mobile Friendly -->
        <div class="mt-6">
          <Pagination v-if="menuStore.pagination.pages > 1" />
        </div>
      </div>
    </main>

    <!-- Item Detail Modal - Full Screen on Mobile -->
    <ItemModal
      v-if="selectedItem"
      :item="selectedItem"
      @close="selectedItem = null"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useMenuStore } from '../stores/menu'
import FilterBar from '../components/FilterBar.vue'
import ItemCard from '../components/ItemCard.vue'
import ItemModal from '../components/ItemModal.vue'
import Pagination from '../components/Pagination.vue'

const menuStore = useMenuStore()
const selectedItem = ref(null)

onMounted(async () => {
  await menuStore.fetchCategories()
  await menuStore.fetchTags()
  await menuStore.fetchOrigins()
  await menuStore.fetchItems()
})
</script>
