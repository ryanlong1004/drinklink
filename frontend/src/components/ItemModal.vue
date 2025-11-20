<template>
  <!-- Full-screen modal on mobile, centered on desktop -->
  <div class="fixed inset-0 bg-black bg-opacity-60 z-50 overflow-y-auto" @click.self="$emit('close')">
    <div class="min-h-screen md:flex md:items-center md:justify-center md:p-4">
      <div class="bg-white md:rounded-2xl md:max-w-2xl w-full md:shadow-2xl animate-slideUp">
        <!-- Mobile-optimized header with large close button -->
        <div
          class="sticky top-0 bg-gradient-to-r from-primary-600 to-primary-700 text-white p-8 md:rounded-t-2xl shadow-lg z-10">
          <div class="flex justify-between items-start gap-5">
            <div class="flex items-center gap-4 flex-1">
              <span class="text-6xl">{{ item.category?.icon || '🍺' }}</span>
              <h2 class="text-4xl md:text-5xl font-black leading-tight">{{ item.name }}</h2>
            </div>
            <button @click="$emit('close')"
              class="flex-shrink-0 w-16 h-16 rounded-full bg-white bg-opacity-20 hover:bg-opacity-30 active:scale-95 transition-all flex items-center justify-center">
              <svg class="w-10 h-10" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2.5">
                <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          <!-- Price in header -->
          <div class="mt-6">
            <span class="inline-block text-5xl font-black bg-white text-primary-600 px-8 py-4 rounded-full shadow-lg">
              ${{ item.price.toFixed(2) }}
            </span>
          </div>
        </div>

        <div class="p-8 space-y-8">
          <!-- Image (if available) -->
          <img v-if="item.image_url" :src="item.image_url" :alt="item.name"
            class="w-full h-56 md:h-72 object-cover rounded-xl shadow-md" />

          <!-- Specs: ABV & Volume - ULTRA large and prominent -->
          <div class="flex gap-5">
            <div v-if="item.abv" class="flex-1 bg-amber-50 border-3 border-amber-300 rounded-xl p-6 text-center">
              <div class="text-amber-600 text-xl font-black mb-2">ABV</div>
              <div class="text-5xl font-black text-amber-900">{{ item.abv }}%</div>
            </div>
            <div v-if="item.volume" class="flex-1 bg-blue-50 border-3 border-blue-300 rounded-xl p-6 text-center">
              <div class="text-blue-600 text-xl font-black mb-2">SIZE</div>
              <div class="text-4xl font-black text-blue-900">{{ item.volume }}</div>
            </div>
          </div>

          <!-- Category Badge -->
          <div v-if="item.category" class="flex justify-center">
            <span
              class="inline-block bg-primary-100 text-primary-900 px-8 py-4 rounded-full text-2xl font-black shadow-sm border-2 border-primary-300">
              {{ item.category.name }}
            </span>
          </div>

          <!-- Description - ULTRA large, easier to read -->
          <p v-if="item.description" class="text-gray-900 text-2xl leading-relaxed font-semibold">
            {{ item.description }}
          </p>

          <!-- Producer and Origin - Card style -->
          <div v-if="item.producer || item.origin" class="bg-gray-50 border-3 border-gray-300 rounded-xl p-7 space-y-5">
            <div v-if="item.producer" class="flex items-start gap-4">
              <span class="text-4xl">🏭</span>
              <div class="flex-1">
                <div class="font-black text-gray-900 text-xl mb-2">PRODUCER</div>
                <div class="text-gray-700 text-2xl font-semibold">{{ item.producer }}</div>
              </div>
            </div>
            <div v-if="item.origin" class="flex items-start gap-4">
              <span class="text-4xl">🌍</span>
              <div class="flex-1">
                <div class="font-black text-gray-900 text-xl mb-2">ORIGIN</div>
                <div class="text-gray-700 text-2xl font-semibold">{{ item.origin }}</div>
              </div>
            </div>
          </div>

          <!-- Tags - ULTRA large, more prominent -->
          <div v-if="item.tags && item.tags.length > 0">
            <h3 class="font-black text-gray-900 mb-5 text-3xl">🎯 Taste Profile</h3>
            <div class="flex flex-wrap gap-4">
              <span v-for="tag in item.tags" :key="tag.id"
                class="inline-flex items-center px-7 py-4 rounded-xl text-2xl font-black shadow-md" :style="{
                  backgroundColor: tag.color + '30',
                  color: tag.color,
                  borderWidth: '3px',
                  borderColor: tag.color
                }">
                {{ tag.name }}
              </span>
            </div>
          </div>
        </div>

        <!-- Bottom padding for mobile safe area -->
        <div class="h-8 md:h-4"></div>
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

<style scoped>
@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(100%);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-slideUp {
  animation: slideUp 0.3s ease-out;
}

@media (min-width: 768px) {
  .animate-slideUp {
    animation: none;
  }
}
</style>
