<template>
  <!-- Mobile-First Card Design: Large tap target, clear hierarchy -->
  <div
    class="bg-white rounded-xl shadow-md hover:shadow-xl active:scale-98 transition-all cursor-pointer p-5 border-2 border-transparent hover:border-primary-200">
    <!-- Header: Icon, Name, Price -->
    <div class="flex items-start gap-3 mb-3">
      <span class="text-4xl flex-shrink-0">{{ item.category?.icon || getCategoryIcon(item.category?.name) }}</span>
      <div class="flex-1 min-w-0">
        <h3 class="text-xl font-bold text-gray-900 leading-tight mb-1">{{ item.name }}</h3>
        <span class="inline-block text-2xl font-bold text-primary-600">${{ item.price.toFixed(2) }}</span>
      </div>
    </div>

    <!-- Description -->
    <p v-if="item.description" class="text-gray-600 text-base mb-4 line-clamp-2 leading-relaxed">
      {{ item.description }}
    </p>

    <!-- Specs: ABV, Volume - Larger, more readable -->
    <div class="flex items-center gap-4 text-base text-gray-700 font-medium mb-3">
      <span v-if="item.abv" class="flex items-center gap-2 bg-amber-50 px-3 py-1.5 rounded-lg">
        <svg class="w-5 h-5 text-amber-600" fill="currentColor" viewBox="0 0 20 20">
          <path
            d="M3 3a1 1 0 000 2v8a2 2 0 002 2h2.586l-1.293 1.293a1 1 0 101.414 1.414L10 15.414l2.293 2.293a1 1 0 001.414-1.414L12.414 15H15a2 2 0 002-2V5a1 1 0 100-2H3zm11 4a1 1 0 10-2 0v4a1 1 0 102 0V7zm-3 1a1 1 0 10-2 0v3a1 1 0 102 0V8zM8 9a1 1 0 00-2 0v2a1 1 0 102 0V9z" />
        </svg>
        {{ item.abv }}%
      </span>
      <span v-if="item.volume" class="bg-blue-50 px-3 py-1.5 rounded-lg text-blue-700">{{ item.volume }}</span>
    </div>

    <!-- Producer & Origin -->
    <div v-if="item.producer || item.origin" class="text-sm text-gray-600 mb-3 font-medium">
      <span v-if="item.producer">{{ item.producer }}</span>
      <span v-if="item.producer && item.origin"> • </span>
      <span v-if="item.origin">🌍 {{ item.origin }}</span>
    </div>

    <!-- Tags - Larger, easier to read -->
    <div v-if="item.tags && item.tags.length > 0" class="flex flex-wrap gap-2">
      <span v-for="tag in item.tags" :key="tag.id" class="inline-block px-3 py-1.5 rounded-full text-sm font-semibold"
        :style="{
          backgroundColor: tag.color + '20',
          color: tag.color
        }">
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
