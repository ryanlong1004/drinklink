<template>
  <!-- Mobile-First Card Design: Balanced for all devices -->
  <div
    class="bg-white rounded-2xl shadow-lg hover:shadow-xl active:scale-98 transition-all cursor-pointer p-6 border-2 border-gray-200 hover:border-primary-300"
  >
    <!-- Header: Icon, Name, Price -->
    <div class="flex items-start gap-4 mb-4">
      <span class="text-5xl flex-shrink-0 leading-none">{{
        item.category?.icon || getCategoryIcon(item.category?.name)
      }}</span>
      <div class="flex-1 min-w-0">
        <h3 class="text-xl font-black text-gray-900 leading-tight mb-2">
          {{ item.name }}
        </h3>
        <span class="inline-block text-2xl font-black text-primary-600"
          >${{ item.price.toFixed(2) }}</span
        >
      </div>
    </div>

    <!-- Description -->
    <p
      v-if="item.description"
      class="text-gray-800 text-base mb-4 line-clamp-3 leading-relaxed font-medium"
    >
      {{ item.description }}
    </p>

    <!-- Specs: ABV, Volume -->
    <div class="flex items-center gap-3 text-sm text-gray-900 font-bold mb-4">
      <span
        v-if="item.abv"
        class="flex items-center gap-2 bg-amber-100 px-4 py-2 rounded-xl border-2 border-amber-300"
      >
        <svg class="w-5 h-5 text-amber-700" fill="currentColor" viewBox="0 0 20 20">
          <path
            d="M3 3a1 1 0 000 2v8a2 2 0 002 2h2.586l-1.293 1.293a1 1 0 101.414 1.414L10 15.414l2.293 2.293a1 1 0 001.414-1.414L12.414 15H15a2 2 0 002-2V5a1 1 0 100-2H3zm11 4a1 1 0 10-2 0v4a1 1 0 102 0V7zm-3 1a1 1 0 10-2 0v3a1 1 0 102 0V8zM8 9a1 1 0 00-2 0v2a1 1 0 102 0V9z"
          />
        </svg>
        <span class="text-amber-900">{{ item.abv }}%</span>
      </span>
      <span
        v-if="item.volume"
        class="bg-blue-100 px-4 py-2 rounded-xl text-blue-900 border-2 border-blue-300"
        >{{ item.volume }}</span
      >
    </div>

    <!-- Producer & Origin -->
    <div v-if="item.producer || item.origin" class="text-sm text-gray-700 mb-4 font-semibold">
      <span v-if="item.producer">{{ item.producer }}</span>
      <span v-if="item.producer && item.origin"> • </span>
      <span v-if="item.origin">🌍 {{ item.origin }}</span>
    </div>

    <!-- Tags -->
    <div v-if="item.tags && item.tags.length > 0" class="flex flex-wrap gap-2">
      <span
        v-for="tag in item.tags"
        :key="tag.id"
        class="inline-block px-3 py-1.5 rounded-full text-xs font-black border-2"
        :style="{
          backgroundColor: tag.color + '20',
          color: tag.color,
          borderColor: tag.color,
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
    required: true,
  },
})

const getCategoryIcon = categoryName => {
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
