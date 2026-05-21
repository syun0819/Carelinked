<template>
  <Teleport to="body">
    <div v-if="modelValue" class="modal-overlay" @click.self="closeModal">
      <section class="match-modal" role="dialog" aria-modal="true" :aria-labelledby="titleId">
        <header class="modal-header">
          <button class="close-btn" type="button" aria-label="Close" @click="closeModal">x</button>
          <h2 :id="titleId">{{ step === 'allocate' ? 'What matters most to you?' : 'Review your priorities' }}</h2>
          <p>
            {{ step === 'allocate'
              ? 'You have 100 points to spend across 8 priorities. Spend more on what matters most.'
              : 'Here is how you ranked things. Confirm to find matches, or go back to adjust.' }}
          </p>

          <div class="stepper" aria-label="Matching steps">
            <span class="step-pill active">1</span>
            <span class="step-label" :class="{ active: step === 'allocate' }">Allocate</span>
            <span class="step-divider">></span>
            <span class="step-pill" :class="{ active: step === 'review', done: step === 'review' }">
              {{ step === 'review' ? '2' : '2' }}
            </span>
            <span class="step-label" :class="{ active: step === 'review' }">Review & confirm</span>
          </div>
        </header>

        <div v-if="step === 'allocate'" class="points-panel">
          <div class="points-row">
            <span>Points left to spend</span>
            <strong :class="{ complete: pointsLeft === 0 }">{{ pointsLeft }} / 100 left</strong>
          </div>
          <div class="allocation-bar" aria-label="Allocated priorities">
            <span
              v-for="segment in allocationSegments"
              :key="segment.key"
              class="allocation-segment"
              role="button"
              tabindex="0"
              :title="`${segment.label}: ${segment.points} points`"
              :style="{ width: `${segment.points}%`, backgroundColor: segment.color }"
              @click="jumpToPreference(segment.key)"
              @keydown.enter.prevent="jumpToPreference(segment.key)"
              @keydown.space.prevent="jumpToPreference(segment.key)"
            ></span>
            <span
              v-if="pointsLeft > 0"
              class="allocation-empty"
              :title="`${pointsLeft} points left`"
              :style="{ width: `${pointsLeft}%` }"
            ></span>
          </div>
          <p class="progress-note" :class="{ complete: isValidTotal }">
            {{ allocationMessage }}
          </p>
        </div>

        <div class="modal-body">
          <template v-if="step === 'allocate'">
            <div
              v-for="pref in preferences"
              :key="pref.key"
              class="preference-row"
              :class="{ highlighted: highlightedKey === pref.key }"
              :data-pref-key="pref.key"
              :style="{ '--pref-color': pref.color }"
            >
              <div class="preference-meta">
                <span class="pref-marker">{{ pref.marker }}</span>
                <div class="pref-copy">
                  <span class="pref-label">{{ pref.label }}</span>
                  <span class="pref-status">{{ statusFor(weights[pref.key]) }}</span>
                </div>
                <div class="pref-value">
                  <strong>{{ weights[pref.key] }}</strong>
                  <span>{{ Number(weights[pref.key] || 0) === 1 ? 'point' : 'points' }}</span>
                </div>
              </div>

              <div class="slider-control">
                <button
                  class="step-btn"
                  type="button"
                  :aria-label="`Decrease ${pref.label} points`"
                  :disabled="weights[pref.key] <= 0"
                  @click="adjustWeight(pref.key, -1)"
                >
                  -
                </button>
                <input
                  class="pref-slider"
                  type="range"
                  min="0"
                  max="100"
                  :value="weights[pref.key]"
                  :style="{ '--slider-fill': `${weights[pref.key]}%` }"
                  :aria-label="`${pref.label} points`"
                  @input="handleSliderInput(pref.key, $event)"
                />
                <button
                  class="step-btn"
                  type="button"
                  :aria-label="`Increase ${pref.label} points`"
                  :disabled="weights[pref.key] >= maxFor(pref.key)"
                  @click="adjustWeight(pref.key, 1)"
                >
                  +
                </button>
              </div>
            </div>
          </template>

          <template v-else>
            <div class="review-title-row">
              <h3>Review your priorities</h3>
              <span>Ranked from most to least important</span>
            </div>

            <ol v-if="rankedPreferences.length" class="review-list">
              <li
                v-for="(item, index) in rankedPreferences"
                :key="item.key"
                class="review-item"
                :style="{ '--pref-color': item.color, '--bar-width': `${item.points}%` }"
              >
                <span class="rank">{{ index + 1 }}.</span>
                <span class="pref-marker">{{ item.marker }}</span>
                <span class="review-label">{{ item.label }}</span>
                <span class="review-bar" aria-hidden="true"><span></span></span>
                <strong>{{ item.points }} pts</strong>
              </li>
            </ol>

            <p v-if="skippedPreferences.length" class="skipped-line">
              Skipped:
              <span v-for="(item, index) in skippedPreferences" :key="item.key">
                {{ item.label }}<span v-if="index < skippedPreferences.length - 1">, </span>
              </span>
            </p>
          </template>
        </div>

        <footer class="modal-actions">
          <template v-if="step === 'allocate'">
            <button class="text-btn" type="button" @click="resetWeights">Reset</button>
            <button class="text-btn" type="button" @click="evenSplit">Even split</button>
            <span class="action-spacer"></span>
            <button class="secondary-btn" type="button" @click="closeModal">Cancel</button>
            <button class="primary-btn" type="button" :disabled="!isValidTotal" @click="step = 'review'">
              Review my answers
            </button>
          </template>

          <template v-else>
            <button class="text-btn" type="button" @click="step = 'allocate'">Back to edit</button>
            <span class="action-spacer"></span>
            <button class="secondary-btn" type="button" @click="closeModal">Cancel</button>
            <button class="primary-btn" type="button" @click="confirmWeights">Confirm & Find My Matches</button>
          </template>
        </footer>
      </section>
    </div>
  </Teleport>
