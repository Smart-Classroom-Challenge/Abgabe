<!-- This example requires Tailwind CSS v2.0+ -->
<script  lang="ts">
import { ref } from 'vue'
import { CheckCircleIcon } from '@heroicons/vue/outline/index.js'
import { XIcon } from '@heroicons/vue/solid/index.js'
import { useStore } from '~/stores/store'

export default {
  components: {
    CheckCircleIcon,
    XIcon,
  },
  setup() {
    const store = useStore()
    const show = ref(false)
    function close_noti() {
      store.$state.shownotify = false
      show.value = store.$state.shownotify
    }

    watch(() => {
      show.value = store.$state.shownotify
      return store.$state.shownotify
    }, (newVal) => {
      if (newVal)
        show.value = true
    })
    return {
      XIcon,
      CheckCircleIcon,
      close_noti,
      show,
    }
  },
}
</script>

<!-- This example requires Tailwind CSS v2.0+ -->
<template>
  <!-- Global notification live region, render this permanently at the end of the document -->
  <div aria-live="assertive" class="fixed inset-0 flex items-end px-4 py-6 pointer-events-none sm:p-6 sm:items-start">
    <div class="flex flex-col items-center w-full space-y-4 sm:items-end">
      <!-- Notification panel, dynamically insert this into the live region when it needs to be displayed -->
      <transition enter-active-class="transition duration-300 ease-out transform" enter-from-class="translate-y-2 opacity-0 sm:translate-y-0 sm:translate-x-2" enter-to-class="translate-y-0 opacity-100 sm:translate-x-0" leave-active-class="transition duration-100 ease-in" leave-from-class="opacity-100" leave-to-class="opacity-0">
        <div v-if="show" class="w-full max-w-sm overflow-hidden bg-white rounded-lg shadow-lg pointer-events-auto ring-1 ring-black ring-opacity-5">
          <div class="p-4">
            <div class="flex items-start">
              <div class="flex-shrink-0">
                <CheckCircleIcon class="w-6 h-6 text-green-400" aria-hidden="true" />
              </div>
              <div class="ml-3 w-0 flex-1 pt-0.5">
                <p class="text-sm font-medium text-gray-900">
                  Successfully saved!
                </p>
                <p class="mt-1 text-sm text-gray-500">
                  Anyone with a link can now view this file.
                </p>
              </div>
              <div class="flex flex-shrink-0 ml-4">
                <button class="inline-flex text-gray-400 bg-white rounded-md hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500" @click="close_noti()">
                  <span class="sr-only">Close</span>
                  <XIcon class="w-5 h-5" aria-hidden="true" />
                </button>
              </div>
            </div>
          </div>
        </div>
      </transition>
    </div>
  </div>
</template>
