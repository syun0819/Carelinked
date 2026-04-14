<template>
  <section class="search-top">
    <div class="search-bar">
      <span class="search-icon">⌕</span>

      <input
        v-model="inputValue"
        class="search-input"
        type="text"
        placeholder="Search by suburb, postcode or region..."
        @keyup.enter="handleSearch"
      />

      <button class="search-btn" @click="handleSearch">
        Search
      </button>
    </div>
  </section>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  modelValue: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['update:modelValue'])

const inputValue = ref(props.modelValue)

watch(
  () => props.modelValue,
  (val) => {
    inputValue.value = val
  }
)

function handleSearch() {
  emit('update:modelValue', inputValue.value)
}
</script>

<style scoped>
.search-top {
  width: 100%;
  max-width: 1000px;
  margin: 0 auto 30px;
  padding: 0 24px;
  display: flex;
  justify-content: center;
}

.search-bar {
  width: 100%;
  max-width: 750px;
  display: flex;
  align-items: center;
  gap: 10px;
  background: white;
  border: 1px solid #ddd8cf;
  border-radius: 10px;
  padding: 6px 16px;
}

.search-icon {
  color: #7b8d87;
  font-size: 30px;
  margin-bottom: 8px;
}

.search-input {
  width: 100%;
  border: none;
  outline: none;
  background: transparent;
  font-size: 15px;
  color: #030303;
}

.search-input::placeholder {
  color: #bec5c2;
}

.search-btn {
  background: #4f6f67;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 13px;
}

.search-btn:hover {
  background: #3f5c55;
}
</style>