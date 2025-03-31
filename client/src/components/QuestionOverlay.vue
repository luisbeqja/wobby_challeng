<template>
  <div v-if="modelValue" class="overlay fixed inset-0 z-50 flex items-center justify-center p-4">
    <div class="bg-base-100 rounded-lg shadow-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
      <div class="p-6">
        <div class="flex justify-between items-start mb-4">
          <h2 class="text-2xl font-bold">Question Details</h2>
          <button 
            class="btn btn-ghost btn-sm"
            @click="$emit('update:modelValue', false)"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
            </svg>
          </button>
        </div>

        <div class="space-y-4">
          <div class="prose max-w-none">
            <p class="text-lg">{{ question?.message }}</p>
          </div>

          <div class="flex flex-wrap gap-4 text-sm text-base-content/70">
            <div class="flex items-center gap-2">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clip-rule="evenodd" />
              </svg>
              <span>{{ question?.speaker }}</span>
            </div>
            <div class="flex items-center gap-2">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z" clip-rule="evenodd" />
              </svg>
              <span>{{ question?.timestamp }}</span>
            </div>
            <div class="flex items-center gap-2">
              <div class="badge badge-primary">{{ question?.category }}</div>
            </div>
          </div>

          <div class="flex justify-end gap-2 mt-6">
            <button 
              class="btn btn-primary"
              @click="$emit('update:modelValue', false)"
            >
              Show in chat
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
interface Question {
  message: string;
  speaker: string;
  timestamp: string;
  category: string;
  isConfirmed?: boolean;
}

defineProps<{
  modelValue: boolean;
  question: Question | null;
}>();

defineEmits<{
  (e: 'update:modelValue', value: boolean): void;
}>();
</script> 

<style scoped>  
.overlay {
  background-color: rgba(0, 0, 0, 0.8);
}
</style>