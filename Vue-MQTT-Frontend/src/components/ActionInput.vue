<script setup lang="ts">
import api from '~/services/service'
import { useAuthStore, useStore } from '~/stores/store'

const store = useStore()
const authstore = useAuthStore()
function create_classroom(Room_name, Room_desc, Room_number) {
  api.create_classroom(authstore.user, { name: Room_name, description: Room_desc, room_number: Room_number })
    .then((res) => {
      store.$patch({
        update_Classrooms: ++store.update_Classrooms,
      })
      store.$state.shownotify = true
      store.show = false
    }).catch((err) => {
      alert(err)
    })
}

function close_modal() {
  store.show = false
}
</script>

<template>
  <div v-if="store.show" class="fixed top-0 left-0 flex items-center justify-center w-full h-full modal">
    <div class="absolute w-full h-full bg-gray-900 opacity-50 modal-overlay" @click.self="close_modal()" />

    <div class="z-50 w-11/12 mx-auto overflow-y-auto bg-white dark:bg-dark-500 rounded shadow-lg modal-container md:max-w-md">
      <div class="px-6 py-4 text-left modal-content">
        <div class="flex items-center justify-center pb-3">
          <p class="text-2xl font-bold text-center">
            Add Classroom
          </p>
        </div>

        <div class="mt-6">
          <!-- <p>Canfirm the deletion of this item</p> -->
          <div>
            <label for="username" class="block text-sm text-gray-800 dark:text-gray-200">Name</label>
            <input v-model="Room_name" type="text" class="block w-full px-4 py-2 mt-2 text-gray-700 bg-white border border-gray-300 rounded-md dark:bg-gray-800 dark:text-gray-300 dark:border-gray-600 focus:border-blue-500 dark:focus:border-blue-500 focus:outline-none focus:ring">
          </div>

          <div class="mt-4">
            <div class="flex items-center justify-between">
              <label for="password" class="block text-sm text-gray-800 dark:text-gray-200">Description</label>
            </div>

            <input v-model="Room_desc" type="text" class="block w-full px-4 py-2 mt-2 text-gray-700 bg-white border border-gray-300 rounded-md dark:bg-gray-800 dark:text-gray-300 dark:border-gray-600 focus:border-blue-500 dark:focus:border-blue-500 focus:outline-none focus:ring">
          </div>

          <div class="mt-4">
            <div class="flex items-center justify-between">
              <label for="password" class="block text-sm text-gray-800 dark:text-gray-200">Room Number</label>
            </div>

            <input v-model="Room_number" type="text" class="block w-full px-4 py-2 mt-2 text-gray-700 bg-white border border-gray-300 rounded-md dark:bg-gray-800 dark:text-gray-300 dark:border-gray-600 focus:border-blue-500 dark:focus:border-blue-500 focus:outline-none focus:ring">
          </div>

          <div class="mt-6 " @click="create_classroom(Room_name, Room_desc, Room_number)">
            <button type="submit" class="flex items-center justify-center w-full px-6 py-2 text-sm font-medium text-white transition-colors duration-200 transform bg-blue-500 rounded-md hover:bg-blue-400 focus:bg-blue-400 focus:outline-none">
              <span class="m-2 text-white">Add Classroom</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
