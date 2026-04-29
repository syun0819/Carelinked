import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import FindBedPage from '../views/FindBedPage.vue'
import FacilityDetailPage from '../views/FacilityDetailPage.vue'
import PasswordPage from '../views/PasswordPage.vue'
import WaitEstimatorPage from '../views/WaitEstimatorPage.vue'

const routes = [
  { path: '/', component: Home },
  { path: '/find-bed', component: FindBedPage},
  { path: '/wait-estimator', component: WaitEstimatorPage },
  {
    path: '/facility/:id',
    name: 'FacilityDetail',
    component: FacilityDetailPage,
    props: true
  },
  { path: '/password', component: PasswordPage },
  { path: '/compare', component: () => import('../views/ComparePage.vue') }
]

function scrollToHashTarget(hash, behavior = 'auto') {
  const target = document.querySelector(hash)
  if (!target) return

  const top = target.getBoundingClientRect().top + window.scrollY - 110
  window.scrollTo({
    top,
    behavior
  })
}

function keepHashTargetAligned(hash) {
  const delays = [0, 100, 300, 700, 1200, 2000]

  delays.forEach((delay, index) => {
    setTimeout(() => {
      scrollToHashTarget(hash, index === delays.length - 1 ? 'smooth' : 'auto')
    }, delay)
  })
}

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    }

    if (to.hash) {
      return false
    }

    return { top: 0 }
  }
})

router.afterEach((to) => {
  if (to.hash) {
    keepHashTargetAligned(to.hash)
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
