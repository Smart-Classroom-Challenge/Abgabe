<!--
  This example requires Tailwind CSS v2.0+

  This example requires some changes to your config:

  ```
  // tailwind.config.js
  module.exports = {
    // ...
    plugins: [
      // ...
      require('@tailwindcss/forms'),
    ],
  }
  ```
-->

<script lang="ts">
import { useRoute } from 'vue-router'
import { Menu, MenuButton, MenuItem, MenuItems, Popover, PopoverButton, PopoverPanel } from '@headlessui/vue'
import { BellIcon, MenuIcon, SearchIcon, XIcon } from '@heroicons/vue/outline/index.js'
import { useStore } from '~/stores/store'
const user = {
  name: 'Chelsea Hagon',
  email: 'chelsea.hagon@example.com',
  imageUrl:
    'https://images.unsplash.com/photo-1550525811-e5869dd03032?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80',
}
const navigation = [
  { name: 'Dashboard', href: '#', current: true },
  { name: 'Calendar', href: '#', current: false },
  { name: 'Teams', href: '#', current: false },
  { name: 'Directory', href: '#', current: false },
]
const userNavigation = [
  { name: 'Your Profile', href: '#' },
  { name: 'Settings', href: '#' },
  { name: 'Sign out', href: '#' },
]

export default {
  components: {
    Menu,
    MenuButton,
    MenuItem,
    MenuItems,
    Popover,
    PopoverButton,
    PopoverPanel,
    BellIcon,
    MenuIcon,
    SearchIcon,
    XIcon,
  },
  setup() {
    const router = useRouter()
    const route = useRoute()
    const store = useStore()
    const id = route.params.id
    function home() {
      router.push('/')
    }
    function NewMeasurmentStation() {
      store.showm = true
    }
    function NewClassroom() {
      store.show = true
    }

    return {
      id,
      home,
      NewClassroom,
      NewMeasurmentStation,
      user,
      navigation,
      userNavigation,
      store,
    }
  },
}
</script>

<template>
  <client-only>
    <!-- When the mobile menu is open, add `overflow-hidden` to the `body` element to prevent double scrollbars -->
    <Popover v-slot="{ open }" as="template">
      <header :class="[open ? 'fixed inset-0 z-40 overflow-y-auto' : '', 'bg-white dark:bg-dark-800 shadow-sm lg:static lg:overflow-y-visible']">
        <div class="px-4 mx-auto max-w-7xl sm:px-6 lg:px-8">
          <div class="relative flex justify-between xl:grid xl:grid-cols-12 lg:gap-8">
            <div class="flex md:absolute md:left-0 md:inset-y-0 lg:static xl:col-span-2">
              <div class="flex items-center flex-shrink-0">
                <a>
                  <img class="block w-auto h-8" src="/FHNW.png" alt="Workflow" @click="home()">

                </a>
              </div>
            </div>
            <div class="flex-1 min-w-0 md:px-8 lg:px-0 xl:col-span-6">
              <div class="flex items-center px-6 py-4 md:max-w-3xl md:mx-auto lg:max-w-none lg:mx-0 xl:px-0">
                <div class="w-full">
                  <label for="search" class="sr-only">Search</label>
                  <div class="relative">
                    <div class="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none">
                      <SearchIcon class="w-5 h-5 text-gray-400" aria-hidden="true" />
                    </div>
                    <input id="search" v-model="store.search" name="search" class="block w-full py-2 pl-10 pr-3 text-sm placeholder-gray-500 dark:text-white bg-white dark:bg-dark-400 dark:focus:bg-dark-400 border border-gray-300 rounded-md focus:outline-none focus:text-gray-900 focus:placeholder-gray-400 focus:ring-1 focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm" placeholder="Search" type="search">
                  </div>
                </div>
              </div>
            </div>
            <div class="flex items-center md:absolute md:right-0 md:inset-y-0 lg:hidden">
              <!-- Mobile menu button -->
              <PopoverButton class="inline-flex items-center justify-center p-2 -mx-2 text-gray-400 rounded-md hover:bg-gray-100 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-indigo-500">
                <span class="sr-only">Open menu</span>
                <MenuIcon v-if="!open" class="block w-6 h-6" aria-hidden="true" />
                <XIcon v-else class="block w-6 h-6" aria-hidden="true" />
              </PopoverButton>
            </div>
            <div class="hidden lg:flex lg:items-center lg:justify-end xl:col-span-4">
              <a class="flex-shrink-0 p-1 ml-5 text-gray-400 bg-white rounded-full hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">
                <span class="sr-only">View notifications</span>
                <BellIcon class="w-6 h-6" aria-hidden="true" />
              </a>

              <a v-if="store.Classrooms" class="inline-flex items-center px-4 py-2 ml-6 text-sm font-medium text-white bg-indigo-600 border border-transparent rounded-md shadow-sm hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500" @click="NewClassroom()"> New Classroom </a>
              <a v-if="store.Measurements" class="inline-flex items-center px-4 py-2 ml-6 text-sm font-medium text-white bg-indigo-600 border border-transparent rounded-md shadow-sm hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500" @click="NewMeasurmentStation()"> New Station </a>
            </div>
          </div>
        </div>

        <PopoverPanel as="nav" class="lg:hidden" aria-label="Global">
          <div class="max-w-3xl px-2 pt-2 pb-3 mx-auto space-y-1 sm:px-4">
            <a v-for="item in navigation" :key="item.name" :href="item.href" :aria-current="item.current ? 'page' : undefined" :class="[item.current ? 'bg-gray-100 text-gray-900' : 'hover:bg-gray-50', 'block rounded-md py-2 px-3 text-base font-medium']">{{ item.name }}</a>
          </div>
          <div class="pt-4 pb-3 border-t border-gray-200">
            <div class="flex items-center max-w-3xl px-4 mx-auto sm:px-6">
              <div class="flex-shrink-0">
                <img class="w-10 h-10 rounded-full" :src="user.imageUrl" alt="">
              </div>
              <div class="ml-3">
                <div class="text-base font-medium text-gray-800">
                  {{ user.name }}
                </div>
                <div class="text-sm font-medium text-gray-500">
                  {{ user.email }}
                </div>
              </div>
              <button type="button" class="flex-shrink-0 p-1 ml-auto text-gray-400 bg-white rounded-full hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">
                <span class="sr-only">View notifications</span>
                <BellIcon class="w-6 h-6" aria-hidden="true" />
              </button>
            </div>
            <div class="max-w-3xl px-2 mx-auto mt-3 space-y-1 sm:px-4">
              <a v-for="item in userNavigation" :key="item.name" :href="item.href" class="block px-3 py-2 text-base font-medium text-gray-500 rounded-md hover:bg-gray-50 hover:text-gray-900">{{ item.name }}</a>
            </div>
          </div>
        </PopoverPanel>
      </header>
    </Popover>
  </client-only>
</template>
