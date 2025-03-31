<template>
  <div class="w-full overflow-x-auto p-4 rounded-lg h-screen">
    <h1 class="text-2xl font-bold mb-4 text-base-100">Questions list</h1>
    <table v-if="questions.length > 0" class="table w-full bg-base-100 p-4 h-full overflow-y-auto">
      <thead>
        <tr>
          <th class="cursor-pointer" @click="sortBy('message')">
            Question
            <span v-if="sortKey === 'message'" class="ml-1">
              {{ sortOrder === 'asc' ? '↑' : '↓' }}
            </span>
          </th>
          <th class="cursor-pointer" @click="sortBy('speaker')">
            Speaker
            <span v-if="sortKey === 'speaker'" class="ml-1">
              {{ sortOrder === 'asc' ? '↑' : '↓' }}
            </span>
          </th>
          <th class="cursor-pointer" @click="sortBy('timestamp')">
            Time
            <span v-if="sortKey === 'timestamp'" class="ml-1">
              {{ sortOrder === 'asc' ? '↑' : '↓' }}
            </span>
          </th>
          <th class="cursor-pointer" @click="sortBy('category')">
            Category
            <span v-if="sortKey === 'category'" class="ml-1">
              {{ sortOrder === 'asc' ? '↑' : '↓' }}
            </span>
          </th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="(question, index) in sortedQuestions"
          :key="index"
          class="hover:bg-base-200 cursor-pointer"
          @click="openQuestion(question)"
        >
          <td class="max-w-md truncate">{{ question.message }}</td>
          <td>{{ question.speaker }}</td>
          <td>{{ question.timestamp }}</td>
          <td>
            <div :class="question.category === 'Other' ? 'badge badge-error' : 'badge badge-primary'">{{ question.category }}</div>
          </td>
        </tr>
      </tbody>
    </table>
    <div v-else class="flex justify-center items-center h-full">
        <router-link to="/new-analysis" class="btn btn-primary">Start new analysis</router-link>
    </div>
    <QuestionOverlay
      v-model="showOverlay"
      :question="selectedQuestion"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import QuestionOverlay from './QuestionOverlay.vue';
import { useRouter } from 'vue-router';

interface Question {
  message: string;
  speaker: string;
  timestamp: string;
  category: string;
  isConfirmed?: boolean;
}

const router = useRouter();
const questions = ref<Question[]>([]);
const emit = defineEmits<{
  (e: 'select', question: Question): void;
}>();

const sortKey = ref<keyof Question>('timestamp');
const sortOrder = ref<'asc' | 'desc'>('asc');
const showOverlay = ref(false);
const selectedQuestion = ref<Question | null>(null);

onMounted(() => {
  const storedData = localStorage.getItem('questionAnalysisData');
  console.log(storedData);
  if (storedData) {
    try {
      const data = JSON.parse(storedData).data;
      questions.value = data.map((q: any) => ({
        ...q,
      }));
    } catch (error) {
      console.error('Error parsing stored data:', error);
      router.push('/');
    }
  } else {
    router.push('/');
  }
});

const sortedQuestions = computed(() => {
  return [...questions.value].sort((a, b) => {
    const aValue = a[sortKey.value] as string;
    const bValue = b[sortKey.value] as string;

    if (sortOrder.value === 'asc') {
      return aValue > bValue ? 1 : -1;
    } else {
      return aValue < bValue ? 1 : -1;
    }
  });
});

const sortBy = (key: keyof Question) => {
  if (sortKey.value === key) {
    sortOrder.value = sortOrder.value === 'asc' ? 'desc' : 'asc';
  } else {
    sortKey.value = key;
    sortOrder.value = 'asc';
  }
};

const openQuestion = (question: Question) => {
  selectedQuestion.value = question;
  showOverlay.value = true;
  emit('select', question);
};
</script>