<script lang="ts">
import { onBeforeMount, onMounted, ref } from 'vue'
import { useAuthStore, useStore } from '~/stores/store'
import { useRoute } from '~/plugins/router'
import api from '~/services/service'

export default {
  setup() {
    const router = useRouter()
    const authstore = useAuthStore()
    const store = useStore()

    const searchedIotDevices = ref([]);
    (
      async() => {
        const res = await api.getClassrooms(
          authstore.user,
        )
        searchedIotDevices.value = res.data.results
      })()

    store.$subscribe((mutation, state) => {
      if (mutation && mutation.payload) {
        if (Object.keys(mutation.payload) === ['update_Classrooms']) {
          const res = api
            .getClassrooms(authstore.user)
            .then((res) => {
              searchedIotDevices.value = res.data.results
            }).catch((error) => {
              if (error.response.status == 401) {
                useStorage('django_jwt', '')
                router.push('/login')
              }
              alert(error.response.data.error)
            })
        }
      }
    })

    function goToMessurmentStatitons(name_to: bigint) {
      router.push(`/classrooms/${name_to}/`)
    }
    function goToAllStations() {
      router.push('/classrooms/all/')
    }
    return {
      store,
      searchedIotDevices,
      goToMessurmentStatitons,
      goToAllStations,
    }
  },
}
</script>

<template>
  <client-only>
    <ActionInput />
    <Notificationy />
    <div>
      <h1
        class="flex flex-row items-center justify-center pt-2 text-4xl title"
      >
        Classrooms
      </h1>
      <div class="container px-4 mx-auto my-12 md:px-12">
        <div class="flex flex-wrap -mx-1 lg:-mx-4">
          <!-- Column -->
          <div class="w-full px-1 my-5 md:w-1/2 lg:my-4 lg:px-4 lg:w-1/3">
            <!-- Article -->
            <article
              class="overflow-hidden rounded-lg shadow-lg"
              @click="goToAllStations()"
            >
              <a>
                <img
                  alt="Placeholder"
                  class="block w-full h-auto"
                  src="https://picsum.photos/600/400?random=9999"
                >
              </a>

              <header
                class="flex items-center justify-between p-2 leading-tight md:p-4"
              >
                <h1 class="text-lg">
                  <a
                    class=" no-underline hover:underline"
                  >
                    All Stations
                  </a>
                </h1>
                <p class="text-sm text-grey-darker" />
              </header>

              <footer
                class="flex items-center justify-between p-2 leading-none md:p-4"
              >
                <a
                  class="flex items-center  no-underline hover:underline"
                >
                  <p class="ml-2 text-sm">
                    Show all Measurement Stations
                  </p>
                </a>
                <a
                  class="no-underline text-grey-darker hover:text-red-dark"
                >
                  <span class="hidden">Like</span>
                  <i class="fa fa-heart" />
                </a>
              </footer>
            </article>
          <!-- END Article -->
          </div>
          <!-- Column -->
          <div
            v-for="file in searchedIotDevices"
            :key="file.source"
            class="w-full px-1 my-5 md:w-1/2 lg:my-4 lg:px-4 lg:w-1/3"
          >
            <!-- Article -->
            <article
              class="overflow-hidden rounded-lg shadow-lg"
              @click="goToMessurmentStatitons(file.id)"
            >
              <a>
                <img
                  alt="Placeholder"
                  class="block w-full h-auto"
                  :src="`https://picsum.photos/600/400?random=${file.id}`"
                >
              </a>

              <header
                class="flex items-center justify-between p-2 leading-tight md:p-4"
              >
                <h1 class="text-lg">
                  <a
                    class=" no-underline hover:underline"
                  >
                    {{ file.description }}
                  </a>
                </h1>
                <p class="text-sm text-grey-darker">
                  id: {{ file.id }}
                </p>
              </header>

              <footer
                class="flex items-center justify-between p-2 leading-none md:p-4"
              >
                <a
                  class="flex items-center  no-underline hover:underline"
                >
                  <p class="ml-2 text-sm">
                    Room Number: {{ file.room_number }}
                  </p>
                </a>
                <a
                  class="no-underline text-grey-darker hover:text-red-dark"
                >
                  <span class="hidden">Like</span>
                  <i class="fa fa-heart" />
                </a>
              </footer>
            </article>
          <!-- END Article -->
          </div>
        <!-- END Column -->
        </div>
      </div>
    </div>
  </client-only>
</template>

<route lang="yaml">
name: classroom
</route>
