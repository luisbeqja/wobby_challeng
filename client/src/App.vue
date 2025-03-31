<script setup lang="ts">
import SideMenu from './components/SideMenu.vue'

</script>

<template>
  <div class="flex">
    <SideMenu />
    <div class="flex-1 bg-white min-h-screen">
      <RouterView />
    </div>
  </div>
</template>

<style scoped>
.logo {
  height: 6em;
  padding: 1.5em;
  will-change: filter;
  transition: filter 300ms;
}
.logo:hover {
  filter: drop-shadow(0 0 2em #646cffaa);
}
.logo.vue:hover {
  filter: drop-shadow(0 0 2em #42b883aa);
}
</style>
