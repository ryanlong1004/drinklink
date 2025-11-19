<template>
  <div class="card hover:shadow-lg transition-shadow cursor-pointer">
    <div class="flex justify-between items-start mb-3">
      <h3 class="text-xl font-semibold text-gray-900">{{ item.name }}</h3>
      <span class="text-lg font-bold text-primary-600">${{ item.price.toFixed(2) }}</span>
    </div>

    <p v-if="item.description" class="text-gray-600 text-sm mb-3 line-clamp-2">
      {{ item.description }}
    </p>

    <div class="flex items-center gap-4 text-sm text-gray-500 mb-3">
      <span v-if="item.abv" class="flex items-center gap-1">
        <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
          <path d="M3 3a1 1 0 000 2v8a2 2 0 002 2h2.586l-1.293 1.293a1 1 0 101.414 1.414L10 15.414l2.293 2.293a1 1 0 001.414-1.414L12.414 15H15a2 2 0 002-2V5a1 1 0 100-2H3zm11 4a1 1 0 10-2 0v4a1 1 0 102 0V7zm-3 1a1 1 0 10-2 0v3a1 1 0 102 0V8zM8 9a1 1 0 00-2 0v2a1 1 0 102 0V9z" />
        </svg>
        {{ item.abv }}%
      </span>
      <span v-if="item.volume">{{ item.volume }}</span>
      <span v-if="item.category" class="text-primary-600">{{ item.category.name }}</span>
    </div>

    <div v-if="item.producer || item.origin" class="text-xs text-gray-500 mb-3">
      <span v-if="item.producer">{{ item.producer }}</span>
      <span v-if="item.producer && item.origin"> • </span>
      <span v-if="item.origin">{{ item.origin }}</span>
    </div>

    <div v-if="item.tags && item.tags.length > 0" class="flex flex-wrap gap-1">
      <span
        v-for="tag in item.tags"
        :key="tag.id"
        class="inline-block px-2 py-1 rounded-full text-xs font-medium"
        :style="{
          backgroundColor: tag.color + '20',
          color: tag.color
        }"
      >
        {{ tag.name }}
      </span>
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
</script>
