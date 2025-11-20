<template>
  <!-- Mobile-First Card Design: ULTRA large fonts for easy reading -->
  <div
    class="bg-white rounded-3xl shadow-xl hover:shadow-2xl active:scale-98 transition-all cursor-pointer p-8 border-3 border-gray-200 hover:border-primary-300">
    <!-- Header: Icon, Name, Price -->
    <div class="flex items-start gap-5 mb-6">
      <span class="text-7xl flex-shrink-0 leading-none">{{ item.category?.icon || getCategoryIcon(item.category?.name)
        }}</span>
      <div class="flex-1 min-w-0">
        <h3 class="text-3xl font-black text-gray-900 leading-tight mb-3">{{ item.name }}</h3>
        <span class="inline-block text-5xl font-black text-primary-600">${{ item.price.toFixed(2) }}</span>
      </div>
    </div>

    <!-- Description -->
    <p v-if="item.description" class="text-gray-800 text-xl mb-6 line-clamp-2 leading-relaxed font-semibold">
      {{ item.description }}
    </p>

    <!-- Specs: ABV, Volume - ULTRA large and bold -->
    <div class="flex items-center gap-4 text-2xl text-gray-900 font-black mb-6">
      <span v-if="item.abv"
        class="flex items-center gap-3 bg-amber-200 px-6 py-4 rounded-2xl border-3 border-amber-400 shadow-md">
        <svg class="w-8 h-8 text-amber-800" fill="currentColor" viewBox="0 0 20 20">
          <path
            d="M3 3a1 1 0 000 2v8a2 2 0 002 2h2.586l-1.293 1.293a1 1 0 101.414 1.414L10 15.414l2.293 2.293a1 1 0 001.414-1.414L12.414 15H15a2 2 0 002-2V5a1 1 0 100-2H3zm11 4a1 1 0 10-2 0v4a1 1 0 102 0V7zm-3 1a1 1 0 10-2 0v3a1 1 0 102 0V8zM8 9a1 1 0 00-2 0v2a1 1 0 102 0V9z" />
        </svg>
        <span class="text-amber-950">{{ item.abv }}%</span>
      </span>
      <span v-if="item.volume"
        class="bg-blue-200 px-6 py-4 rounded-2xl text-blue-950 border-3 border-blue-400 shadow-md">{{
          item.volume }}</span>
    </div>

    <!-- Producer & Origin -->
    <div v-if="item.producer || item.origin" class="text-xl text-gray-800 mb-6 font-bold">
      <span v-if="item.producer">{{ item.producer }}</span>
      <span v-if="item.producer && item.origin"> • </span>
      <span v-if="item.origin">🌍 {{ item.origin }}</span>
    </div>

    <!-- Tags - ULTRA large and bold -->
    <div v-if="item.tags && item.tags.length > 0" class="flex flex-wrap gap-3">
      <span v-for="tag in item.tags" :key="tag.id"
        class="inline-block px-6 py-3 rounded-2xl text-xl font-black border-3 shadow-sm" :style="{
          backgroundColor: tag.color + '30',
          color: tag.color,
          borderColor: tag.color
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
