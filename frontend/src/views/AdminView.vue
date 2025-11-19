<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <header class="bg-white shadow-sm">
      <div class="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
        <div>
          <h1 class="text-2xl font-bold text-primary-600">DrinkLink Admin</h1>
        </div>
        <div class="flex items-center gap-4">
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

const router = useRouter()
const authStore = useAuthStore()
const adminStore = useAdminStore()

const activeTab = ref('items')

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

onMounted(async () => {
  const isValid = await authStore.verifyToken()
  if (!isValid) {
    router.push('/login')
  }
})
</script>
