<template>
  <Transition name="bar-slide">
    <div v-if="compareStore.count > 0" class="compare-bar">
      <div class="compare-bar-inner">

        <div class="compare-bar-left">
          <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" class="compare-bar-icon">
            <rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/>
            <rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/>
          </svg>
          <span class="compare-bar-label">
            Compare ({{ compareStore.count }})
            <span v-if="compareStore.count < compareStore.initialSelectionLimit" class="compare-bar-hint">— select at least 2 facilities</span>
          </span>
        </div>

        <div class="compare-bar-chips">
          <span v-for="item in compareStore.items" :key="item.id" class="compare-chip">
            <span class="chip-name">{{ item.name }}</span>
            <button class="chip-remove" @click="compareStore.remove(item.id)" aria-label="Remove">×</button>
          </span>
        </div>

        <div class="compare-bar-right">
          <button class="clear-btn" @click="compareStore.clear()">Clear all</button>
          <button
            class="go-btn"
            :class="{ disabled: compareStore.count < compareStore.initialSelectionLimit }"
            :disabled="compareStore.count < compareStore.initialSelectionLimit"
            @click="goToCompare"
          >
            Compare
            <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
              <path d="M5 12h14M13 6l6 6-6 6"/>
            </svg>
          </button>
        </div>

      </div>
    </div>
  </Transition>

  <!-- Toast notification -->
  <Transition name="toast-fade">
    <div v-if="toastMsg" class="compare-toast">
      <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
        <polyline points="20 6 9 17 4 12"/>
      </svg>
      {{ toastMsg }}
    </div>
  </Transition>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useCompareStore } from '../stores/compareStore'

const compareStore = useCompareStore()
const router = useRouter()

const toastMsg = ref('')
let toastTimer = null
let prevCount = compareStore.count

watch(() => compareStore.count, (newCount) => {
  if (newCount > prevCount) {
    const latest = compareStore.items[compareStore.items.length - 1]
    if (latest) {
      toastMsg.value = `${latest.name} added to compare`
      clearTimeout(toastTimer)
      toastTimer = setTimeout(() => { toastMsg.value = '' }, 2800)
    }
  }
  prevCount = newCount
})

function goToCompare() {
  router.push({ path: '/compare', query: { mode: 'results' } })
}
</script>

<style scoped>
.compare-bar {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  z-index: 2100;
  background: #f5f2ec;
  border-top: 1px solid #ddd8cf;
  box-shadow: 0 -2px 12px rgba(0,0,0,0.08);
}

.compare-bar-inner {
  max-width: 1360px;
  margin: 0 auto;
  padding: 8px 32px;
  display: flex;
  align-items: center;
  gap: 20px;
  flex-wrap: wrap;
}

.compare-bar-icon { color: #4a6659; flex-shrink: 0; }

.compare-bar-left {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-shrink: 0;
}

.compare-bar-label {
  font-size: 14px;
  font-weight: 700;
  color: #22332e;
  white-space: nowrap;
}

.compare-bar-hint {
  font-weight: 400;
  color: #8a9e96;
  font-size: 13px;
}

.compare-bar-chips {
  display: flex;
  gap: 8px;
  flex: 1;
  flex-wrap: wrap;
}

.compare-chip {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: #fff;
  border: 1px solid #ccc7be;
  border-radius: 999px;
  padding: 4px 10px 4px 12px;
  font-size: 13px;
  color: #22332e;
}

.chip-name {
  max-width: 160px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.chip-remove {
  border: none;
  background: transparent;
  color: #8a9e96;
  font-size: 16px;
  cursor: pointer;
  line-height: 1;
  padding: 0;
  display: flex;
  align-items: center;
}
.chip-remove:hover { color: #22332e; }

.compare-bar-right {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-shrink: 0;
}

.clear-btn {
  background: transparent;
  border: none;
  color: #8a9e96;
  font-size: 13px;
  cursor: pointer;
  white-space: nowrap;
}
.clear-btn:hover { color: #22332e; }

.go-btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: #3d6b59;
  color: #fff;
  border: none;
  border-radius: 999px;
  padding: 9px 22px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.15s;
  white-space: nowrap;
}
.go-btn:hover:not(.disabled) { background: #2e5244; }
.go-btn.disabled { background: #c8c2b8; color: #8a9e96; cursor: not-allowed; }

/* Toast */
.compare-toast {
  position: fixed;
  bottom: 76px;
  right: 28px;
  z-index: 2200;
  background: #22332e;
  color: #fff;
  border: 1px solid #3d6b59;
  border-radius: 10px;
  padding: 10px 16px;
  font-size: 13px;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 8px;
  box-shadow: 0 4px 16px rgba(0,0,0,0.2);
}

/* Transitions */
.bar-slide-enter-active,
.bar-slide-leave-active { transition: transform 0.25s ease, opacity 0.25s ease; }
.bar-slide-enter-from,
.bar-slide-leave-to { transform: translateY(100%); opacity: 0; }

.toast-fade-enter-active,
.toast-fade-leave-active { transition: opacity 0.3s ease, transform 0.3s ease; }
.toast-fade-enter-from,
.toast-fade-leave-to { opacity: 0; transform: translateY(8px); }
</style>
