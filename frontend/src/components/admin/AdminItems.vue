<template>
  <div>
    <div class="flex justify-between items-center mb-6">
      <h2 class="text-2xl font-bold">Menu Items</h2>
      <button @click="showCreateModal = true" class="btn btn-primary">
        + Add Item
      </button>
    </div>

    <div v-if="adminStore.loading" class="text-center py-12">
      <p>Loading...</p>
    </div>

    <div v-else class="bg-white rounded-lg shadow overflow-x-auto">
      <table class="min-w-full divide-y divide-gray-200">
        <thead class="bg-gray-50">
          <tr>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Name</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Category</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Price</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">ABV</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Actions</th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          <tr v-for="item in adminStore.items" :key="item.id">
            <td class="px-6 py-4 whitespace-nowrap">{{ item.name }}</td>
            <td class="px-6 py-4 whitespace-nowrap">{{ item.category?.name || '-' }}</td>
            <td class="px-6 py-4 whitespace-nowrap">${{ item.price.toFixed(2) }}</td>
            <td class="px-6 py-4 whitespace-nowrap">{{ item.abv ? item.abv + '%' : '-' }}</td>
            <td class="px-6 py-4 whitespace-nowrap">
              <button
                @click="togglePublish(item)"
                :class="[
                  'px-2 py-1 rounded text-xs font-medium',
                  item.is_published
                    ? 'bg-green-100 text-green-800'
                    : 'bg-gray-100 text-gray-800'
                ]"
              >
                {{ item.is_published ? 'Published' : 'Draft' }}
              </button>
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm">
              <button @click="editItem(item)" class="text-primary-600 hover:text-primary-900 mr-3">
                Edit
              </button>
              <button @click="deleteItem(item)" class="text-red-600 hover:text-red-900">
                Delete
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Create/Edit Modal would go here -->
    <div v-if="showCreateModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div class="bg-white rounded-lg max-w-2xl w-full max-h-[90vh] overflow-y-auto p-6">
        <h3 class="text-xl font-bold mb-4">{{ editingItem ? 'Edit Item' : 'Create Item' }}</h3>
        <p class="text-gray-600 mb-4">Item form would go here with all fields</p>
        <button @click="showCreateModal = false" class="btn btn-secondary">Close</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAdminStore } from '../../stores/admin'

const adminStore = useAdminStore()
const showCreateModal = ref(false)
const editingItem = ref(null)

onMounted(() => {
  adminStore.fetchAllItems()
  adminStore.fetchCategories()
  adminStore.fetchTags()
})

const togglePublish = async (item) => {
  await adminStore.updateItem(item.id, {
    is_published: !item.is_published
  })
}

const editItem = (item) => {
  editingItem.value = item
  showCreateModal.value = true
}

const deleteItem = async (item) => {
  if (confirm(`Delete "${item.name}"?`)) {
    await adminStore.deleteItem(item.id)
  }
}
</script>
