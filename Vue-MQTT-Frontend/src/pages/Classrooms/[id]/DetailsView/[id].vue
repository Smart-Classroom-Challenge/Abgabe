<script setup lang="ts">
import { onMounted, reactive, ref } from 'vue'
import * as mqtt from 'mqtt/dist/mqtt.min'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore, useStore, useStore2 } from '~/stores/store'
const authstore = useAuthStore()
const store = useStore()
const store2 = useStore2()
const data_show = ref(false)
const show_data = reactive([])
const binding = ref([[]])
const binding2 = ref([[]])

const binding3 = ref([[]])
const binding4 = ref([[]])

const binding5 = ref([[]])
const binding6 = ref([[]])

const binding7 = ref([[]])
const binding8 = ref([[]])

const binding9 = ref([[]])
const binding10 = ref([[]])

const refresh = ref(0)
const render = ref(true)
const router = useRouter()
const path = router.currentRoute.value.fullPath
const arg1 = path.split('/')[2]
const arg2 = path.split('/')[4]
let data_classroom: any
onMounted(async() => {
  const routeid = useRoute().params.id
  const store = useStore()
  const options = {
    // Clean session
    clean: true,
    connectTimeout: 4000,
    // Auth
    clientId: `Frontend${Math.random() * (9999999 - 1) + 2}`,
    username: '8e0v0tanDPfBzeKkuasrarRQUKwN0WQW0EiPXg2oV6NiaossmIKmXp2HYnlO9ZAZ',
    password: '',
  }
  if (arg1 !== 'all') {
    const response = await fetch(
      `${store.base_url}/api/Classrooms/${arg1}`,
      {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${authstore.user}`,
        },
      },
    )
    data_classroom = await response.json()
  }
  else {
    data_classroom = {
      id: 'all',
      name: '+',
    }
  }

  let client: any
  if (store.base_url === 'http://localhost:8000')
    client = mqtt.connect('ws://mqtt.flespi.io:80', options)

  else
    client = mqtt.connect('wss://mqtt.flespi.io:443', options)

  await client.on('connect', () => {
    if (data_classroom) {
      client.subscribe(`fhnw/${data_classroom.name}/${routeid}/measurement`, (err) => {
        if (!err) {
          console.log('Subscribed to : ' + `fhnw/${data_classroom.name}/${routeid}/measurement`)
          if (err)
            alert(err)
        }
      })
    }
  })

  client.on('message', async(topic, message) => {
    debugger

    console.log(`Received message from : ${topic}`)
    const data_gets = await JSON.parse(message)
    show_data.push(data_gets)
    const time = await data_gets.time
    const ts = new Date(time)
    const timeS = ts.toLocaleTimeString()
    const co2 = await data_gets.co2
    const temperature = await data_gets.temperature
    const motion = await data_gets.motion
    const light = await data_gets.light
    const humidity = await data_gets.humidity

    binding.value.push([
      timeS,
      co2,
    ])

    binding2.value.push([
      timeS,
      co2,
    ])

    binding3.value.push([
      timeS,
      temperature,
    ])
    binding4.value.push([
      timeS,
      temperature,
    ])

    binding5.value.push([
      timeS,
      motion,
    ])
    binding6.value.push([
      timeS,
      motion,
    ])

    binding7.value.push([
      timeS,
      light,
    ])
    binding8.value.push([
      timeS,
      light,
    ])

    binding9.value.push([
      timeS,
      humidity,
    ])
    binding10.value.push([
      timeS,
      humidity,
    ])

    data_show.value = true
    refresh.value = refresh.value++
    render.value = !render.value

    // message is Buffer
    // store2.measurementData.push(
    // JSON.parse(message.toString()),
    // )
  })
})

</script>

<template>
  <div v-if="data_show">
    <div :key="refresh">
      <div class="grid grid-cols-3 gap-4">
        <!-- LOL it has some minor issues to be reactive so the v-if does the trick but pretty a anti pattern -->
        <!-- But the big problem is the lib is not compatible with the composition api i guess -->
        <div class="...">
          <h1>Co2</h1>
          <line-chart
            v-if="render"
            :library="{ backgroundColor: '#eee' }"
            :data="binding"
          /><line-chart
            v-if="!render"
            :library="{ backgroundColor: '#eee' }"
            :data="binding2"
          />
        </div>
        <div class="...">
          <h1>temperature</h1>
          <line-chart
            v-if="render"
            :library="{ backgroundColor: '#eee' }"
            :data="binding3"
          />
          <line-chart
            v-if="!render"
            :library="{ backgroundColor: '#eee' }"
            :data="binding4"
          />
        </div>
        <div class="...">
          <h1>motion</h1>
          <line-chart
            v-if="render"
            :library="{ backgroundColor: '#eee' }"
            :data="binding5"
          />
          <line-chart
            v-if="!render"
            :library="{ backgroundColor: '#eee' }"
            :data="binding6"
          />
        </div>

        <div class="...">
          <h1>light</h1>
          <line-chart
            v-if="render"
            :library="{ backgroundColor: '#eee' }"
            :data="binding7"
          />
          <line-chart
            v-if="!render"
            :library="{ backgroundColor: '#eee' }"
            :data="binding8"
          />
        </div>
        <div class="...">
          <h1>humidity</h1>
          <line-chart
            v-if="render"
            :library="{ backgroundColor: '#eee' }"
            :data="binding9"
          />
          <line-chart
            v-if="!render"
            :library="{ backgroundColor: '#eee' }"
            :data="binding10"
          />
        </div>
        <div class="col-span-2 ...">
          07
        </div>
      </div>
    </div>
    <div v-for="elements in show_data" :keys="elements.time">
      {{ elements }}
    </div>
  </div>
</template>
