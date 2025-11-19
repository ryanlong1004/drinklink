<template>
  <div>
    <div class="flex justify-between items-center mb-6">
      <h2 class="text-2xl font-bold">Tags</h2>
      <div class="flex gap-3">
        <button
          @click="handleAutoGenerate"
          :disabled="autoGenerating"
          class="px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 disabled:opacity-50 flex items-center gap-2"
        >
          <svg v-if="!autoGenerating" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
          </svg>
          <svg v-else class="w-5 h-5 animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
          {{ autoGenerating ? 'Generating...' : '✨ Auto-Generate Tags' }}
        </button>
        <button @click="showCreateModal = true" class="btn btn-primary">
          + Add Tag
        </button>
      </div>
    </div>

    <!-- Success message -->
    <div v-if="autoGenMessage" class="mb-4 p-4 bg-green-50 border border-green-200 rounded-md">
      <p class="text-green-800 font-medium">{{ autoGenMessage }}</p>
      <p v-if="autoGenDetails" class="text-sm text-green-700 mt-1">
        Created {{ autoGenDetails.created_tags?.length || 0 }} new tags
        ({{ autoGenDetails.already_existed }} already existed)
      </p>
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
const autoGenerating = ref(false)
const autoGenMessage = ref('')
const autoGenDetails = ref(null)

onMounted(() => {
  adminStore.fetchTags()
})

const handleAutoGenerate = async () => {
  if (!confirm('Auto-generate tags from all items? This will analyze item descriptions and create new tags.')) {
    return
  }
  
  autoGenerating.value = true
  autoGenMessage.value = ''
  autoGenDetails.value = null
  
  try {
    const result = await adminStore.autoGenerateTags()
    if (result) {
      autoGenMessage.value = result.message
      autoGenDetails.value = result
      
      // Clear message after 5 seconds
      setTimeout(() => {
        autoGenMessage.value = ''
        autoGenDetails.value = null
      }, 5000)
    }
  } finally {
    autoGenerating.value = false
  }
}
</script>
