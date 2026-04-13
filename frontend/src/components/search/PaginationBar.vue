<template>
  <div class="pagination">

    <!-- 上一頁 -->
    <button
      :disabled="currentPage === 1"
      @click="changePage(currentPage - 1)"
    >
      ‹
    </button>

    <span v-if="visiblePages[0] > 1">...</span>

    <button
      v-for="page in visiblePages"
      :key="page"
      :class="{ 'active-page': page === currentPage }"
      @click="changePage(page)"
    >
      {{ page }}
    </button>

    <span v-if="visiblePages[visiblePages.length - 1] < totalPages">
      ...
    </span>

    <button
      :disabled="currentPage === totalPages"
      @click="changePage(currentPage + 1)"
    >
      ›
    </button>

  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  currentPage: Number,
  pageSize: Number,
  total: Number
})

const emit = defineEmits(['page-change'])

const totalPages = computed(() => {
  return Math.ceil(props.total / props.pageSize)
})

const visiblePages = computed(() => {
  const pages = []
  const maxVisible = 9   

  if (totalPages.value <= maxVisible) {
    for (let i = 1; i <= totalPages.value; i++) {
      pages.push(i)
    }
  } else {
    let start = Math.max(1, props.currentPage - 5)
    let end = Math.min(totalPages.value, props.currentPage + 4)

    if (end - start < maxVisible - 1) {
      if (start === 1) {
        end = start + maxVisible - 1
      } else if (end === totalPages.value) {
        start = end - maxVisible + 1
      }
    }

    for (let i = start; i <= end; i++) {
      pages.push(i)
    }
  }

  return pages
})

function changePage(page) {
  if (page < 1 || page > totalPages.value) return
  emit('page-change', page)
}
</script>

<style scoped>
.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 10px;
  margin-top: 28px;
  flex-wrap: wrap;
}

.pagination button {
  min-width: 44px;
  height: 44px;
  padding: 0 12px;
  border: 1px solid #d8d2c8;
  background: white;
  border-radius: 999px;
  cursor: pointer;
  font-size: 16px;
  font-weight: 500;
  color: #5f6d67;   
  display: flex;
  align-items: center;
  justify-content: center;
}

.pagination button:hover {
  border-color: #8fa298;
}

.pagination button.active-page {
  background: #5d776d;
  color: white;
  border-color: #5d776d;
}

.pagination button:disabled {
  opacity: 0.45;
  cursor: not-allowed;
}

.pagination span {
  color: #5f6d67;
  font-size: 18px;
  padding: 0 4px;
}
</style>