<template>
  <div class="p-4 h-screen overflow-y-auto">
    <div class="w-full p-4 bg-base-100 rounded-lg shadow-xl">
      <h2 class="text-2xl font-bold mb-4">Questions by Category</h2>
      <div class="w-full h-[400px]">
        <canvas ref="chartRef"></canvas>
      </div>
    </div>

    <button
      v-if="leaderboardData.length === 0"
      class="btn btn-primary fixed bottom-4 right-4"
      @click="fetchLeaderboardData"
      :disabled="isLoading"
    >
      <span class="loading loading-spinner" v-if="isLoading"></span>
      {{ isLoading ? 'Loading...' : 'Get Leaderboard Data' }}
    </button>

    <!-- Leaderboard Section -->
    <div
      v-if="leaderboardData.length > 0 && !isLoading"
      class="w-full p-4 bg-base-100 rounded-lg shadow-xl mt-4"
    >
      <h2 class="text-2xl font-bold">FAQ Leaderboard</h2>
      <p
        class="text-sm text-primary mb-10 cursor-pointer"
        @click="fetchLeaderboardData"
        v-if="!isLoading"
      >
        Refresh Leaderboard
      </p>
      <div v-if="isLoading" class="flex justify-center items-center h-32">
        <div class="loading loading-spinner loading-lg"></div>
      </div>
      <div v-else class="space-y-6">
        <div v-for="(item, index) in leaderboardData" :key="index" class="card bg-base-200">
          <div class="card-body">
            <div class="flex justify-between items-start">
              <div>
                <h3 class="card-title text-lg">
                  {{ item.representative_question }}
                </h3>
                <p class="text-sm text-gray-500">
                  Asked {{ item.question_count - 1}} times
                </p>
              </div>
              <div class="badge badge-primary">{{ index + 1 }}</div>
            </div>
            
            <div v-if="item.example_questions.length > 1" class="mt-4">
              <details class="collapse bg-base-100 border-base-300 border">
                <summary class="collapse-title font-semibold">
                  View Similar Questions ({{ item.example_questions.length - 1 }})
                </summary>
                <div class="collapse-content">
                  <ul class="space-y-2">
                    <li v-for="(example, idx) in item.example_questions.slice(1)" :key="idx" class="text-sm mb-4">
                      {{ example }}
                    </li>
                  </ul>
                </div>
              </details>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue';
import Chart from 'chart.js/auto';
import router from '../router';

interface Question {
  category: string;
  message: string;
  speaker: string;
  timestamp: string;
}

interface LeaderboardItem {
  representative_question: string;
  question_count: number;
  example_questions: string[];
}

const questions = ref<Question[]>([]);
const leaderboardData = ref<LeaderboardItem[]>([]);
const isLoading = ref(true);

const fetchLeaderboardData = async () => {
  isLoading.value = true;
  const response = await fetch('api/leaderboard', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ messages: questions.value }),
  });

  if (response.ok) {
    const result = await response.json();
    leaderboardData.value = result.data;
    localStorage.setItem(
      'leaderboardData',
      JSON.stringify(leaderboardData.value)
    );
  } else {
    console.error('Failed to fetch leaderboard data');
  }
  isLoading.value = false;
};

onMounted(async () => {
  const storedData = localStorage.getItem('questionAnalysisData');
  const storedLeaderboardData = localStorage.getItem('leaderboardData');
  if (storedData) {
    try {
      const data = JSON.parse(storedData).data;
      if (storedLeaderboardData) {
        leaderboardData.value = JSON.parse(storedLeaderboardData);
      }
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
  isLoading.value = false;
});

const chartRef = ref<HTMLCanvasElement | null>(null);
let chart: Chart | null = null;

const colorPalette = [
  { bg: 'rgba(54, 162, 235, 0.8)', border: 'rgba(54, 162, 235, 1)' },
  { bg: 'rgba(255, 99, 132, 0.8)', border: 'rgba(255, 99, 132, 1)' },
  { bg: 'rgba(75, 192, 192, 0.8)', border: 'rgba(75, 192, 192, 1)' },
  { bg: 'rgba(255, 206, 86, 0.8)', border: 'rgba(255, 206, 86, 1)' },
  { bg: 'rgba(153, 102, 255, 0.8)', border: 'rgba(153, 102, 255, 1)' },
  { bg: 'rgba(255, 159, 64, 0.8)', border: 'rgba(255, 159, 64, 1)' },
  { bg: 'rgba(201, 203, 207, 0.8)', border: 'rgba(201, 203, 207, 1)' },
  { bg: 'rgba(255, 99, 71, 0.8)', border: 'rgba(255, 99, 71, 1)' },
  { bg: 'rgba(50, 205, 50, 0.8)', border: 'rgba(50, 205, 50, 1)' },
  { bg: 'rgba(147, 112, 219, 0.8)', border: 'rgba(147, 112, 219, 1)' },
];

// Function to generate colors for any number of categories
const generateColors = (count: number) => {
  const colors = [];
  for (let i = 0; i < count; i++) {
    if (i < colorPalette.length) {
      colors.push(colorPalette[i]);
    } else {
      const hue = (i * 137.5) % 360;
      colors.push({
        bg: `hsla(${hue}, 70%, 60%, 0.8)`,
        border: `hsla(${hue}, 70%, 50%, 1)`,
      });
    }
  }
  return colors;
};

const prepareData = () => {
  const categoryCounts = questions.value.reduce((acc, question) => {
    acc[question.category] = (acc[question.category] || 0) + 1;
    return acc;
  }, {} as Record<string, number>);

  const categories = Object.keys(categoryCounts);
  const colors = generateColors(categories.length);

  return {
    labels: categories,
    datasets: [
      {
        label: 'Number of Questions',
        data: Object.values(categoryCounts),
        backgroundColor: colors.map((c) => c.bg),
        borderColor: colors.map((c) => c.border),
        borderWidth: 1,
      },
    ],
  };
};

onMounted(() => {
  if (chartRef.value) {
    const ctx = chartRef.value.getContext('2d');
    if (ctx) {
      chart = new Chart(ctx, {
        type: 'bar',
        data: prepareData(),
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              position: 'top',
            },
            title: {
              display: true,
              text: 'Questions Distribution by Category',
            },
          },
          scales: {
            y: {
              beginAtZero: true,
              ticks: {
                stepSize: 1,
              },
            },
          },
        },
      });
    }
  }
});

onUnmounted(() => {
  if (chart) {
    chart.destroy();
    chart = null;
  }
});
</script>

<style scoped>
.card {
  transition: transform 0.2s;
}

.card:hover {
  transform: translateY(-2px);
}
</style>
