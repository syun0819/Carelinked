<template>
  <section class="search-top">
    <label class="search-bar">
      <span class="search-icon">⌕</span>
      <input
        class="search-input"
        :value="modelValue"
        type="text"
        placeholder="Search by facility name, suburb, or care type..."
        @input="$emit('update:modelValue', $event.target.value)"
      />
    </label>
  </section>
</template>

<script setup>
defineProps({
  modelValue: {
    type: String,
    default: ''
  }
})

defineEmits(['update:modelValue'])
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
  font-size: 16px;
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
</style>