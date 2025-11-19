<template>
  <div>
    <div class="flex justify-between items-center mb-6">
      <h2 class="text-2xl font-bold">Tags</h2>
      <button @click="showCreateModal = true" class="btn btn-primary">
        + Add Tag
      </button>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      <div
        v-for="tag in adminStore.tags"
        :key="tag.id"
        class="card"
      >
        <div class="flex items-center gap-2 mb-2">
          <div
            class="w-4 h-4 rounded-full"
            :style="{ backgroundColor: tag.color }"
          ></div>
          <h3 class="text-lg font-semibold">{{ tag.name }}</h3>
        </div>
        <p class="text-sm text-gray-600 mb-3">{{ tag.description || 'No description' }}</p>
        <div class="flex gap-2">
          <button class="text-sm text-primary-600 hover:text-primary-900">Edit</button>
          <button class="text-sm text-red-600 hover:text-red-900">Delete</button>
        </div>
      </div>
    </div>

    <!-- Modal placeholder -->
    <div v-if="showCreateModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div class="bg-white rounded-lg max-w-md w-full p-6">
        <h3 class="text-xl font-bold mb-4">Create Tag</h3>
        <p class="text-gray-600 mb-4">Tag form would go here with color picker</p>
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
  adminStore.fetchTags()
})
</script>
