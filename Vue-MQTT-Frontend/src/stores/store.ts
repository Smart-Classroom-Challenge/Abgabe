import { defineStore } from 'pinia'
import { useStorage } from '@vueuse/core'

export const useStore = defineStore('store', {
  state: () => ({
    jwt: '',
    jwt_refresh: '',
    search: '',
    show: false,
    showm: false,
    Classrooms: true,
    Measurements: false,
    update_Classrooms: 0,
    update_Station: 0,
    shownotify: false,
    measurementData: [],
    clasrooms_saved: [],
    base_url: import.meta.env.VITE_API_URL,
  }),
  actions: {
    set_jwt(token) {
		  this.$state.jwt = token
    },
    set_rjwt(token) {
		  this.$state.jwt_refresh = token
    },
  },
})

export const useStore2 = defineStore('data', {
  state: () => ({
    measurementData: [],
  }),
})

export const useAuthStore = defineStore('authStore', {
  state: () => {
    return {
      // 'user' = localStorage.user
      // 'guest' = default value
      user: useStorage('django_jwt', import.meta.env.VITE_JWT_STD),
    }
  },
})