</template>

<script setup>
import { computed, reactive, ref, watch } from 'vue'
import { MATCH_PREFERENCES, emptyMatchWeights } from '../../constants/matchPreferences'

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false
  },
  initialWeights: {
    type: Object,
    default: null
  }
})

const emit = defineEmits(['update:modelValue', 'confirm'])

const preferences = MATCH_PREFERENCES
const titleId = 'preference-match-title'
const step = ref('allocate')
const highlightedKey = ref('')
const weights = reactive(emptyMatchWeights())

const totalPoints = computed(() =>
  preferences.reduce((sum, pref) => sum + Number(weights[pref.key] || 0), 0)
)

const pointsLeft = computed(() => 100 - totalPoints.value)
const isValidTotal = computed(() => totalPoints.value === 100)
const allocationMessage = computed(() => {
  if (totalPoints.value === 100) return 'All 100 points spent - ready to review'
  return `Spend ${pointsLeft.value} more points to continue`
})
const allocationSegments = computed(() =>
  preferences
    .map(pref => ({ ...pref, points: Number(weights[pref.key] || 0) }))
    .filter(pref => pref.points > 0)
)

const rankedPreferences = computed(() =>
  preferences
    .map(pref => ({ ...pref, points: Number(weights[pref.key] || 0) }))
    .filter(pref => pref.points > 0)
    .sort((a, b) => b.points - a.points || a.label.localeCompare(b.label))
)

const skippedPreferences = computed(() =>
  preferences
    .map(pref => ({ ...pref, points: Number(weights[pref.key] || 0) }))
    .filter(pref => pref.points === 0)
)

watch(
  () => props.modelValue,
  (isOpen) => {
    if (isOpen) {
      step.value = 'allocate'
      setWeights(props.initialWeights)
    }
  }
)

function setWeights(nextWeights) {
  const defaults = emptyMatchWeights()
  preferences.forEach((pref) => {
    const value = Number(nextWeights?.[pref.key] ?? defaults[pref.key] ?? 0)
    weights[pref.key] = Math.max(0, Math.min(100, Math.round(value)))
  })
}

