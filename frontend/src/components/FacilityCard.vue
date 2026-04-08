<template>
  <div class="facility-card">
    <img
      :src="facility.image_url"
      :alt="facility.service_name"
      class="facility-image"
    />

    <div class="facility-body">
      <div class="card-top">
        <h3 class="facility-name">{{ facility.service_name }}</h3>
        <span class="availability-badge">{{ facility.availability_level }}</span>
      </div>

      <p class="facility-suburb">
        {{ facility.physical_suburb }}, {{ facility.physical_state }}
      </p>

      <p class="facility-type">{{ facility.care_type }}</p>

      <p class="facility-address">
        {{ facility.physical_address }}, {{ facility.physical_post_code }}
      </p>

      <div class="facility-info-row">
        <div class="info-block">
          <span class="info-label">Wait Time</span>
          <span class="info-value wait-time">{{ facility.estimated_wait_time }}</span>
        </div>

        <div class="info-block">
          <span class="info-label">Residential Places</span>
          <span class="info-value">{{ facility.residential_places }}</span>
        </div>
      </div>

      <div class="card-footer">
        <span class="provider-name">{{ facility.provider_name }}</span>
        <button class="view-btn">View Details</button>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  facility: {
    type: Object,
    required: true
  }
})
</script>

<style scoped>
.facility-card {
  background: white;
  border: 1px solid #e3dfd8;
  border-radius: 14px;
  overflow: hidden;
  box-shadow: 0 8px 18px rgba(0, 0, 0, 0.05);
}

.facility-image {
  width: 100%;
  height: 180px;
  object-fit: cover;
  display: block;
}

.facility-body {
  padding: 16px;
}

.card-top {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 12px;
  margin-bottom: 8px;
}

.facility-name {
  margin: 0;
  font-size: 20px;
  line-height: 1.3;
  color: #1f2d2a;
}

.availability-badge {
  background: #e6f1eb;
  color: #5d8b72;
  padding: 4px 10px;
  border-radius: 999px;
  font-size: 12px;
  font-weight: 600;
  white-space: nowrap;
}

.facility-suburb {
  margin: 0 0 6px;
  font-size: 14px;
  color: #5f6d67;
}

.facility-type {
  margin: 0 0 6px;
  font-size: 14px;
  font-weight: 500;
  color: #5d8b72;
}

.facility-address {
  margin: 0 0 16px;
  font-size: 13px;
  color: #8a8f8c;
}

.facility-info-row {
  display: flex;
  gap: 28px;
  margin-bottom: 16px;
}

.info-block {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.info-label {
  font-size: 12px;
  color: #8a8f8c;
}

.info-value {
  font-size: 16px;
  font-weight: 600;
  color: #1f2d2a;
}

.wait-time {
  color: #c9793b;
}

.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
}

.provider-name {
  font-size: 13px;
  color: #5f6d67;
}

.view-btn {
  background: #5d8b72;
  color: white;
  border: none;
  border-radius: 8px;
  padding: 8px 16px;
  font-size: 13px;
  cursor: pointer;
}

.view-btn:hover {
  background: #4c735d;
}
</style>