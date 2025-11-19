<template>
  <div
    class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50"
    @click.self="$emit('close')"
  >
    <div class="bg-white rounded-lg max-w-2xl w-full max-h-[90vh] overflow-y-auto">
      <div class="p-6">
        <!-- Header -->
        <div class="flex justify-between items-start mb-4">
          <h2 class="text-2xl font-bold text-gray-900">{{ item.name }}</h2>
          <button
            @click="$emit('close')"
            class="text-gray-400 hover:text-gray-600"
          >
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <!-- Image (if available) -->
        <img
          v-if="item.image_url"
          :src="item.image_url"
          :alt="item.name"
          class="w-full h-64 object-cover rounded-lg mb-4"
        />

        <!-- Price and Details -->
        <div class="flex items-center justify-between mb-4">
          <span class="text-3xl font-bold text-primary-600">${{ item.price.toFixed(2) }}</span>
          <div class="flex gap-4 text-sm text-gray-600">
            <span v-if="item.abv">ABV: {{ item.abv }}%</span>
            <span v-if="item.volume">{{ item.volume }}</span>
          </div>
        </div>

        <!-- Category -->
        <div v-if="item.category" class="mb-4">
          <span class="inline-block bg-primary-100 text-primary-800 px-3 py-1 rounded-full text-sm font-medium">
            {{ item.category.name }}
          </span>
        </div>

        <!-- Description -->
        <p v-if="item.description" class="text-gray-700 mb-4 leading-relaxed">
          {{ item.description }}
        </p>

        <!-- Producer and Origin -->
        <div v-if="item.producer || item.origin" class="mb-4 p-4 bg-gray-50 rounded-lg">
          <div v-if="item.producer" class="mb-2">
            <span class="font-semibold text-gray-700">Producer:</span>
            <span class="text-gray-600 ml-2">{{ item.producer }}</span>
          </div>
          <div v-if="item.origin">
            <span class="font-semibold text-gray-700">Origin:</span>
            <span class="text-gray-600 ml-2">{{ item.origin }}</span>
          </div>
        </div>

        <!-- Tags -->
        <div v-if="item.tags && item.tags.length > 0">
          <h3 class="font-semibold mb-2">Taste Profile</h3>
          <div class="flex flex-wrap gap-2">
            <span
              v-for="tag in item.tags"
              :key="tag.id"
              class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium"
              :style="{
                backgroundColor: tag.color + '20',
                color: tag.color,
                borderWidth: '2px',
                borderColor: tag.color
              }"
            >
              {{ tag.name }}
            </span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  item: {
    type: Object,
    required: true
  }
})

defineEmits(['close'])
</script>
