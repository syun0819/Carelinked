<template>
  <div class="password-page">
    <div class="password-card">
      <div class="logo-row">
        <span class="logo-icon">🌿</span>
        <span class="logo-text">CareLink</span>
      </div>

      <h1 class="title">Welcome</h1>
      <p class="subtitle">Enter the access password to continue.</p>

      <div class="input-group">
        <input
          ref="inputEl"
          v-model="password"
          type="password"
          placeholder="Password"
          class="password-input"
          :class="{ 'input-error': error }"
          @keydown.enter="submit"
        />
      </div>

      <p v-if="error" class="error-text">Incorrect password. Please try again.</p>

      <button class="enter-btn" @click="submit">Enter</button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const password = ref('')
const error = ref(false)
const inputEl = ref(null)

function submit() {
  if (password.value === import.meta.env.VITE_ACCESS_PASSWORD) {
    localStorage.setItem('authenticated', 'true')
    router.push('/')
  } else {
    error.value = true
    password.value = ''
    inputEl.value?.focus()
  }
}
</script>

<style scoped>
.password-page {
  min-height: 100vh;
  background: #f7f4ee;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: var(--font-sans, sans-serif);
}

.password-card {
  background: #ffffff;
  border: 1px solid #ddd8cf;
  border-radius: 16px;
  padding: 48px 40px 40px;
  width: 100%;
  max-width: 400px;
  box-shadow: 0 4px 24px rgba(0, 0, 0, 0.07);
  text-align: center;
}

.logo-row {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  margin-bottom: 28px;
}

.logo-icon {
  font-size: 28px;
}

.logo-text {
  font-size: 22px;
  font-weight: 700;
  color: #2f5d50;
  font-family: var(--font-display, serif);
  letter-spacing: -0.01em;
}

.title {
  margin: 0 0 8px;
  font-size: 26px;
  font-weight: 700;
  color: #24332f;
  font-family: var(--font-display, serif);
}

.subtitle {
  margin: 0 0 28px;
  font-size: 14px;
  color: #6b7e76;
}

.input-group {
  margin-bottom: 12px;
}

.password-input {
  width: 100%;
  padding: 12px 16px;
  font-size: 15px;
  border: 1px solid #ccc8be;
  border-radius: 8px;
  background: #faf9f6;
  color: #24332f;
  outline: none;
  box-sizing: border-box;
  transition: border-color 0.15s;
}

.password-input:focus {
  border-color: #557067;
}

.password-input.input-error {
  border-color: #d64545;
}

.error-text {
  margin: 0 0 16px;
  font-size: 13px;
  color: #d64545;
  font-weight: 500;
}

.enter-btn {
  width: 100%;
  padding: 12px;
  background: #557067;
  color: #ffffff;
  font-size: 15px;
  font-weight: 600;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  margin-top: 4px;
  transition: background 0.15s;
}

.enter-btn:hover {
  background: #486158;
}
</style>
