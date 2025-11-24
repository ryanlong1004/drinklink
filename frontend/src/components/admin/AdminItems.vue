<template>
  <div>
    <div class="flex justify-between items-center mb-6">
      <h2 class="text-2xl font-bold">
        Menu Items
      </h2>
      <div class="flex gap-2">
        <button
          class="btn bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded"
          @click="showSearchModal = true"
        >
          🔍 Search Database
        </button>
        <button
          class="btn btn-primary"
          @click="showCreateModal = true"
        >
          + Add Item
        </button>
      </div>
    </div>

    <div
      v-if="adminStore.loading"
      class="text-center py-12"
    >
      <p>Loading...</p>
    </div>

    <div
      v-else-if="adminStore.error"
      class="text-center py-12"
    >
      <p class="text-red-600">
        Error: {{ adminStore.error }}
      </p>
    </div>

    <div
      v-else-if="adminStore.items.length === 0"
      class="text-center py-12"
    >
      <p class="text-gray-600">
        No items found. Add your first item!
      </p>
    </div>

    <div
      v-else
      class="bg-white rounded-lg shadow overflow-x-auto"
    >
      <table class="min-w-full divide-y divide-gray-200">
        <thead class="bg-gray-50">
          <tr>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
              Name
            </th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
              Category
            </th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
              Price
            </th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
              ABV
            </th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
              Status
            </th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
              Actions
            </th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          <tr
            v-for="item in adminStore.items"
            :key="item.id"
          >
            <td class="px-6 py-4 whitespace-nowrap">
              {{ item.name }}
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              {{ item.category?.name || '-' }}
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              ${{ item.price.toFixed(2) }}
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              {{ item.abv ? item.abv + '%' : '-' }}
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <button
                :class="[
                  'px-2 py-1 rounded text-xs font-medium',
                  item.is_published
                    ? 'bg-green-100 text-green-800'
                    : 'bg-gray-100 text-gray-800'
                ]"
                @click="togglePublish(item)"
              >
                {{ item.is_published ? 'Published' : 'Draft' }}
              </button>
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm">
              <button
                class="text-primary-600 hover:text-primary-900 mr-3"
                @click="editItem(item)"
              >
                Edit
              </button>
              <button
                class="text-red-600 hover:text-red-900"
                @click="deleteItem(item)"
              >
                Delete
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Create/Edit Modal -->
    <ItemForm
      v-if="showCreateModal"
      :item="editingItem"
      @close="closeModal"
      @saved="handleSaved"
    />

    <!-- Search Modal -->
    <ItemSearch
      v-if="showSearchModal"
      @close="showSearchModal = false"
      @item-selected="handleItemSelected"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAdminStore } from '../../stores/admin'
import ItemForm from './ItemForm.vue'
import ItemSearch from './ItemSearch.vue'

const adminStore = useAdminStore()
const showCreateModal = ref(false)
const showSearchModal = ref(false)
const editingItem = ref(null)

onMounted(async () => {
  console.log('AdminItems mounted, fetching data...')
  await adminStore.fetchAllItems()
  await adminStore.fetchCategories()
  await adminStore.fetchTags()
  console.log('Items loaded:', adminStore.items.length)
  console.log('Items:', adminStore.items)
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

const closeModal = () => {
  showCreateModal.value = false
  editingItem.value = null
}

const handleSaved = () => {
  // Modal will close itself via @close event
  console.log('Item saved successfully')
}

const handleItemSelected = (itemData) => {
  console.log('Item selected from search:', itemData)
  showSearchModal.value = false
  editingItem.value = itemData
  showCreateModal.value = true
}
</script>
