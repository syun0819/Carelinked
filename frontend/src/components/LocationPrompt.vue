<template>
  <section class="location-bar">
    <button class="location-btn" @click="requestLocation">
      📍 Use my location
    </button>

    <p v-if="status === 'granted'" class="location-success">
      Showing nearby results
    </p>

    <p v-else-if="status === 'denied'" class="location-error">
      Location access denied. Please enable it in your browser settings.
    </p>

    <p v-else class="location-hint">
      We only use your location to show nearby facilities.
    </p>
  </section>
</template>

<script setup>
import { ref } from 'vue'

const emit = defineEmits(['location-success'])

const status = ref('idle')

function requestLocation() {
  if (!navigator.geolocation) {
    status.value = 'denied'
    return
  }

  navigator.geolocation.getCurrentPosition(
    (position) => {
      status.value = 'granted'

      emit('location-success', {
        lat: position.coords.latitude,
        lng: position.coords.longitude
      })
    },
    () => {
      status.value = 'denied'
    }
  )
}
</script>

<style scoped>
.location-bar {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: 6px;
  margin-top: 14px;
}

.location-btn {
  border: none;
  border-radius: 24px;
  padding: 10px 16px;
  background: #2e7d32;
  color: white;
  cursor: pointer;
  font-weight: 600;
  font-size: 14px;
}

.location-btn:hover {
  background: #1b5e20;
}

.location-hint {
  color: #666;
  font-size: 13px;
  max-width: 320px;
  margin: 0;
}

.location-success {
  color: #2e7d32;
  font-size: 13px;
  margin: 0;
}

.location-error {
  color: #c62828;
  font-size: 13px;
  margin: 0;
}
</style>