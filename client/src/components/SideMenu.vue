<template>
  <div class="h-screen w-80  bg-base-100 text-white flex flex-col">
    <div class="p-4">
      <h2 class="text-2xl font-bold mb-8 px-4">🧐 Dynamic FAQ</h2>
    </div>

    <nav class="flex-1">
      <ul class="menu w-full gap-2 p-4">
        <li>
          <router-link 
            to="/" 
            class="flex items-center gap-4 text-white hover:bg-[#1a2332] rounded-lg p-3"
            :class="{ 'bg-[#1a2332]': currentPath === '/' }"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
            </svg>
            Questions
          </router-link>
        </li>
        <li>
          <router-link 
            to="/bar-chart" 
            class="flex items-center gap-4 text-white hover:bg-[#1a2332] rounded-lg p-3"
            :class="{ 'bg-[#1a2332]': currentPath === '/bar-chart' }"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
            </svg>
            Chart
          </router-link>
        </li>
        <li>
          <router-link 
            to="/new-analysis" 
            class="flex items-center gap-4 text-white hover:bg-[#1a2332] rounded-lg p-3"
            :class="{ 'bg-[#1a2332]': currentPath === '/new-analysis' }"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4m6 6v10m6-2a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4" />
            </svg>
            Upload
          </router-link>
        </li>
      </ul>
    </nav>

    <!-- Bottom Section (if needed) -->
    <div class="p-4">
      <p>by Luis for Wobby ♥︎</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

const currentPath = ref(window.location.pathname || '/')

// Update current path when hash changes
onMounted(() => {
  window.addEventListener('hashchange', () => {
    currentPath.value = window.location.hash.slice(1) || '/'
  })
})
</script>

<style scoped>
.router-link-active {
  background-color: #1a2332;
}
</style>
