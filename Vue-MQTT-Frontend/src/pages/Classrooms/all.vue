<script lang="ts">
import { useRoute, useRouter } from 'vue-router'
import { computed, onMounted, reactive, ref } from 'vue'
import { useAuthStore, useStore } from '~/stores/store'

// router get props
export default {
  setup() {
    const store = useStore()
    const authstore = useAuthStore()
    const stations = reactive([])
    const router = useRouter()
    async function getStations(id: any) {
      try {
        const response = await fetch(
          `${store.base_url}/api/MeasurementStations/`,
          {
            method: 'GET',
            headers: {
              'Content-Type': 'application/json',
              'Authorization': `Bearer ${authstore.user}`,
            },
          },
        )
        const data = await response.json()
        data.results.forEach((doc) => {
          fetch(
            `${store.base_url}/api/ConnectionHistory/?fk_measurement_station=${doc.id}&filter_type=latest`,
            {
              method: 'GET',
              headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${authstore.user}`,
              },
            },
          )
            .then(response => response.json())
            .then((jsonResponse) => {
              doc.details = jsonResponse.results[0]

              stations.push(doc)
            }).catch((err) => {
              stations.push(doc)
              alert(err)
            })
        })
      }
      catch (err) {
        // catches errors both in fetch and response.json
        alert(err)
      }
    }

    const searchedProducts = computed(() => {
      return stations.filter((product) => {
        return (
          product.name
            .toLowerCase()
            .includes(store.search.toLowerCase())
        )
      })
    })

    function goTo(id) {
      router.push(`/classrooms/all/DetailsView/${id}`)
    }
    onMounted(async() => {
      getStations()
    })
    return {
      goTo,
      stations,
      searchedProducts,
    }
  },
}
</script>

<template>
  <div>
    <ActionInputM />
    <h1 class="flex flex-row items-center justify-center pt-2 text-4xl title">
      Measurement Stations
    </h1>
    <div class="container px-4 mx-auto my-12 md:px-12">
      <div class="flex flex-wrap -mx-1 lg:-mx-4">
        <div
          v-for="file in searchedProducts"
          :key="file.source"
          class="w-full px-1 my-5 md:w-1/2 lg:my-4 lg:px-4 lg:w-1/3"
          @click="goTo(file.id)"
        >
          <!-- Article -->
          <article class="overflow-hidden rounded-lg shadow-lg">
            <a>
              <img
                alt="Placeholder"
                class="block w-full h-auto"
                :src="`https://picsum.photos/600/400?random=${file.id + 100}`"
              >
            </a>

            <header class="flex items-center justify-between p-2 leading-tight md:p-4">
              <h1 class="text-lg">
                <a class="no-underline hover:underline">{{ file.name }}</a>
              </h1>
              <p class="text-sm text-grey-darker">
                id: {{ file.id }}
              </p>
            </header>

            <header
              v-if="file.details"
              class="flex items-center justify-between p-2 leading-tight md:p-4"
            >
              <h2 class="text-lg">
                <a class="no-underline hover:underline">IP Adresse: {{ file.details.ip_address }}</a>
              </h2>
            </header>
            <div v-if="file.details" class="pl-10 text-left">
              <p>
                Bluethooth Status :
                {{ file.details.bluetooth_connected }}
              </p>
              <p class="text-md text-grey-darker">
                ping_backend: {{ file.details.ping_backend }}
              </p>
              <p>time: {{ file.details.time }}</p>
              <p>
                wlan_signal_strength:
                {{ file.details.wlan_signal_strength }}
              </p>
              <p>ping_broker: {{ file.details.ping_backend }}</p>
              <p>ping_grafana: {{ file.details.ping_grafana }}</p>
            </div>
            <footer class="flex items-center justify-between p-2 leading-none md:p-4">
              <a class="flex items-center no-underline hover:underline">
                <p class="ml-2 text-sm">Room Number: {{ file.fk_classroom }}</p>
              </a>
              <a class="no-underline text-grey-darker hover:text-red-dark">
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
</template>
