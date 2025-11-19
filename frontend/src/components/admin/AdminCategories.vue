<template>
  <div>
    <div class="flex justify-between items-center mb-6">
      <h2 class="text-2xl font-bold">Categories</h2>
      <button @click="showCreateModal = true" class="btn btn-primary">
        + Add Category
      </button>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      <div
        v-for="category in adminStore.categories"
        :key="category.id"
        class="card"
      >
        <h3 class="text-lg font-semibold mb-2">{{ category.name }}</h3>
        <p class="text-sm text-gray-600 mb-3">{{ category.description || 'No description' }}</p>
        <div class="flex gap-2">
          <button class="text-sm text-primary-600 hover:text-primary-900">Edit</button>
          <button class="text-sm text-red-600 hover:text-red-900">Delete</button>
        </div>
      </div>
    </div>

    <!-- Modal placeholder -->
    <div v-if="showCreateModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div class="bg-white rounded-lg max-w-md w-full p-6">
        <h3 class="text-xl font-bold mb-4">Create Category</h3>
        <p class="text-gray-600 mb-4">Category form would go here</p>
        <button @click="showCreateModal = false" class="btn btn-secondary">Close</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAdminStore } from '../../stores/admin'

const adminStore = useAdminStore()
const showCreateModal = ref(false)

onMounted(() => {
  adminStore.fetchCategories()
})
</script>
