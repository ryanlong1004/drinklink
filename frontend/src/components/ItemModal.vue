<template>
  <!-- Full-screen modal on mobile, centered on desktop -->
  <div
    class="fixed inset-0 bg-black bg-opacity-60 z-50 overflow-y-auto"
    @click.self="$emit('close')"
  >
    <div class="min-h-screen md:flex md:items-center md:justify-center md:p-4">
      <div class="bg-white md:rounded-2xl md:max-w-2xl w-full md:shadow-2xl animate-slideUp">
        <!-- Header -->
        <div
          class="sticky top-0 bg-gradient-to-r from-primary-600 to-primary-700 text-white p-6 md:rounded-t-2xl shadow-lg z-10"
        >
          <div class="flex justify-between items-start gap-4">
            <div class="flex items-center gap-3 flex-1">
              <span class="text-4xl">{{ item.category?.icon || '🍺' }}</span>
              <h2 class="text-2xl md:text-3xl font-bold leading-tight">
                {{ item.name }}
              </h2>
            </div>
            <button
              class="flex-shrink-0 w-10 h-10 rounded-full bg-white bg-opacity-20 hover:bg-opacity-30 active:scale-95 transition-all flex items-center justify-center"
              @click="$emit('close')"
            >
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M6 18L18 6M6 6l12 12"
                />
              </svg>
            </button>
          </div>
          <div class="mt-4">
            <span
              class="inline-block text-3xl font-bold bg-white text-primary-600 px-5 py-2 rounded-full shadow"
            >
              ${{ item.price.toFixed(2) }}
            </span>
          </div>
        </div>

        <div class="p-6 space-y-6">
          <img
            v-if="item.image_url"
            :src="item.image_url"
            :alt="item.name"
            class="w-full h-48 object-cover rounded-lg shadow"
          />

          <!-- Specs -->
          <div class="flex gap-3">
            <div
              v-if="item.abv"
              class="flex-1 bg-amber-50 border-2 border-amber-300 rounded-lg p-4 text-center"
            >
              <div class="text-amber-600 text-sm font-bold mb-1">ABV</div>
              <div class="text-2xl font-bold text-amber-900">{{ item.abv }}%</div>
            </div>
            <div
              v-if="item.volume"
              class="flex-1 bg-blue-50 border-2 border-blue-300 rounded-lg p-4 text-center"
            >
              <div class="text-blue-600 text-sm font-bold mb-1">SIZE</div>
              <div class="text-xl font-bold text-blue-900">
                {{ item.volume }}
              </div>
            </div>
          </div>

          <div v-if="item.category">
            <span
              class="inline-block bg-primary-100 text-primary-900 px-4 py-2 rounded-full text-sm font-bold"
            >
              {{ item.category.name }}
            </span>
          </div>

          <p v-if="item.description" class="text-gray-700 text-base leading-relaxed">
            {{ item.description }}
          </p>

          <div
            v-if="item.producer || item.origin"
            class="bg-gray-50 border-2 border-gray-200 rounded-lg p-4 space-y-3"
          >
            <div v-if="item.producer" class="flex items-start gap-3">
              <span class="text-2xl">🏭</span>
              <div>
                <div class="font-bold text-gray-900 text-xs mb-1">PRODUCER</div>
                <div class="text-gray-700 text-sm">
                  {{ item.producer }}
                </div>
              </div>
            </div>
            <div v-if="item.origin" class="flex items-start gap-3">
              <span class="text-2xl">🌍</span>
              <div>
                <div class="font-bold text-gray-900 text-xs mb-1">ORIGIN</div>
                <div class="text-gray-700 text-sm">
                  {{ item.origin }}
                </div>
              </div>
            </div>
          </div>

          <div v-if="item.tags && item.tags.length > 0">
            <h3 class="font-bold text-gray-900 mb-3 text-lg">🎯 Taste Profile</h3>
            <div class="flex flex-wrap gap-2">
              <span
                v-for="tag in item.tags"
                :key="tag.id"
                class="inline-flex items-center px-3 py-1.5 rounded-lg text-sm font-bold"
                :style="{
                  backgroundColor: tag.color + '30',
                  color: tag.color,
                  borderWidth: '2px',
                  borderColor: tag.color,
                }"
              >
                {{ tag.name }}
              </span>
            </div>
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
    required: true,
  },
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
