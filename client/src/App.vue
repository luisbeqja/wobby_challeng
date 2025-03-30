<script setup lang="ts">
import InputHandling from './components/InputHandling.vue'
import SideMenu from './components/SideMenu.vue'
import QuestionPreview from './components/QuestionPreview.vue'
import { ref } from 'vue'

const showQuestionPreview = ref(false)
const uploadedData = ref(null)

const handleUploadSuccess = (data: any) => {
  uploadedData.value = data
  showQuestionPreview.value = true
}
</script>

<template>
  <div class="flex">
    <SideMenu />
    <div class="flex-1 bg-white min-h-screen">
      <InputHandling 
        v-if="!showQuestionPreview" 
        @upload-success="handleUploadSuccess" 
      />
      <QuestionPreview 
        v-else
        :initial-data="uploadedData"
        @back="showQuestionPreview = false" 
      />
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
