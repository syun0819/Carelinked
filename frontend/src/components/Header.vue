<template>
  <header class="header">
    <router-link to="/" class="logo">
      <img :src="logo" alt="CareLink logo" class="logo-img" />
      <div class="logo-text">
        <div class="brand">CareLink</div>
        <div class="sub">VICTORIA</div>
      </div>
    </router-link>

    <nav class="nav">
      <router-link to="/" class="nav-item" active-class="active">Home</router-link>
      <router-link to="/find-bed" class="nav-item" active-class="active">
        Find Care
      </router-link>
      <button class="nav-item nav-link-btn" @click="goToSection('#how-it-works')">
        How It Works
      </button>
    </nav>
  </header>
</template>

<script setup>
import { useRouter } from 'vue-router'
import logo from '../assets/CareLinkLogo.png'

const router = useRouter()

function goToSection(hash) {
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
  z-index: 1000;
}

.logo {
  display: flex;
  align-items: center;
  gap: 10px;
  transform: scale(1.35);
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
  font-weight: 600;
  font-size: 16px;
  color: #1f2d2a;
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
  font-size: 17px;
  color: #6f7f78;
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
</style>