function updateWeight(key, value) {
  const current = Number(weights[key] || 0)
  const otherTotal = totalPoints.value - current
  const maxAllowed = Math.max(0, 100 - otherTotal)
  const nextValue = Math.max(0, Math.min(maxAllowed, Math.round(Number(value))))
  weights[key] = nextValue
  return nextValue
}

function handleSliderInput(key, event) {
  const nextValue = updateWeight(key, event.target.value)
  event.target.value = nextValue
}

function maxFor(key) {
  const current = Number(weights[key] || 0)
  const otherTotal = totalPoints.value - current
  return Math.max(0, Math.min(100, 100 - otherTotal))
}

function adjustWeight(key, delta) {
  updateWeight(key, Number(weights[key] || 0) + delta)
}

function jumpToPreference(key) {
  const row = document.querySelector(`[data-pref-key="${key}"]`)
  if (!row) return

  row.scrollIntoView({ behavior: 'smooth', block: 'center' })
  highlightedKey.value = key
  window.setTimeout(() => {
    if (highlightedKey.value === key) highlightedKey.value = ''
  }, 1200)
}

function statusFor(value) {
  if (!value) return 'Skip'
  if (value >= 30) return 'Essential'
  if (value >= 15) return 'Important'
  return 'Nice to have'
}

function resetWeights() {
  setWeights(null)
}

function evenSplit() {
  const base = Math.floor(100 / preferences.length)
  let remainder = 100 - base * preferences.length
  preferences.forEach((pref) => {
    weights[pref.key] = base + (remainder > 0 ? 1 : 0)
    remainder -= 1
  })
}

function closeModal() {
  emit('update:modelValue', false)
}

function confirmWeights() {
  if (!isValidTotal.value) return
  const confirmed = preferences.reduce((next, pref) => {
    next[pref.key] = Number(weights[pref.key] || 0)
    return next
  }, {})
  emit('confirm', confirmed)
  closeModal()
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  inset: 0;
  z-index: 5000;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(20, 29, 27, 0.42);
  padding: 18px;
}

.match-modal {
  width: min(1120px, 100%);
  max-height: min(92vh, 980px);
  display: flex;
  flex-direction: column;
  background: #f8f6f1;
  border: 1px solid #ded8ce;
  border-radius: 8px;
  box-shadow: 0 24px 80px rgba(31, 45, 42, 0.35);
  color: #1f2d2a;
  overflow: hidden;
}

.modal-header {
  position: relative;
  padding: 28px 32px 22px;
  border-bottom: 1px solid #e2ddd5;
}

.close-btn {
  position: absolute;
  top: 18px;
  right: 22px;
  border: none;
  background: transparent;
  color: #69746f;
  font-size: 22px;
  line-height: 1;
  cursor: pointer;
}

.modal-header h2 {
  margin: 0 36px 8px 0;
  font-family: var(--font-display);
  font-size: 32px;
  color: #20332f;
}

.modal-header h2::before {
  content: "*";
  margin-right: 12px;
  color: #2d6a5f;
}

.modal-header p {
  max-width: 900px;
  margin: 0 0 22px;
  color: #66736f;
  font-size: 17px;
  line-height: 1.55;
}

.stepper {
  display: flex;
  align-items: center;
  gap: 9px;
  color: #69746f;
  font-size: 14px;
}

.step-pill {
  width: 27px;
  height: 27px;
  border-radius: 50%;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background: #efece6;
  color: #74817c;
  font-size: 13px;
}

.step-pill.active,
.step-pill.done {
  background: #23695e;
  color: #fff;
}

.step-label.active {
  color: #23695e;
  font-weight: 700;
}

.points-panel {
  padding: 24px 32px 28px;
  border-bottom: 1px solid #e2ddd5;
  background: #f5f2ec;
}

