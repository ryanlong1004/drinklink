<template>
  <div class="card hover:shadow-lg transition-shadow cursor-pointer">
    <div class="flex justify-between items-start mb-3">
      <div class="flex items-center gap-2 flex-1">
        <span class="text-2xl">{{ item.category?.icon || getCategoryIcon(item.category?.name) }}</span>
        <h3 class="text-xl font-semibold text-gray-900">{{ item.name }}</h3>
      </div>
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

const getCategoryIcon = (categoryName) => {
  if (!categoryName) return '🍺'
  
  const name = categoryName.toLowerCase()
  
  if (name.includes('draft') || name.includes('tap')) {
    return '🍺' // Draft beer mug
  } else if (name.includes('seltzer') || name.includes('seltzer')) {
    return '🥫' // Can for hard seltzers
  } else if (name.includes('bottle')) {
    return '🍾' // Bottle
  } else if (name.includes('wine')) {
    return '🍷' // Wine glass
  } else if (name.includes('cocktail') || name.includes('mixed')) {
    return '🍸' // Cocktail
  } else if (name.includes('spirit') || name.includes('liquor')) {
    return '🥃' // Whiskey glass
  } else if (name.includes('cider')) {
    return '🍺' // Beer mug (for cider)
  } else {
    return '🍺' // Default to beer mug
  }
}
</script>
