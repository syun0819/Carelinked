import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import FindBedPage from '../views/FindBedPage.vue'
import FacilityDetailPage from '../views/FacilityDetailPage.vue'

const routes = [
  { path: '/', component: Home },
  { path: '/find-bed', component: FindBedPage},
  {
    path: '/facility/:id',
    name: 'FacilityDetail',
    component: FacilityDetailPage,
    props: true
  }
]

export default createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    }

    return { top: 0 }
  }
})