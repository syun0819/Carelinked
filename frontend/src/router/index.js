import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import FindBedPage from '../views/FindBedPage.vue'
import FacilityDetailPage from '../views/FacilityDetailPage.vue'
import PasswordPage from '../views/PasswordPage.vue'

const routes = [
  { path: '/', component: Home },
  { path: '/find-bed', component: FindBedPage},
  {
    path: '/facility/:id',
    name: 'FacilityDetail',
    component: FacilityDetailPage,
    props: true
  },
  { path: '/password', component: PasswordPage }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    }

    if (to.hash) {
      return {
        el: to.hash,
        top: 110,
        behavior: 'smooth'
      }
    }

    return { top: 0 }
  }
})

router.beforeEach((to, _from, next) => {
  const isAuthenticated = localStorage.getItem('authenticated')
  if (!isAuthenticated && to.path !== '/password') {
    next('/password')
  } else {
    next()
  }
})

export default router
