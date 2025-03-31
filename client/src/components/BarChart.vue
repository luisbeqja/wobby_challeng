<template>
  <div class="p-4">
    <div class="w-full p-4 bg-base-100 rounded-lg shadow-xl">
      <h2 class="text-2xl font-bold mb-4">Questions by Category</h2>
      <div class="w-full h-[400px]">
        <canvas ref="chartRef"></canvas>
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

const questions = ref<Question[]>([]);

onMounted(() => {
  const storedData = localStorage.getItem('questionAnalysisData');
  if (storedData) {
    try {
      const data = JSON.parse(storedData).data;
      console.log(data);
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
  { bg: 'rgba(147, 112, 219, 0.8)', border: 'rgba(147, 112, 219, 1)' }
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
        border: `hsla(${hue}, 70%, 50%, 1)`
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
        backgroundColor: colors.map(c => c.bg),
        borderColor: colors.map(c => c.border),
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
