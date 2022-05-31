<script setup lang="ts">
import { ref } from 'vue'
import { useStore2 } from '~/stores/store'
const store2 = useStore2()
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
const data = ref([])
const render = ref(true)
store2.$subscribe((mutation, state) => {
  binding.value.push([
    mutation.events[0].newValue.time,
    mutation.events[0].newValue.co2,
  ])
  binding2.value.push([
    mutation.events[0].newValue.time,
    mutation.events[0].newValue.co2,
  ])

  binding3.value.push([
    mutation.events[0].newValue.time,
    mutation.events[0].newValue.temperature,
  ])
  binding4.value.push([
    mutation.events[0].newValue.time,
    mutation.events[0].newValue.temperature,
  ])

  binding5.value.push([
    mutation.events[0].newValue.time,
    mutation.events[0].newValue.motion,
  ])
  binding6.value.push([
    mutation.events[0].newValue.time,
    mutation.events[0].newValue.motion,
  ])

  binding7.value.push([
    mutation.events[0].newValue.time,
    mutation.events[0].newValue.light,
  ])
  binding8.value.push([
    mutation.events[0].newValue.time,
    mutation.events[0].newValue.light,
  ])

  binding9.value.push([
    mutation.events[0].newValue.time,
    mutation.events[0].newValue.humidity,
  ])
  binding10.value.push([
    mutation.events[0].newValue.time,
    mutation.events[0].newValue.humidity,
  ])

  data.value.push(mutation.events[0].newValue)
  refresh.value = refresh.value++
  render.value = !render.value
})
</script>

<template>
  <div v-if="data ">
    <div v-for="elements in data" :keys="elements.time">
      {{ elements }}
    </div>
    <div :key="refresh">
      <div class="grid grid-cols-3 gap-4">
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
  </div>
</template>
