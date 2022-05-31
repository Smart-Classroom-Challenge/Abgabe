<script setup lang="ts">
import { useRouter } from 'vue-router'
const router = useRouter()
onMounted(() => {
  router.push('/classrooms')
})
</script>

<template>
  <div>
    <h1>Index view</h1>
  </div>
</template>

<route lang="yaml">
name: home
meta:
  layout: home
</route>
