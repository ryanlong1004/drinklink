<template>
  <div>
    <div class="flex justify-between items-center mb-6">
      <h2 class="text-2xl font-bold">Categories</h2>
      <button class="btn btn-primary" @click="showCreateModal = true">+ Add Category</button>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      <div v-for="category in adminStore.categories" :key="category.id" class="card">
        <div class="flex justify-between items-start mb-2">
          <h3 class="text-lg font-semibold">
            {{ category.name }}
          </h3>
          <span class="text-xs text-gray-500 bg-gray-100 px-2 py-1 rounded">
            Order: {{ category.sort_order }}
          </span>
        </div>
        <p class="text-xs text-gray-500 mb-2 font-mono">
          {{ category.slug }}
        </p>
        <p class="text-sm text-gray-600 mb-3">
          {{ category.description || 'No description' }}
        </p>
        <div class="flex gap-2">
          <button
            class="text-sm text-primary-600 hover:text-primary-900"
            @click="editCategory(category)"
          >
            Edit
          </button>
          <button class="text-sm text-red-600 hover:text-red-900" @click="deleteCategory(category)">
            Delete
          </button>
        </div>
      </div>
    </div>

    <!-- Category Form Modal -->
    <CategoryForm
      v-if="showCreateModal"
      :category="editingCategory"
      @close="closeModal"
      @saved="handleSaved"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAdminStore } from '../../stores/admin'
import CategoryForm from './CategoryForm.vue'

const adminStore = useAdminStore()
const showCreateModal = ref(false)
const editingCategory = ref(null)

onMounted(() => {
  adminStore.fetchCategories()
})

const editCategory = category => {
  editingCategory.value = category
  showCreateModal.value = true
}

const deleteCategory = async category => {
  if (confirm(`Delete "${category.name}"? This will also remove this category from all items.`)) {
    await adminStore.deleteCategory(category.id)
  }
}

const closeModal = () => {
  showCreateModal.value = false
  editingCategory.value = null
}

const handleSaved = () => {
  console.log('Category saved successfully')
}
</script>
