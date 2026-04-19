<template>
  <div class="skeleton-list">
    <article v-for="n in 4" :key="n" class="skeleton-card">
      <div class="skeleton-image shimmer"></div>

      <div class="skeleton-body">
        <div class="skeleton-top-row">
          <div class="skeleton-main-info">
            <div class="skeleton-line title shimmer"></div>
            <div class="skeleton-line address shimmer"></div>
            <div class="skeleton-tag shimmer"></div>
          </div>
          <div class="skeleton-badge shimmer"></div>
        </div>

        <div class="skeleton-metrics shimmer"></div>

        <div class="skeleton-info-line shimmer"></div>

        <div class="skeleton-footer">
          <div class="skeleton-btn shimmer"></div>
        </div>
      </div>
    </article>
  </div>
</template>

<script setup>
</script>

<style scoped>
@keyframes shimmer {
  0% { background-position: -400px 0; }
  100% { background-position: 400px 0; }
}

.shimmer {
  background: linear-gradient(90deg, #ece8e0 25%, #f5f2ec 50%, #ece8e0 75%);
  background-size: 800px 100%;
  animation: shimmer 1.4s infinite linear;
  border-radius: 6px;
}

.skeleton-list {
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.skeleton-card {
  background: #ffffff;
  border: 1px solid #ddd8cf;
  border-radius: 8px;
  overflow: hidden;
}

.skeleton-image {
  width: 100%;
  height: 160px;
  border-radius: 0;
}

.skeleton-body {
  padding: 14px 20px 0;
}

.skeleton-top-row {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 18px;
  min-height: 100px;
}

.skeleton-main-info {
  flex: 1;
  min-width: 0;
}

.skeleton-line {
  height: 14px;
  margin-bottom: 10px;
}

.skeleton-line.title {
  height: 18px;
  width: 65%;
}

.skeleton-line.address {
  width: 50%;
}

.skeleton-tag {
  height: 24px;
  width: 110px;
  border-radius: 999px;
}

.skeleton-badge {
  flex-shrink: 0;
  width: 90px;
  height: 28px;
  border-radius: 999px;
}

.skeleton-metrics {
  height: 52px;
  margin: 8px 0;
  border-radius: 6px;
}

.skeleton-info-line {
  height: 16px;
  width: 55%;
  margin: 14px 0;
}

.skeleton-footer {
  display: flex;
  justify-content: flex-end;
  padding: 12px 0 14px;
}

.skeleton-btn {
  width: 120px;
  height: 38px;
  border-radius: 999px;
}

@media (max-width: 768px) {
  .skeleton-image {
    height: 180px;
  }

  .skeleton-body {
    padding: 18px 18px 0;
  }
}
</style>
