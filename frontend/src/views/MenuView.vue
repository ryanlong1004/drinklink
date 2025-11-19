<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <header class="bg-white shadow-sm sticky top-0 z-10">
      <div class="max-w-7xl mx-auto px-4 py-4">
        <h1 class="text-3xl font-bold text-primary-600">DrinkLink</h1>
        <p class="text-gray-600">Discover your next favorite drink</p>
      </div>
    </header>

    <!-- Search and Filters -->
    <div class="max-w-7xl mx-auto px-4 py-6">
      <FilterBar />
    </div>

    <!-- Items Grid -->
    <main class="max-w-7xl mx-auto px-4 pb-12">
      <div v-if="menuStore.loading" class="text-center py-12">
        <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
        <p class="mt-4 text-gray-600">Loading menu...</p>
      </div>

      <div v-else-if="menuStore.error" class="text-center py-12">
        <p class="text-red-600">{{ menuStore.error }}</p>
      </div>

      <div v-else>
        <div v-if="menuStore.items.length === 0" class="text-center py-12">
          <p class="text-gray-600 text-lg">No items found. Try adjusting your filters.</p>
        </div>

        <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <ItemCard 
            v-for="item in menuStore.items" 
            :key="item.id" 
            :item="item"
            @click="selectedItem = item"
          />
        </div>

        <!-- Pagination -->
        <Pagination v-if="menuStore.pagination.pages > 1" />
      </div>
    </main>

    <!-- Item Detail Modal -->
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
  await menuStore.fetchItems()
})
</script>
