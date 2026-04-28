import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useCompareStore = defineStore('compare', () => {
  const maxItems = 3
  const initialSelectionLimit = 2
  const items = ref(JSON.parse(localStorage.getItem('compareItems') || '[]'))

  const count = computed(() => items.value.length)
  const isFull = computed(() => items.value.length >= maxItems)
  const isInitialSelectionFull = computed(() => items.value.length >= initialSelectionLimit)
  const facilityIds = computed(() => items.value.map(i => i.id))

  function add(id, name) {
    if (has(id) || isFull.value) return
    items.value.push({ id, name })
    persist()
  }

  function remove(id) {
    items.value = items.value.filter(i => i.id !== id)
    persist()
  }

  function toggle(id, name) {
    if (has(id)) remove(id)
    else add(id, name)
  }

  function clear() {
    items.value = []
    persist()
  }

  function has(id) {
    return items.value.some(i => i.id === id)
  }

  function persist() {
    localStorage.setItem('compareItems', JSON.stringify(items.value))
  }

  return {
    items,
    count,
    isFull,
    isInitialSelectionFull,
    maxItems,
    initialSelectionLimit,
    facilityIds,
    add,
    remove,
    toggle,
    clear,
    has
  }
})
