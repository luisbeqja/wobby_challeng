<template>
  <div class="w-full max-w-2xl mx-0 p-4">
    <div class="question-preview overflow-y-auto card bg-base-100 shadow-xl">
      <div class="card-body">
        <div class="flex justify-between items-center mb-4">
          <h2 class="card-title text-2xl font-bold">Question Preview</h2>
          <button 
            class="btn btn-ghost btn-sm"
            @click="$emit('back')"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M9.707 16.707a1 1 0 01-1.414 0l-6-6a1 1 0 010-1.414l6-6a1 1 0 011.414 1.414L4.414 9H17a1 1 0 110 2H4.414l5.293 5.293a1 1 0 010 1.414z" clip-rule="evenodd" />
            </svg>
            Back
          </button>
        </div>
        
        <!-- Loading State -->
        <div v-if="isLoading" class="flex flex-col items-center justify-center py-12">
          <span class="loading loading-spinner loading-lg"></span>
          <p class="mt-4 text-lg">Processing messages...</p>
        </div>

        <!-- messages List -->
        <div v-else class="space-y-4">
          <div v-for="(question, index) in messages" :key="index" 
               class="border rounded-lg p-4 bg-opacity-50">
            <div class="flex items-start justify-between">
              <div class="flex-1">
                <p class="font-medium">{{ question.message }}</p>
                <div class="mt-2 text-sm opacity-70">
                  <span>Speaker: {{ question.speaker }}</span>
                  <span class="mx-2">|</span>
                  <span>Timestamp: {{ question.timestamp }}</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Empty State -->
          <div v-if="messages.length === 0" class="text-center py-8">
            <p class="text-lg opacity-70">No messages found</p>
          </div>
        </div>

        <!-- Actions -->
        <div class="flex justify-between mt-6">
          <div class="space-x-2">
            <span class="text-sm">{{ messages.length }} total messages</span>
          </div>
          <div class="space-x-2">
            <button 
              class="btn btn-primary"
              @click="analyzeWithAI"
              :disabled="isAnalyzing || messages.length === 0"
            >
              <span class="loading loading-spinner" v-if="isAnalyzing"></span>
              {{ isAnalyzing ? 'Analyzing...' : 'Analyze with AI' }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'

interface Question {
    message: string;
    speaker: string;
    timestamp: string;
    isConfirmed?: boolean;
}

const props = defineProps<{
  initialData: any;
}>()

const messages = ref<Question[]>([])
const isLoading = ref(true)
const isAnalyzing = ref(false)

// Watch for changes in initialData prop
watch(() => props.initialData, (newData) => {
  console.log('Initial data received:', newData)
  if (newData) {
    messages.value = newData.results.map((q: any) => ({
      ...q,
      isConfirmed: false
    }))
    isLoading.value = false
  }
}, { immediate: true })


const analyzeWithAI = async () => {
  if (messages.value.length === 0) return
  
  isAnalyzing.value = true
  try {
    const response = await fetch('http://localhost:5000/analyze', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ messages: messages.value })
    })

    if (response.ok) {
      const data = await response.json()
      messages.value = data.map((q: Question) => ({
        ...q,
        isConfirmed: false
      }))
    } else {
      throw new Error('Failed to analyze messages')
    }
  } catch (error) {
    console.error('Error analyzing messages:', error)
    alert('Error analyzing messages. Please try again.')
  } finally {
    isAnalyzing.value = false
  }
}

defineEmits(['back'])
</script>


<style scoped>
.question-preview {
  max-height: 95vh;
}
</style>