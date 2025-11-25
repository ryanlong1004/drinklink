<template>
  <div class="min-h-screen bg-gray-50 flex items-center justify-center px-4">
    <div class="max-w-md w-full">
      <div class="card">
        <h1 class="text-2xl font-bold text-center mb-6">
          Admin Login
        </h1>

        <form @submit.prevent="handleLogin">
          <div class="mb-4">
            <label class="block text-sm font-medium mb-2">Username</label>
            <input
              v-model="username"
              type="text"
              class="input"
              required
              autocomplete="username"
            >
          </div>

          <div class="mb-6">
            <label class="block text-sm font-medium mb-2">Password</label>
            <input
              v-model="password"
              type="password"
              class="input"
              required
              autocomplete="current-password"
            >
          </div>

          <button
            type="submit"
            class="btn btn-primary w-full"
            :disabled="loading"
          >
            {{ loading ? 'Logging in...' : 'Login' }}
          </button>

          <p
            v-if="error"
            class="text-red-600 text-sm mt-4 text-center"
          >
            {{ error }}
          </p>
        </form>

        <div class="mt-6 text-center">
          <router-link
            to="/"
            class="text-primary-600 hover:text-primary-700"
          >
            Back to Menu
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const username = ref('')
const password = ref('')
const loading = ref(false)
const error = ref('')

const handleLogin = async () => {
  loading.value = true
  error.value = ''

  const success = await authStore.login(username.value, password.value)

  if (success) {
    router.push('/admin')
  } else {
    error.value = 'Invalid username or password'
  }

  loading.value = false
}
</script>
