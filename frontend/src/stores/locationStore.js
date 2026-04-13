import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useLocationStore = defineStore('location', () => {
  const userLat = ref(null)
  const userLng = ref(null)
  const locationLoaded = ref(false)
  const locationError = ref('')

  function setLocation(lat, lng) {
    userLat.value = lat
    userLng.value = lng
    locationLoaded.value = true
    locationError.value = ''
  }

  function setLocationError(message) {
    userLat.value = null
    userLng.value = null
    locationLoaded.value = true
    locationError.value = message
  }

  function requestUserLocation() {
    return new Promise((resolve) => {
      if (locationLoaded.value) {
        resolve()
        return
      }

      if (!navigator.geolocation) {
        setLocationError('Geolocation is not supported by your browser.')
        resolve()
        return
      }

      navigator.geolocation.getCurrentPosition(
        (position) => {
          setLocation(position.coords.latitude, position.coords.longitude)
          resolve()
        },
        () => {
          setLocationError('Location access denied. Distance filtering may be unavailable.')
          resolve()
        },
        {
          enableHighAccuracy: true,
          timeout: 10000,
          maximumAge: 300000
        }
      )
    })
  }

  return {
    userLat,
    userLng,
    locationLoaded,
    locationError,
    setLocation,
    setLocationError,
    requestUserLocation
  }
})