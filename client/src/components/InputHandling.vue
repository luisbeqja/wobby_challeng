<template>
  <div class="w-full max-w-2xl mx-0 p-4">
    <div class="card bg-base-100 shadow-xl">
      <div class="card-body">
        <h2 class="card-title text-2xl font-bold mb-4 text-center justify-center">Extract messages</h2>
        
        <div class="form-control w-full mb-6">
          <textarea
            v-model="textInput"
            class="textarea textarea-bordered h-32 w-full"
            placeholder="Paste your conversation here..."
            @paste="handleTextPaste"
            :disabled="isLoading"
          ></textarea>
          <button 
            class="btn btn-primary mt-4 float-right" 
            @click="uploadText"
            :disabled="isLoading || !textInput.trim()"
          >
            <span class="loading loading-spinner" v-if="isLoading"></span>
            {{ isLoading ? 'Processing...' : 'Upload Text' }}
          </button>
        </div>

        <div class="divider">OR</div>

        <div class="form-control w-full">
          <div class="flex items-center space-x-4">
            <input
              type="file"
              accept=".pdf"
              @change="handleFileUpload"
              class="file-input file-input-bordered w-full"
              :disabled="isLoading"
            />
            <button
              class="btn btn-primary"
              @click="uploadFile"
              :disabled="isLoading || !selectedFile"
            >
              <span class="loading loading-spinner" v-if="isLoading"></span>
              {{ isLoading ? 'Processing...' : 'Upload PDF' }}
            </button>
          </div>
          <label class="label" v-if="selectedFile">
            <span class="label-text-alt">Selected file: {{ selectedFile.name }}</span>
          </label>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import router from '../router'
const textInput = ref('')
const selectedFile = ref<File | null>(null)
const isLoading = ref(false)

const handleTextPaste = (event: ClipboardEvent) => {
  const clipboardData = event.clipboardData
  if (clipboardData) {
    const pastedText = clipboardData.getData('text')
    textInput.value = pastedText
    emit('text-input', pastedText)
  }
}

const uploadText = async () => {
    if (!textInput.value.trim()) {
        alert('Please enter some text first')
        return
    }

    isLoading.value = true
    try {
        const response = await fetch('http://localhost:5000/upload/text', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ text: textInput.value })
        })

        if (response.ok) {
            const data = await response.json()
            localStorage.setItem('questionPreviewData', JSON.stringify(data))
            router.push('/question-preview')
            textInput.value = ''
        } else {
            const errorData = await response.json()
            console.error('Error uploading text:', errorData)
            alert('Error uploading text: ' + (errorData.error || response.statusText))
        }
    } catch (error) {
        console.error('Error uploading text:', error)
        alert('Error uploading text. Please try again.')
    } finally {
        isLoading.value = false
    }
}

const handleFileUpload = (event: Event) => {
  const target = event.target as HTMLInputElement;
  const file = target.files ? target.files[0] : null;
  if (file && file.type === 'application/pdf') {
    selectedFile.value = file
  } else {
    alert('Please select a valid PDF file')
    if (event.target) (event.target as HTMLInputElement).value = ''
  }
}

const uploadFile = async () => {
  if (!selectedFile.value) return

  isLoading.value = true
  try {
    const formData = new FormData()
    formData.append('file', selectedFile.value)
    
    const response = await fetch('http://localhost:5000/upload/pdf', {
      method: 'POST',
      body: formData
    })

    if (response.ok) {
      const data = await response.json()
      console.log('File uploaded successfully')
      localStorage.setItem('questionPreviewData', JSON.stringify(data))
      router.push('/question-preview')
      selectedFile.value = null
      const fileInput = document.querySelector('input[type="file"]') as HTMLInputElement
      if (fileInput) fileInput.value = ''
    } else {
      const errorData = await response.json()
      console.error('Error uploading file:', errorData)
      alert('Error uploading file: ' + (errorData.error || response.statusText))
    }
  } catch (error) {
    console.error('Error uploading file:', error)
    alert('Error uploading file. Please try again.')
  } finally {
    isLoading.value = false
  }
}

const emit = defineEmits(['text-input', 'file-upload', 'upload-text', 'upload-success'])
</script>

<style scoped>
.textarea {
  resize: none;
}
</style>