.points-row {
  max-width: 620px;
  margin: 0 auto 10px;
  display: flex;
  justify-content: space-between;
  color: #5b6864;
  font-size: 14px;
}

.points-row strong {
  color: #9b521c;
}

.points-row strong.complete {
  color: #168545;
}

.allocation-bar {
  max-width: 620px;
  height: 13px;
  margin: 0 auto;
  border-radius: 999px;
  background: #ece9e2;
  overflow: hidden;
  display: flex;
}

.allocation-segment,
.allocation-empty {
  height: 100%;
  transition: width 0.2s ease;
}

.allocation-segment {
  border: none;
  cursor: pointer;
}

.allocation-segment:hover,
.allocation-segment:focus-visible {
  filter: brightness(0.9);
  outline: 2px solid rgba(31, 45, 42, 0.28);
  outline-offset: -2px;
}

.allocation-empty {
  background: #ece9e2;
}

.progress-note {
  margin: 10px 0 0;
  text-align: center;
  color: #69746f;
  font-size: 14px;
}

.progress-note.complete {
  color: #168545;
}

.modal-body {
  padding: 28px 32px;
  overflow: auto;
}

.preference-row {
  background: #fff;
  border: 1px solid #ded8ce;
  border-radius: 8px;
  padding: 20px 22px 18px;
  margin-bottom: 16px;
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

.preference-row.highlighted {
  border-color: var(--pref-color);
  box-shadow: 0 0 0 3px color-mix(in srgb, var(--pref-color) 22%, transparent);
}

.preference-meta {
  display: grid;
  grid-template-columns: 42px minmax(0, 1fr) auto;
  gap: 14px;
  align-items: center;
  margin-bottom: 16px;
}

.pref-marker {
  width: 30px;
  height: 30px;
  border-radius: 7px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border: 2px solid var(--pref-color);
  color: var(--pref-color);
  font-size: 11px;
  font-weight: 800;
}

.pref-copy {
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.pref-label {
  color: #1f2d2a;
  font-size: 19px;
  font-weight: 700;
}

.pref-status {
  color: #69746f;
  font-size: 14px;
}

.pref-value {
  color: #69746f;
  font-size: 14px;
}

.pref-value strong {
  color: var(--pref-color);
  font-size: 22px;
}

.slider-control {
  display: grid;
  grid-template-columns: 34px minmax(0, 1fr) 34px;
  align-items: center;
  gap: 12px;
}

.step-btn {
  width: 34px;
  height: 34px;
  border-radius: 50%;
  border: 2px solid var(--pref-color);
  background: #fff;
  color: var(--pref-color);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-size: 22px;
  font-weight: 800;
  line-height: 1;
  cursor: pointer;
}

.step-btn:hover:not(:disabled) {
  background: var(--pref-color);
  color: #fff;
}

.step-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
  filter: grayscale(1);
}

.pref-slider {
  width: 100%;
  height: 24px;
  appearance: none;
  background: transparent;
  cursor: pointer;
}

.pref-slider:disabled {
  cursor: not-allowed;
  opacity: 0.55;
  filter: grayscale(1);
}

.pref-slider::-webkit-slider-runnable-track {
  height: 8px;
  border-radius: 999px;
  border: none;
  background: linear-gradient(
    to right,
    var(--pref-color) 0%,
    var(--pref-color) var(--slider-fill),
    #ebe8e2 var(--slider-fill),
    #ebe8e2 100%
  );
}

.pref-slider::-webkit-slider-thumb {
  appearance: none;
  width: 22px;
  height: 22px;
  margin-top: -7px;
  border-radius: 50%;
  border: none;
  background: var(--pref-color);
  box-shadow: 0 1px 4px rgba(31, 45, 42, 0.18);
}

.pref-slider::-moz-range-track {
  height: 8px;
  border-radius: 999px;
  border: none;
  background: #ebe8e2;
}

.pref-slider::-moz-range-progress {
  height: 8px;
  border-radius: 999px;
  background: var(--pref-color);
}

.pref-slider::-moz-range-thumb {
  width: 22px;
  height: 22px;
  border-radius: 50%;
  border: none;
  background: var(--pref-color);
  box-shadow: 0 1px 4px rgba(31, 45, 42, 0.18);
}

.pref-slider:focus-visible {
  outline: 3px solid color-mix(in srgb, var(--pref-color) 32%, transparent);
  outline-offset: 4px;
  border-radius: 999px;
}

.review-title-row {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  gap: 16px;
  margin-bottom: 18px;
}

.review-title-row h3 {
  margin: 0;
  font-size: 21px;
}

.review-title-row span {
  color: #69746f;
  font-size: 14px;
}

.review-list {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.review-item {
  display: grid;
  grid-template-columns: 34px 34px minmax(0, 1fr) minmax(90px, 120px) 70px;
  align-items: center;
  gap: 12px;
  min-height: 58px;
  padding: 0 16px;
  background: #fff;
  border: 1px solid #ded8ce;
  border-radius: 8px;
}

.rank {
  color: #69746f;
  font-weight: 700;
}

.review-label {
  min-width: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  font-size: 18px;
  font-weight: 700;
}

.review-bar {
  height: 8px;
  border-radius: 999px;
  background: #ebe8e2;
  overflow: hidden;
}

.review-bar span {
  display: block;
  width: var(--bar-width);
  height: 100%;
  border-radius: inherit;
  background: var(--pref-color);
}

.review-item strong {
  color: var(--pref-color);
  text-align: right;
}

.skipped-line {
  margin: 16px 0 0;
  color: #66736f;
  font-size: 14px;
}

.modal-actions {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 20px 32px;
  border-top: 1px solid #e2ddd5;
  background: #fbfaf7;
}

.action-spacer {
  flex: 1;
}

.text-btn,
.secondary-btn,
.primary-btn {
  min-height: 48px;
  border-radius: 8px;
  font: inherit;
  font-weight: 700;
  cursor: pointer;
}

.text-btn {
  border: none;
  background: transparent;
  color: #65736e;
  padding: 0 10px;
}

.secondary-btn {
  border: 1px solid #ddd8cf;
  background: #fff;
  color: #1f2d2a;
  padding: 0 24px;
}

.primary-btn {
  border: none;
  background: #23695e;
  color: #fff;
  padding: 0 28px;
}

.primary-btn:disabled {
  opacity: 0.55;
  cursor: not-allowed;
}

@media (max-width: 700px) {
  .modal-overlay {
    align-items: stretch;
    padding: 0;
  }

  .match-modal {
    max-height: 100vh;
    border-radius: 0;
  }

  .modal-header,
  .points-panel,
  .modal-body,
  .modal-actions {
    padding-left: 18px;
    padding-right: 18px;
  }

  .modal-header h2 {
    font-size: 24px;
  }

  .preference-meta {
    grid-template-columns: 34px minmax(0, 1fr);
  }

  .pref-value {
    grid-column: 2;
  }

  .review-item {
    grid-template-columns: 28px 30px minmax(0, 1fr) 58px;
  }

  .review-bar {
    grid-column: 3 / 5;
  }

  .modal-actions {
    flex-wrap: wrap;
  }

  .action-spacer {
    display: none;
  }

  .secondary-btn,
  .primary-btn {
    flex: 1;
  }
  .review-label {
    white-space: normal;
    overflow: visible;
    text-overflow: unset;
    font-size: 15px;
  }

  .review-item {
    grid-template-columns: 28px 30px 1fr;
    row-gap: 6px;
    padding: 16px;
    margin-bottom: 8px;
  }

  .review-bar {
    grid-column: 2 / 4;
  }

  .review-item strong {
    grid-column: 2 / 4;
    text-align: left;
    font-size: 14px;
  }

  .primary-btn {
    flex: 1 1 100%;
    width: 100%;
  }

  .secondary-btn {
    flex: 1 1 auto;
  }

  .modal-actions {
    gap: 8px;
    padding: 16px 18px;
  }
}
</style>
