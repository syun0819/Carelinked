<template>
  <header class="header">
    <router-link to="/" class="logo">
      <img :src="logo" alt="CareLinked logo" class="logo-img" />
      <div class="logo-text">
        <div class="brand">CareLinked</div>
        <div class="sub">AUSTRALIA</div>
      </div>
    </router-link>

    <!-- Desktop nav -->
    <nav class="nav">
      <router-link to="/" class="nav-item" active-class="active">Home</router-link>
      <router-link to="/find-bed" class="nav-item" active-class="active">
        Find Care
      </router-link>
      <router-link to="/wait-estimator" class="nav-item" active-class="active">
        Wait Estimator
      </router-link>
      <button class="nav-item nav-link-btn" @click="goToSection('#how-it-works')">
        How It Works
      </button>
      <router-link :to="{ path: '/compare', query: { mode: 'select' } }" class="nav-item" active-class="active">Compare</router-link>
    </nav>

    <!-- Mobile hamburger -->
    <button class="hamburger" @click="menuOpen = !menuOpen" aria-label="Menu">
      <span></span>
      <span></span>
      <span></span>
    </button>

    <!-- Mobile drawer -->
    <div class="mobile-drawer" :class="{ open: menuOpen }">
      <div class="drawer-header">
        <span class="drawer-title">Menu</span>
        <button class="drawer-close" @click="menuOpen = false">✕</button>
      </div>
      <nav class="drawer-nav">
        <router-link to="/" class="drawer-item" @click="menuOpen = false">Home</router-link>
        <router-link to="/find-bed" class="drawer-item" @click="menuOpen = false">Find Care</router-link>
        <router-link to="/wait-estimator" class="drawer-item" @click="menuOpen = false">Wait Estimator</router-link>
        <button class="drawer-item drawer-btn" @click="goToSectionMobile('#how-it-works')">How It Works</button>
        <router-link :to="{ path: '/compare', query: { mode: 'select' } }" class="drawer-item" @click="menuOpen = false">Compare</router-link>
      </nav>
    </div>

    <!-- Overlay -->
    <div class="drawer-overlay" :class="{ open: menuOpen }" @click="menuOpen = false"></div>
  </header>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import logo from '../assets/CareLinkLogo.png'

const router = useRouter()
const menuOpen = ref(false)

function goToSection(hash) {
  router.push({ path: '/', hash })
}

function goToSectionMobile(hash) {
  menuOpen.value = false
  router.push({ path: '/', hash })
}
</script>

<style scoped>
.header {
  position: fixed;
  width: 100%;
  padding: 16px 80px;
  background: white;
  display: flex;
  align-items: center;
  justify-content: space-between;
  box-sizing: border-box;
  z-index: 3000;
  border-bottom: 1px solid #f0ece4;
}

.logo {
  display: flex;
  align-items: center;
  gap: 10px;
  text-decoration: none;
  color: inherit;
}

.logo-img {
  width: 36px;
  height: 36px;
  object-fit: contain;
}

.logo-text {
  display: flex;
  flex-direction: column;
  line-height: 1;
}

.brand {
  font-weight: 700;
  font-size: 16px;
  color: #1f2d2a;
  font-family: var(--font-display);
}

.sub {
  font-size: 8px;
  color: #6f7f78;
  letter-spacing: 1px;
}

.nav {
  display: flex;
  gap: 32px;
}

.nav-item {
  font-size: 15px;
  color: #2D6A5F;
  text-decoration: none;
  cursor: pointer;
  font-family: var(--font-sans);
  background: none;
  border: none;
  padding: 0;
  line-height: 1.2;
}

.nav-item.active {
  color: #1f2d2a;
  font-weight: 600;
}

.nav-link-btn:hover,
.nav-item:hover {
  color: #2f4e44;
}

/* Hamburger */
.hamburger {
  display: none;
  flex-direction: column;
  gap: 5px;
  background: none;
  border: none;
  cursor: pointer;
  padding: 4px;
  z-index: 1100;
}

.hamburger span {
  display: block;
  width: 24px;
  height: 2px;
  background: #1f2d2a;
  border-radius: 2px;
}

/* Mobile drawer */
.mobile-drawer {
  position: fixed;
  top: 0;
  right: -100%;
  width: 75%;
  max-width: 300px;
  height: 100vh;
  background: white;
  z-index: 1200;
  padding: 24px;
  box-sizing: border-box;
  transition: right 0.3s ease;
  box-shadow: -4px 0 20px rgba(0,0,0,0.1);
}

.mobile-drawer.open {
  right: 0;
}

.drawer-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 32px;
}

.drawer-title {
  font-size: 18px;
  font-weight: 700;
  color: #1f2d2a;
  font-family: var(--font-display);
}

.drawer-close {
  background: none;
  border: none;
  font-size: 20px;
  cursor: pointer;
  color: #6f7f78;
  padding: 0;
}

.drawer-nav {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.drawer-item {
  display: block;
  padding: 14px 16px;
  font-size: 16px;
  font-weight: 500;
  color: #1f2d2a;
  text-decoration: none;
  border-radius: 10px;
  font-family: var(--font-sans);
  transition: background 0.2s;
  background: none;
  border: none;
  cursor: pointer;
  text-align: left;
  width: 100%;
}

.drawer-item:hover,
.drawer-item.router-link-active {
  background: #f0ece4;
  color: #2f4e44;
  font-weight: 600;
}

/* Overlay */
.drawer-overlay {
  display: none;
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.3);
  z-index: 1100;
}

.drawer-overlay.open {
  display: block;
}

/* Mobile breakpoint */
@media (max-width: 768px) {
  .header {
    padding: 16px 24px;
  }

  .nav {
    display: none;
  }

  .hamburger {
    display: flex;
  }
}
</style>
