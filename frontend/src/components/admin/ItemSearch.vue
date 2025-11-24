<template>
  <div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
    <div class="bg-white rounded-lg max-w-4xl w-full max-h-[90vh] overflow-y-auto">
      <div class="sticky top-0 bg-white border-b px-6 py-4 flex justify-between items-center">
        <h3 class="text-xl font-bold">
          Search & Add Item
        </h3>
        <button
          class="text-gray-400 hover:text-gray-600"
          @click="$emit('close')"
        >
          <svg
            class="w-6 h-6"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M6 18L18 6M6 6l12 12"
            />
          </svg>
        </button>
      </div>

      <div class="p-6">
        <!-- Search Bar -->
        <div class="mb-6">
          <label class="block text-sm font-medium text-gray-700 mb-2">
            Search for a drink
          </label>
          <div class="flex gap-2">
            <input
              v-model="searchQuery"
              type="text"
              placeholder="Enter beer, wine, or drink name..."
              class="flex-1 px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
              @keyup.enter="handleSearch"
            >
            <button
              :disabled="searching || !searchQuery.trim()"
              class="px-6 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700 disabled:opacity-50"
              @click="handleSearch"
            >
              {{ searching ? 'Searching...' : 'Search' }}
            </button>
          </div>
          <p class="text-sm text-gray-500 mt-2">
            Search our database of beers, wines, and spirits to quickly add items with pre-filled data
          </p>
        </div>

        <!-- Search Results -->
        <div
          v-if="searchResults.length > 0"
          class="space-y-3"
        >
          <h4 class="font-semibold text-gray-900">
            Search Results ({{ searchResults.length }})
          </h4>
          
          <div
            v-for="result in searchResults"
            :key="result.id"
            class="border border-gray-200 rounded-lg p-4 hover:border-primary-500 transition-colors cursor-pointer"
            @click="selectItem(result)"
          >
            <div class="flex justify-between items-start">
              <div class="flex-1">
                <h5 class="font-semibold text-lg text-gray-900">
                  {{ result.name }}
                </h5>
                <p class="text-sm text-gray-600 mt-1">
                  {{ result.style || result.type }}
                </p>
                <p class="text-sm text-gray-500 mt-2 line-clamp-2">
                  {{ result.description }}
                </p>
                
                <div class="flex gap-4 mt-3 text-sm">
                  <span
                    v-if="result.abv"
                    class="text-gray-600"
                  >
                    <strong>ABV:</strong> {{ result.abv }}%
                  </span>
                  <span
                    v-if="result.origin"
                    class="text-gray-600"
                  >
                    <strong>Origin:</strong> {{ result.origin }}
                  </span>
                  <span
                    v-if="result.producer"
                    class="text-gray-600"
                  >
                    <strong>Producer:</strong> {{ result.producer }}
                  </span>
                </div>
              </div>
              
              <button
                class="ml-4 px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 text-sm"
              >
                Add Item
              </button>
            </div>
          </div>
        </div>

        <!-- No Results -->
        <div
          v-else-if="hasSearched && !searching"
          class="text-center py-12"
        >
          <svg
            class="w-16 h-16 mx-auto text-gray-400 mb-4"
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
          <p class="text-gray-600 mb-4">
            No results found for "{{ lastSearchQuery }}"
          </p>
          <button
            class="px-4 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700"
            @click="createManually"
          >
            Create Item Manually
          </button>
        </div>

        <!-- Loading State -->
        <div
          v-if="searching"
          class="text-center py-12"
        >
          <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mb-4" />
          <p class="text-gray-600">
            Searching database...
          </p>
        </div>

        <!-- Initial State -->
        <div
          v-if="!hasSearched && !searching"
          class="text-center py-12"
        >
          <svg
            class="w-16 h-16 mx-auto text-gray-300 mb-4"
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
          <p class="text-gray-500">
            Enter a drink name to search
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAdminStore } from '../../stores/admin'

const emit = defineEmits(['close', 'item-selected'])

const adminStore = useAdminStore()

const searchQuery = ref('')
const lastSearchQuery = ref('')
const searching = ref(false)
const hasSearched = ref(false)
const searchResults = ref([])

const handleSearch = async () => {
  if (!searchQuery.value.trim()) return
  
  searching.value = true
  hasSearched.value = true
  lastSearchQuery.value = searchQuery.value
  searchResults.value = []
  
  try {
    const results = await adminStore.searchDrinkDatabase(searchQuery.value)
    searchResults.value = results
  } catch (error) {
    console.error('Search error:', error)
  } finally {
    searching.value = false
  }
}

const selectItem = (item) => {
  // Map the search result to item form data
  const itemData = {
    name: item.name,
    description: item.description || '',
    price: item.suggested_price || null,
    abv: item.abv || null,
    volume: item.volume || '',
    origin: item.origin || '',
    producer: item.producer || item.brewery || '',
    category_id: item.suggested_category_id || null,
    tag_ids: item.suggested_tag_ids || [],
    is_published: false, // Default to draft
    sort_order: 0,
    image_url: item.image_url || ''
  }
  
  emit('item-selected', itemData)
  emit('close')
}

const createManually = () => {
  emit('close')
  // The parent component will handle opening the regular create form
}
</script>
