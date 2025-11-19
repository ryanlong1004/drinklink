import { defineStore } from 'pinia'
import api from '../services/api'

export const useMenuStore = defineStore('menu', {
    state: () => ({
        items: [],
        categories: [],
        tags: [],
        origins: [],
        loading: false,
        error: null,
        filters: {
            categoryId: null,
            tagIds: [],
            origin: null,
            search: '',
            sortBy: 'name',
            sortOrder: 'asc'
        },
        pagination: {
            page: 1,
            pageSize: 20,
            total: 0,
            pages: 0
        }
    }),

    getters: {
        filteredItems: (state) => state.items,

        selectedTags: (state) => {
            return state.tags.filter(tag => state.filters.tagIds.includes(tag.id))
        }
    },

    actions: {
        async fetchItems() {
            this.loading = true
            this.error = null

            try {
                const params = {
                    page: this.pagination.page,
                    page_size: this.pagination.pageSize,
                    category_id: this.filters.categoryId,
                    tag_ids: this.filters.tagIds.join(','),
                    origin: this.filters.origin,
                    search: this.filters.search,
                    sort_by: this.filters.sortBy,
                    sort_order: this.filters.sortOrder,
                    published_only: true
                }

                const response = await api.getItems(params)
                this.items = response.data.items
                this.pagination.total = response.data.total
                this.pagination.pages = response.data.pages
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

        async fetchOrigins() {
            try {
                const response = await api.getOrigins()
                this.origins = response.data.origins
            } catch (error) {
                console.error('Error fetching origins:', error)
            }
        },

        setFilter(key, value) {
            this.filters[key] = value
            this.pagination.page = 1
            this.fetchItems()
        },

        toggleTag(tagId) {
            const index = this.filters.tagIds.indexOf(tagId)
            if (index > -1) {
                this.filters.tagIds.splice(index, 1)
            } else {
                this.filters.tagIds.push(tagId)
            }
            this.pagination.page = 1
            this.fetchItems()
        },

        clearFilters() {
            this.filters = {
                categoryId: null,
                tagIds: [],
                origin: null,
                search: '',
                sortBy: 'name',
                sortOrder: 'asc'
            }
            this.pagination.page = 1
            this.fetchItems()
        },

        setPage(page) {
            this.pagination.page = page
            this.fetchItems()
        }
    }
})
