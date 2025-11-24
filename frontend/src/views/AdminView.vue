<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <header class="bg-white shadow-sm">
      <div class="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
        <div>
          <h1 class="text-2xl font-bold text-primary-600">DrinkLink Admin</h1>
        </div>
        <div class="flex items-center gap-4">
          <button @click="handleExport" class="btn btn-primary" :disabled="exporting">
            {{ exporting ? 'Exporting...' : 'Export Data' }}
          </button>
          <label class="btn btn-primary cursor-pointer">
            <input type="file" @change="handleImport" accept=".json" class="hidden" :disabled="importing">
            {{ importing ? 'Importing...' : 'Import Data' }}
          </label>
          <router-link to="/" class="text-gray-600 hover:text-gray-900">
            View Menu
          </router-link>
          <button @click="handleLogout" class="btn btn-secondary">
            Logout
          </button>
        </div>
      </div>
    </header>

    <!-- Tabs -->
    <div class="max-w-7xl mx-auto px-4 py-6">
      <div class="border-b border-gray-200">
        <nav class="-mb-px flex space-x-8">
          <button
            @click="activeTab = 'items'"
            :class="[
              'py-4 px-1 border-b-2 font-medium text-sm',
              activeTab === 'items'
                ? 'border-primary-500 text-primary-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            ]"
          >
            Menu Items
          </button>
          <button
            @click="activeTab = 'categories'"
            :class="[
              'py-4 px-1 border-b-2 font-medium text-sm',
              activeTab === 'categories'
                ? 'border-primary-500 text-primary-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            ]"
          >
            Categories
          </button>
          <button
            @click="activeTab = 'tags'"
            :class="[
              'py-4 px-1 border-b-2 font-medium text-sm',
              activeTab === 'tags'
                ? 'border-primary-500 text-primary-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            ]"
          >
            Tags
          </button>
        </nav>
      </div>
    </div>

    <!-- Content -->
    <main class="max-w-7xl mx-auto px-4 pb-12">
      <component :is="currentTabComponent" />
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { useAdminStore } from '../stores/admin'
import AdminItems from '../components/admin/AdminItems.vue'
import AdminCategories from '../components/admin/AdminCategories.vue'
import AdminTags from '../components/admin/AdminTags.vue'
import api from '../services/api'

const router = useRouter()
const authStore = useAuthStore()
const adminStore = useAdminStore()

const activeTab = ref('items')
const exporting = ref(false)
const importing = ref(false)

const currentTabComponent = computed(() => {
  const components = {
    items: AdminItems,
    categories: AdminCategories,
    tags: AdminTags
  }
  return components[activeTab.value]
})

const handleLogout = () => {
  authStore.logout()
  router.push('/login')
}

const handleExport = async () => {
  try {
    exporting.value = true
    const response = await api.exportData()
    
    // Create blob from JSON data and download
    const jsonStr = JSON.stringify(response.data, null, 2)
    const blob = new Blob([jsonStr], { type: 'application/json' })
    const url = window.URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = `drinklink-data-${new Date().toISOString().split('T')[0]}.json`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    window.URL.revokeObjectURL(url)
    
    alert('Data exported successfully!')
  } catch (error) {
    console.error('Export failed:', error)
    alert('Failed to export data: ' + (error.response?.data?.detail || error.message))
  } finally {
    exporting.value = false
  }
}

const handleImport = async (event) => {
  const file = event.target.files[0]
  if (!file) return
  
  try {
    importing.value = true
    
    // Read file
    const text = await file.text()
    const data = JSON.parse(text)
    
    // Import data
    const response = await api.importData(data)
    
    alert(
      `Import successful!\n` +
      `Categories: ${response.data.categories_imported || 0}\n` +
      `Tags: ${response.data.tags_imported || 0}\n` +
      `Items: ${response.data.items_imported || 0}`
    )
    
    // Refresh current view
    if (activeTab.value === 'items') {
      await adminStore.fetchAllItems()
    } else if (activeTab.value === 'categories') {
      await adminStore.fetchCategories()
    } else if (activeTab.value === 'tags') {
      await adminStore.fetchTags()
    }
  } catch (error) {
    console.error('Import failed:', error)
    alert('Failed to import data: ' + (error.response?.data?.detail || error.message))
  } finally {
    importing.value = false
    event.target.value = '' // Reset file input
  }
}

onMounted(async () => {
  const isValid = await authStore.verifyToken()
  if (!isValid) {
    router.push('/login')
  }
})
</script>
