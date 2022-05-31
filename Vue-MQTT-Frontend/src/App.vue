<script setup lang="ts">
// https://github.com/vueuse/head
// you can use this to manipulate the document head in any components,
// they will be rendered correctly in the html results with vite-ssg
import { useRouter } from 'vue-router'
import { onMounted, ref } from 'vue'
import { useStorage } from '@vueuse/core'
import { useAuthStore, useStore } from '~/stores/store'
import api from '~/services/service'
const store = useStore()
const authstore = useAuthStore()
const router = useRouter()
useHead({
  title: 'Smartclassroom',
  meta: [
    { name: 'for FHNW Brugg', content: 'Made with love by Etienne Roulet' },
  ],
})

function check_jwt(jwt: any) {
  api.getClassrooms(jwt)
    .then((response) => {
      return response.data
    })
    .then((data) => {
      store.clasrooms_saved = data.results
    })
    .catch((error) => {
      if (error.response.status === 401) {
        localStorage.setItem('django_jwt', '')
        router.push('/login')
      }
      console.log(error.response.data.error)
    })
}
onMounted(() => {
  if (
    authstore.user === ''
    || authstore.user === null
  )
    router.push('/login')

  else if (localStorage.getItem('django_jwt'))
    check_jwt(localStorage.getItem('django_jwt'))
})
router.beforeEach((to, from) => {
  if (to.fullPath.startsWith('/classrooms/')) {
    store.Classrooms = false
    store.Measurements = true
  }
  else {
    store.Classrooms = true
    store.Measurements = false
  }
  if (to.path === '/login') {

  }
  else {
    if (
      !authstore.user
      || authstore.user === null
    )
      router.push('/login')
    else if (authstore.user)
      check_jwt(authstore.user)
  }
})
</script>

<template>
  <Navbar />
  <router-view />
</template>
