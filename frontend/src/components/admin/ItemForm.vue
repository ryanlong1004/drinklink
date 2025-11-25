<template>
  <div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
    <div class="bg-white rounded-lg max-w-3xl w-full max-h-[90vh] overflow-y-auto">
      <div class="sticky top-0 bg-white border-b px-6 py-4 flex justify-between items-center">
        <h3 class="text-xl font-bold">
          {{ isEditing ? 'Edit Item' : 'Create Item' }}
        </h3>
        <button
          class="text-gray-400 hover:text-gray-600"
          @click="$emit('close')"
        >
          <svg
            class="w-6 h-6"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M6 18L18 6M6 6l12 12"
            />
          </svg>
        </button>
      </div>

      <form
        class="p-6 space-y-6"
        @submit.prevent="handleSubmit"
      >
        <!-- Name -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">
            Name <span class="text-red-500">*</span>
          </label>
          <input
            v-model="form.name"
            type="text"
            required
            maxlength="100"
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
            placeholder="e.g., Miller Lite Draft"
          >
        </div>

        <!-- Description -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">
            Description
            <button
              type="button"
              :disabled="suggestingTags || !form.name"
              class="ml-2 text-xs text-primary-600 hover:text-primary-800 disabled:opacity-50"
              @click="suggestTags"
            >
              {{ suggestingTags ? 'Suggesting...' : '✨ Suggest Tags' }}
            </button>
          </label>
          <textarea
            v-model="form.description"
            rows="3"
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
            placeholder="Describe the drink's flavor profile, notes, etc."
          />
        </div>

        <!-- Category & Price Row -->
        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Category</label>
            <select
              v-model="form.category_id"
              class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
            >
              <option :value="null">
                No category
              </option>
              <option
                v-for="cat in categories"
                :key="cat.id"
                :value="cat.id"
              >
                {{ cat.name }}
              </option>
            </select>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Price <span class="text-red-500">*</span>
            </label>
            <div class="relative">
              <span class="absolute left-3 top-2 text-gray-500">$</span>
              <input
                v-model.number="form.price"
                type="number"
                step="0.01"
                min="0.01"
                required
                class="w-full pl-7 pr-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                placeholder="0.00"
              >
            </div>
          </div>
        </div>

        <!-- ABV, Volume, Sort Order Row -->
        <div class="grid grid-cols-3 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">ABV (%)</label>
            <input
              v-model.number="form.abv"
              type="number"
              step="0.1"
              min="0"
              max="100"
              class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
              placeholder="e.g., 5.0"
            >
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Volume</label>
            <input
              v-model="form.volume"
              type="text"
              maxlength="20"
              class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
              placeholder="e.g., 16 oz"
            >
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Sort Order</label>
            <input
              v-model.number="form.sort_order"
              type="number"
              class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
              placeholder="0"
            >
          </div>
        </div>

        <!-- Origin & Producer Row -->
        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Origin</label>
            <input
              v-model="form.origin"
              type="text"
              maxlength="100"
              class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
              placeholder="e.g., California, USA"
            >
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Producer</label>
            <input
              v-model="form.producer"
              type="text"
              maxlength="100"
              class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
              placeholder="e.g., Miller Brewing Company"
            >
          </div>
        </div>

        <!-- Image URL -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Image URL</label>
          <input
            v-model="form.image_url"
            type="url"
            maxlength="500"
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
            placeholder="https://example.com/image.jpg"
          >
        </div>

        <!-- Tags -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Tags</label>
          <div class="flex flex-wrap gap-2">
            <button
              v-for="tag in availableTags"
              :key="tag.id"
              type="button"
              :class="[
                'px-3 py-1 rounded-full text-sm font-medium transition-colors',
                form.tag_ids.includes(tag.id)
                  ? 'text-white'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200',
              ]"
              :style="form.tag_ids.includes(tag.id) ? { backgroundColor: tag.color } : {}"
              @click="toggleTag(tag.id)"
            >
              {{ tag.name }}
            </button>
          </div>
          <p
            v-if="suggestedTagIds.length > 0"
            class="text-xs text-gray-500 mt-2"
          >
            💡 Suggested: {{ suggestedTagIds.length }} tag(s) based on description
          </p>
        </div>

        <!-- Published Status -->
        <div class="flex items-center">
          <input
            id="is_published"
            v-model="form.is_published"
            type="checkbox"
            class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
          >
          <label
            for="is_published"
            class="ml-2 block text-sm text-gray-700"
          >
            Publish immediately (visible to public)
          </label>
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
            {{ submitting ? 'Saving...' : isEditing ? 'Update Item' : 'Create Item' }}
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
  item: {
    type: Object,
    default: null,
  },
})

const emit = defineEmits(['close', 'saved'])

const adminStore = useAdminStore()
const submitting = ref(false)
const suggestingTags = ref(false)
const suggestedTagIds = ref([])

const isEditing = computed(() => !!props.item)

const categories = computed(() => adminStore.categories)
const availableTags = computed(() => adminStore.tags)

// Initialize form
const form = ref({
  name: '',
  description: '',
  category_id: null,
  price: null,
  abv: null,
  volume: '',
  origin: '',
  producer: '',
  is_published: true,
  sort_order: 0,
  image_url: '',
  tag_ids: [],
})

// Populate form if editing
if (props.item) {
  form.value = {
    name: props.item.name,
    description: props.item.description || '',
    category_id: props.item.category_id,
    price: props.item.price,
    abv: props.item.abv,
    volume: props.item.volume || '',
    origin: props.item.origin || '',
    producer: props.item.producer || '',
    is_published: props.item.is_published,
    sort_order: props.item.sort_order,
    image_url: props.item.image_url || '',
    tag_ids: props.item.tags?.map(t => t.id) || [],
  }
}

const toggleTag = tagId => {
  const index = form.value.tag_ids.indexOf(tagId)
  if (index > -1) {
    form.value.tag_ids.splice(index, 1)
  } else {
    form.value.tag_ids.push(tagId)
  }
}

const suggestTags = async () => {
  if (!form.value.name) return

  suggestingTags.value = true
  try {
    const result = await adminStore.suggestTags({
      name: form.value.name,
      description: form.value.description || undefined,
      abv: form.value.abv || undefined,
      origin: form.value.origin || undefined,
    })

    // Add suggested tags that exist in the database
    if (result.existing_tags && result.existing_tags.length > 0) {
      const newTagIds = result.existing_tags
        .map(t => t.id)
        .filter(id => !form.value.tag_ids.includes(id))
      form.value.tag_ids.push(...newTagIds)
      suggestedTagIds.value = newTagIds

      // Clear the suggestion highlight after a few seconds
      setTimeout(() => {
        suggestedTagIds.value = []
      }, 3000)
    }
  } finally {
    suggestingTags.value = false
  }
}

const handleSubmit = async () => {
  submitting.value = true
  try {
    let success
    if (isEditing.value) {
      success = await adminStore.updateItem(props.item.id, form.value)
    } else {
      success = await adminStore.createItem(form.value)
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
