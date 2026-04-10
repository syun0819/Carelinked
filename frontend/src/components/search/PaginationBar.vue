<template>
  <div class="pagination">
    <button>‹</button>
    <button class="active-page">1</button>
    <button>2</button>
    <button>3</button>
    <button>›</button>
  </div>
</template>

<style scoped>
.pagination {
  display: flex;
  justify-content: center;
  gap: 8px;
  margin-top: 18px;
}

.pagination button {
  border: 1px solid #ddd8cf;
  background: white;
  border-radius: 999px;
  padding: 8px 12px;
  cursor: pointer;
}

.active-page {
  background: #557067 !important;
  color: white;
}
</style>