<template>
  <div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
    <div class="bg-white rounded-lg max-w-2xl w-full max-h-[90vh] overflow-y-auto">
      <div class="sticky top-0 bg-white border-b px-6 py-4 flex justify-between items-center">
        <h3 class="text-xl font-bold">
          {{ isEditing ? 'Edit Category' : 'Create Category' }}
        </h3>
        <button class="text-gray-400 hover:text-gray-600" @click="$emit('close')">
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

      <form class="p-6 space-y-6" @submit.prevent="handleSubmit">
        <!-- Name -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">
            Name <span class="text-red-500">*</span>
          </label>
          <input
            v-model="form.name"
            type="text"
            required
            maxlength="50"
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
            placeholder="e.g., Draft Beer"
            @input="generateSlug"
          />
        </div>

        <!-- Slug -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">
            Slug <span class="text-red-500">*</span>
            <span class="text-xs text-gray-500 font-normal ml-2">URL-friendly identifier</span>
          </label>
          <input
            v-model="form.slug"
            type="text"
            required
            maxlength="50"
            pattern="[a-z0-9-]+"
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
            placeholder="e.g., draft-beer"
          />
          <p class="text-xs text-gray-500 mt-1">
            Only lowercase letters, numbers, and hyphens allowed
          </p>
        </div>

        <!-- Icon Picker -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">
            Icon
            <span class="text-xs text-gray-500 font-normal ml-2">Select an emoji icon</span>
          </label>
          <div class="grid grid-cols-8 gap-2">
            <button
              v-for="icon in availableIcons"
              :key="icon"
              type="button"
              :class="[
                'text-3xl p-3 rounded-lg border-2 transition-all hover:scale-110',
                form.icon === icon
                  ? 'border-primary-500 bg-primary-50'
                  : 'border-gray-200 hover:border-gray-300',
              ]"
              @click="form.icon = icon"
            >
              {{ icon }}
            </button>
          </div>
          <div v-if="form.icon" class="mt-2 flex items-center gap-2 text-sm text-gray-600">
            <span>Selected:</span>
            <span class="text-2xl">{{ form.icon }}</span>
            <button
              type="button"
              class="text-xs text-red-600 hover:text-red-800"
              @click="form.icon = null"
            >
              Clear
            </button>
          </div>
        </div>

        <!-- Description -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Description</label>
          <textarea
            v-model="form.description"
            rows="3"
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
            placeholder="Optional description for this category"
          />
        </div>

        <!-- Sort Order -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">
            Sort Order
            <span class="text-xs text-gray-500 font-normal ml-2">Lower numbers appear first</span>
          </label>
          <input
            v-model.number="form.sort_order"
            type="number"
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
            placeholder="0"
          />
        </div>

        <!-- Actions -->
        <div class="flex justify-end gap-3 pt-4 border-t">
          <button
            type="button"
            class="px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50"
            @click="$emit('close')"
          >
            Cancel
          </button>
          <button
            type="submit"
            :disabled="submitting"
            class="px-4 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700 disabled:opacity-50"
          >
            {{ submitting ? 'Saving...' : isEditing ? 'Update Category' : 'Create Category' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useAdminStore } from '../../stores/admin'

const props = defineProps({
  category: {
    type: Object,
    default: null,
  },
})

const emit = defineEmits(['close', 'saved'])

const adminStore = useAdminStore()
const submitting = ref(false)
const slugManuallyEdited = ref(false)

const availableIcons = [
  '🍺', // Beer mug
  '🍻', // Clinking beer mugs
  '🍶', // Sake bottle (beer bottle)
  '🥃', // Tumbler glass (can represent bottled drinks)
  '🍷', // Wine glass
  '🥫', // Can
  '🍸', // Cocktail glass
  '🍹', // Tropical drink
  '🥂', // Clinking glasses
  '🧃', // Juice box
  '🧋', // Bubble tea
  '☕', // Coffee
  '🍵', // Tea
  '🥤', // Cup with straw
  '🧊', // Ice cube
  '🍇', // Grapes
  '🍾', // Champagne bottle (alternative)
]

const isEditing = computed(() => !!props.category)

// Initialize form
const form = ref({
  name: '',
  slug: '',
  description: '',
  icon: null,
  sort_order: 0,
})

// Populate form if editing
if (props.category) {
  form.value = {
    name: props.category.name,
    slug: props.category.slug,
    description: props.category.description || '',
    icon: props.category.icon || null,
    sort_order: props.category.sort_order,
  }
  // When editing, slug is already set, so mark as manually edited
  slugManuallyEdited.value = true
}

const generateSlug = () => {
  // Only auto-generate slug if user hasn't manually edited it
  if (!slugManuallyEdited.value && form.value.name) {
    form.value.slug = form.value.name
      .toLowerCase()
      .replace(/[^a-z0-9]+/g, '-')
      .replace(/^-+|-+$/g, '')
  }
}

// Track when user manually edits the slug
const handleSlugInput = () => {
  slugManuallyEdited.value = true
}

const handleSubmit = async () => {
  submitting.value = true
  try {
    let success
    if (isEditing.value) {
      success = await adminStore.updateCategory(props.category.id, form.value)
    } else {
      success = await adminStore.createCategory(form.value)
    }

    if (success) {
      emit('saved')
      emit('close')
    }
  } finally {
    submitting.value = false
  }
}
</script>
