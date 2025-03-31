import { createMemoryHistory, createRouter } from 'vue-router'

import QuestionPreview from './components/QuestionPreview.vue'
import QuestionsTable from './components/QuestionsTable.vue'
import InputHandling from './components/InputHandling.vue'
import BarChart from './components/BarChart.vue'
const routes = [
    { path: '/', component: QuestionsTable },
    { path: '/new-analysis', component: InputHandling },
    { path: '/question-preview', component: QuestionPreview },
    { path: '/bar-chart', component: BarChart },
]

const router = createRouter({
    history: createMemoryHistory(),
    routes,
})

export default router