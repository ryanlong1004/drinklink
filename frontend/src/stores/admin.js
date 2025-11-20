import { defineStore } from 'pinia'
import api from '../services/api'
import { useMenuStore } from './menu'

export const useAdminStore = defineStore('admin', {
    state: () => ({
        items: [],
        categories: [],
        tags: [],
        loading: false,
        error: null
    }),

    actions: {
        async fetchAllItems() {
            this.loading = true
            try {
                const response = await api.getItems({
                    published_only: false,
                    page_size: 100
                })
                this.items = response.data.items
            } catch (error) {
                this.error = error.message
                console.error('Error fetching items:', error)
            } finally {
                this.loading = false
            }
        },

        async fetchCategories() {
            try {
                const response = await api.getCategories()
                this.categories = response.data
            } catch (error) {
                console.error('Error fetching categories:', error)
            }
        },

        async fetchTags() {
            try {
                const response = await api.getTags()
                this.tags = response.data
            } catch (error) {
                console.error('Error fetching tags:', error)
            }
        },

        async createItem(data) {
            try {
                await api.createItem(data)
                await this.fetchAllItems()
                return true
            } catch (error) {
                this.error = error.message
                console.error('Error creating item:', error)
                return false
            }
        },

        async updateItem(id, data) {
            try {
                await api.updateItem(id, data)
                await this.fetchAllItems()
                return true
            } catch (error) {
                this.error = error.message
                console.error('Error updating item:', error)
                return false
            }
        },

        async deleteItem(id) {
            try {
                await api.deleteItem(id)
                await this.fetchAllItems()
                return true
            } catch (error) {
                this.error = error.message
                console.error('Error deleting item:', error)
                return false
            }
        },

        async suggestTags(itemData) {
            try {
                const response = await api.suggestTags(itemData)
                return response.data
            } catch (error) {
                console.error('Error suggesting tags:', error)
                return { suggested_tag_names: [], existing_tags: [] }
            }
        },

        async createTag(data) {
            try {
                await api.createTag(data)
                await this.fetchTags()
                return true
            } catch (error) {
                console.error('Error creating tag:', error)
                return false
            }
        },

        async createCategory(data) {
            try {
                await api.createCategory(data)
                await this.fetchCategories()
                return true
            } catch (error) {
                console.error('Error creating category:', error)
                return false
            }
        },

        async updateCategory(id, data) {
            try {
                await api.updateCategory(id, data)
                await this.fetchCategories()
                // Also refresh menu store to update category icons on items
                const menuStore = useMenuStore()
                await menuStore.fetchCategories()
                await menuStore.fetchItems()
                return true
            } catch (error) {
                console.error('Error updating category:', error)
                return false
            }
        },

        async deleteCategory(id) {
            try {
                await api.deleteCategory(id)
                await this.fetchCategories()
                return true
            } catch (error) {
                console.error('Error deleting category:', error)
                return false
            }
        },

        async autoGenerateTags() {
            try {
                const response = await api.autoGenerateTags()
                await this.fetchTags()
                return response.data
            } catch (error) {
                console.error('Error auto-generating tags:', error)
                return null
            }
        },

        async searchDrinkDatabase(query) {
            try {
                const response = await api.searchDrinkDatabase(query)
                return response.data.results
            } catch (error) {
                console.error('Error searching drink database:', error)
                return []
            }
        }
    }
})
