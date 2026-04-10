import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import FindBedPage from '../views/FindBedPage.vue'

const routes = [
  { path: '/', component: Home },
  { path: '/find-bed', component: FindBedPage}
]

export default createRouter({
  history: createWebHistory(),
  routes
})