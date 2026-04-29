<template>
  <router-view/>
</template>

<script setup>
import { onMounted, watch, nextTick } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useScrollAnimation } from './composables/useScrollAnimation'

const route = useRoute()
const router = useRouter()
const { observeElements } = useScrollAnimation()

router.afterEach(async () => {
  await nextTick()
  window.scrollTo({ top: 0, behavior: 'instant' })
  setTimeout(observeElements, 300)
})

onMounted(async () => {
  await nextTick()
  window.scrollTo({ top: 0, behavior: 'instant' })
  setTimeout(observeElements, 300)
})
</script>

<style>
.page-animate {
  animation: pageFadeIn 0.6s ease forwards;
}

@keyframes pageFadeIn {
  from {
    opacity: 0;
    transform: translateY(16px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

* {
  box-sizing: border-box;
}

html, body {
  max-width: 100%;
  overflow-x: hidden;
}

.scroll-animate {
  opacity: 0;
  transform: translateY(15px);
  transition: opacity 0.5s ease, transform 0.5s ease;
  will-change: opacity, transform;
}

.scroll-animate.animate-in {
  opacity: 1;
  transform: translateY(0);
}

.scroll-animate:nth-child(2) { transition-delay: 0.1s; }
.scroll-animate:nth-child(3) { transition-delay: 0.2s; }
.scroll-animate:nth-child(4) { transition-delay: 0.3s; }
.scroll-animate:nth-child(5) { transition-delay: 0.4s; }
</style>