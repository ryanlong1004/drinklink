import axios from 'axios'

const api = axios.create({
    baseURL: import.meta.env.VITE_API_URL || '',
    headers: {
        'Content-Type': 'application/json'
    },
    paramsSerializer: {
        serialize: (params) => {
            const searchParams = new URLSearchParams()
            Object.keys(params).forEach(key => {
                if (params[key] !== null && params[key] !== undefined) {
                    // Convert boolean to lowercase string for FastAPI
                    const value = typeof params[key] === 'boolean'
                        ? params[key].toString().toLowerCase()
                        : params[key]
                    searchParams.append(key, value)
                }
            })
            return searchParams.toString()
        }
    }
})

// Add auth token to requests
api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('token')
        if (token) {
            config.headers.Authorization = `Bearer ${token}`
        }
        return config
    },
    (error) => {
        return Promise.reject(error)
    }
)

// Handle 401 errors
api.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response?.status === 401) {
            localStorage.removeItem('token')
            window.location.href = '/login'
        }
        return Promise.reject(error)
    }
)

export default {
    // Auth
    login(username, password) {
        return api.post('/api/v1/auth/login', { username, password })
    },

    verifyToken() {
        return api.get('/api/v1/auth/verify')
    },

    // Items
    getItems(params = {}) {
        return api.get('/api/v1/items', { params })
    },

    getItem(id) {
        return api.get(`/api/v1/items/${id}`)
    },

    createItem(data) {
        return api.post('/api/v1/items', data)
    },

    updateItem(id, data) {
        return api.put(`/api/v1/items/${id}`, data)
    },

    deleteItem(id) {
        return api.delete(`/api/v1/items/${id}`)
    },

    suggestTags(params) {
        return api.post('/api/v1/items/suggest-tags', null, { params })
    },

    getOrigins() {
        return api.get('/api/v1/items/origins/list')
    },

    searchDrinkDatabase(query) {
        return api.get('/api/v1/items/search-database', { params: { q: query } })
    },

    // Categories
    getCategories() {
        return api.get('/api/v1/categories')
    },

    getCategory(id) {
        return api.get(`/api/v1/categories/${id}`)
    },

    createCategory(data) {
        return api.post('/api/v1/categories', data)
    },

    updateCategory(id, data) {
        return api.put(`/api/v1/categories/${id}`, data)
    },

    deleteCategory(id) {
        return api.delete(`/api/v1/categories/${id}`)
    },

    // Tags
    getTags() {
        return api.get('/api/v1/tags')
    },

    getTag(id) {
        return api.get(`/api/v1/tags/${id}`)
    },

    createTag(data) {
        return api.post('/api/v1/tags', data)
    },

    updateTag(id, data) {
        return api.put(`/api/v1/tags/${id}`, data)
    },

    deleteTag(id) {
        return api.delete(`/api/v1/tags/${id}`)
    },

    autoGenerateTags() {
        return api.post('/api/v1/tags/auto-generate')
    }
}
