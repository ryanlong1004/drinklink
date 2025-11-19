import { defineStore } from 'pinia'
import api from '../services/api'

export const useAuthStore = defineStore('auth', {
    state: () => ({
        token: localStorage.getItem('token') || null,
        username: null,
        isAuthenticated: false
    }),

    actions: {
        async login(username, password) {
            try {
                const response = await api.login(username, password)
                this.token = response.data.access_token
                this.username = username
                this.isAuthenticated = true
                localStorage.setItem('token', this.token)
                return true
            } catch (error) {
                console.error('Login error:', error)
                return false
            }
        },

        async verifyToken() {
            if (!this.token) {
                return false
            }

            try {
                const response = await api.verifyToken()
                this.username = response.data.username
                this.isAuthenticated = true
                return true
            } catch (error) {
                this.logout()
                return false
            }
        },

        logout() {
            this.token = null
            this.username = null
            this.isAuthenticated = false
            localStorage.removeItem('token')
        }
    }
})
