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
        Find a Bed
      </router-link>
      <a>Wait Time Estimator</a>
      <a>How it Works</a>
    </nav>
  </header>
</template>

<script setup>
import logo from '../assets/CareLinkLogo.png'
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

.nav a {
  font-size: 14px;
  color: #6f7f78;
  text-decoration: none;
  cursor: pointer;
  font-family: 'Inter', sans-serif;
}

.nav a.active {
  color: #1f2d2a;
  font-weight: 500;
}
</style>