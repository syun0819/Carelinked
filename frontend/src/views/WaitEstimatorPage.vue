<template>
  <div class="wait-page">
    <Header />

    <main class="wait-main page-animate">
      <template v-if="!result">
        <section class="wait-intro">
          <div class="wait-kicker">
            <svg viewBox="0 0 24 24" aria-hidden="true">
              <path d="M12 3l1.8 5.2L19 10l-5.2 1.8L12 17l-1.8-5.2L5 10l5.2-1.8L12 3Z" />
              <path d="M5 14l.8 2.2L8 17l-2.2.8L5 20l-.8-2.2L2 17l2.2-.8L5 14Z" />
            </svg>
            Personal Wait Time Estimator
          </div>
          <h1>Answer a few questions</h1>
          <p>
            Based on AIHW open data. Select an answer to continue, or skip any question you prefer not to answer.
          </p>
        </section>

        <section class="insight-grid" aria-label="AIHW wait time context">
          <article
            v-for="insight in estimatorInsights"
            :key="insight.title"
            class="insight-card"
            :class="`insight-${insight.tone}`"
          >
            <div class="insight-icon" aria-hidden="true">
              <svg viewBox="0 0 24 24">
                <template v-if="insight.icon === 'clock'">
                  <circle cx="12" cy="12" r="8" />
                  <path d="M12 7v5l3 2" />
                </template>
                <template v-else-if="insight.icon === 'home'">
                  <path d="M4 11 12 4l8 7v9a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1v-9Z" />
                  <path d="M9 21v-7h6v7" />
                </template>
                <template v-else-if="insight.icon === 'map'">
                  <path d="M9 18 3 21V6l6-3 6 3 6-3v15l-6 3-6-3Z" />
                  <path d="M9 3v15M15 6v15" />
                </template>
                <template v-else>
                  <path d="M12 3l1.8 5.2L19 10l-5.2 1.8L12 17l-1.8-5.2L5 10l5.2-1.8L12 3Z" />
                  <path d="M5 14l.8 2.2L8 17l-2.2.8L5 20l-.8-2.2L2 17l2.2-.8L5 14Z" />
                </template>
              </svg>
            </div>
            <div>
              <h2>{{ insight.title }}</h2>
              <p>{{ insight.copy }}</p>
            </div>
          </article>
        </section>

        <section class="progress-wrap" aria-label="Estimator progress">
          <div class="progress-text">
            <template v-if="!isReviewStep">
              Question {{ currentIndex + 1 }} of {{ questions.length }}
            </template>
            <template v-else>
              Review your answers
            </template>
            <span v-if="answeredCount > 0">· {{ answeredCount }} answered</span>
          </div>
          <div class="progress-dots">
            <button
              v-for="(question, index) in questions"
              :key="question.id"
              class="progress-dot"
              :class="{
                active: index === currentIndex,
                answered: isAnswered(question.id) && index !== currentIndex
              }"
              type="button"
              :aria-label="`Go to question ${index + 1}`"
              @click="goToQuestion(index)"
            >
              <svg v-if="isAnswered(question.id) && index !== currentIndex" viewBox="0 0 24 24" aria-hidden="true">
                <path d="M20 6 9 17l-5-5" />
              </svg>
            </button>
          </div>
        </section>

        <section v-if="!isReviewStep" class="question-card">
          <div class="question-header">
            <div class="question-copy">
              <div class="question-section">{{ currentQuestion.section }}</div>
              <div class="question-title-row">
                <div class="question-icon" aria-hidden="true">
                  <svg viewBox="0 0 24 24">
                    <template v-if="currentQuestion.icon === 'user'">
                      <circle cx="12" cy="8" r="3" />
                      <path d="M6 20v-1a6 6 0 0 1 12 0v1" />
                    </template>
                    <template v-else-if="currentQuestion.icon === 'calendar'">
                      <rect x="4" y="5" width="16" height="15" rx="2" />
                      <path d="M8 3v4M16 3v4M4 10h16" />
                    </template>
                    <template v-else-if="currentQuestion.icon === 'people'">
                      <circle cx="9" cy="8" r="3" />
                      <path d="M3 20v-1a6 6 0 0 1 12 0v1" />
                      <path d="M16 6.5a3 3 0 0 1 0 5" />
                      <path d="M21 20v-1a5 5 0 0 0-3-4.6" />
                    </template>
                    <template v-else-if="currentQuestion.icon === 'globe'">
                      <circle cx="12" cy="12" r="8" />
                      <path d="M4 12h16M12 4a12 12 0 0 1 0 16M12 4a12 12 0 0 0 0 16" />
                    </template>
                    <template v-else-if="currentQuestion.icon === 'map'">
                      <path d="M9 18 3 21V6l6-3 6 3 6-3v15l-6 3-6-3Z" />
                      <path d="M9 3v15M15 6v15" />
                    </template>
                    <template v-else-if="currentQuestion.icon === 'list'">
                      <path d="M9 6h11M9 12h11M9 18h11" />
                      <path d="m4 6 1 1 2-2M4 12l1 1 2-2M4 18l1 1 2-2" />
                    </template>
                    <template v-else-if="currentQuestion.icon === 'home'">
                      <path d="M4 11 12 4l8 7v9a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1v-9Z" />
                      <path d="M9 21v-7h6v7" />
                    </template>
                    <template v-else-if="currentQuestion.icon === 'flag'">
                      <path d="M6 21V4h11l-2 4 2 4H6" />
                    </template>
                    <template v-else-if="currentQuestion.icon === 'hospital'">
                      <rect x="4" y="4" width="16" height="16" rx="2" />
                      <path d="M12 8v8M8 12h8" />
                    </template>
                    <template v-else-if="currentQuestion.icon === 'health'">
                      <path d="M12 21s-7-4.6-9-10a4.8 4.8 0 0 1 8-5 4.8 4.8 0 0 1 8 5c-2 5.4-9 10-9 10Z" />
                    </template>
                    <template v-else>
                      <rect x="6" y="3" width="12" height="18" rx="2" />
                      <path d="M9 8h6M9 12h6M9 16h3" />
                    </template>
                  </svg>
                </div>
                <div>
                  <h2>{{ currentQuestion.title }}</h2>
                  <p>{{ currentQuestion.prompt }}</p>
                </div>
              </div>
            </div>

            <div
              class="tooltip-wrap"
              @mouseenter="openTooltip = currentQuestion.id"
              @mouseleave="closeTooltip"
            >
              <button
                class="info-btn"
                type="button"
                :aria-expanded="openTooltip === currentQuestion.id"
                :aria-label="`Why we ask about ${currentQuestion.title}`"
                @click="toggleTooltip(currentQuestion.id)"
              >
                i
              </button>
              <div v-if="openTooltip === currentQuestion.id" class="tooltip-card">
                <strong>Why we ask</strong>
                <span>{{ currentQuestion.tooltip }}</span>
              </div>
            </div>
          </div>

          <div class="answer-list">
            <button
              v-for="option in currentQuestion.options"
              :key="option.label"
              class="answer-option"
              :class="{ selected: isSelected(currentQuestion.id, option.value) }"
              type="button"
              @click="handleAnswerSelect(currentQuestion, option.value)"
            >
              <span :class="{ muted: option.value === null }">{{ option.label }}</span>
              <span class="radio" aria-hidden="true">
                <span v-if="isSelected(currentQuestion.id, option.value)"></span>
              </span>
            </button>
          </div>
        </section>

        <section v-if="isReviewStep" class="review-card">
          <div class="review-heading">
            <div>
              <div class="question-section">FINAL CHECK</div>
              <h2>Review your answers</h2>
              <p>Answers marked “Prefer not to say” are treated as neutral in the estimate.</p>
            </div>
          </div>

          <div class="review-list">
            <button
              v-for="(question, index) in questions"
              :key="question.id"
              class="review-row"
              type="button"
              @click="goToQuestion(index)"
            >
              <span>
                <strong>{{ question.title }}</strong>
                <small>{{ displayAnswer(question) }}</small>
              </span>
              <svg viewBox="0 0 24 24" aria-hidden="true">
                <path d="M9 18l6-6-6-6" />
              </svg>
            </button>
          </div>
        </section>

        <section class="wizard-actions">
          <button
            class="back-btn"
            type="button"
            :disabled="!isReviewStep && currentIndex === 0"
            @click="previousQuestion"
          >
            <svg viewBox="0 0 24 24" aria-hidden="true">
              <path d="M19 12H5M12 19l-7-7 7-7" />
            </svg>
            Back
          </button>

          <button
            v-if="!isReviewStep && !currentQuestion.required"
            class="skip-btn"
            type="button"
            @click="nextQuestion"
          >
            Skip
          </button>

          <button
            v-else
            class="next-btn"
            type="button"
            :disabled="!allAnswered || submitting"
            @click="submitEstimate"
          >
            {{ submitting ? 'Calculating...' : 'See my estimate' }}
            <svg viewBox="0 0 24 24" aria-hidden="true">
              <path d="M5 12h14M13 6l6 6-6 6" />
            </svg>
          </button>
        </section>

        <p v-if="isReviewStep && !allAnswered" class="completion-hint">
          Answer all questions to see your estimate. Tap a dot above to jump back.
        </p>
        <p v-if="error" class="error-message">{{ error }}</p>
      </template>

      <section v-else class="result-view">
        <div class="wait-kicker">
          <svg viewBox="0 0 24 24" aria-hidden="true">
            <path d="M12 3l1.8 5.2L19 10l-5.2 1.8L12 17l-1.8-5.2L5 10l5.2-1.8L12 3Z" />
            <path d="M5 14l.8 2.2L8 17l-2.2.8L5 20l-.8-2.2L2 17l2.2-.8L5 14Z" />
          </svg>
          Personal Wait Time Estimator
        </div>
        <h1>Your estimated wait time</h1>

        <div class="result-card">
          <div class="result-kicker">
            <svg viewBox="0 0 24 24" aria-hidden="true">
              <circle cx="12" cy="12" r="8" />
              <path d="M12 7v5l3 2" />
            </svg>
            Your personal estimate
          </div>
          <h2>Your wait time is estimated to be</h2>
          <div class="estimate-value" :class="estimateToneClass">{{ estimateText }}</div>
          <div class="estimate-pill" :class="estimateToneClass">{{ outcomeLabel }}</div>
          <p class="result-copy">
            Compared with the AIHW-reported average residential aged care wait of 41 days.
          </p>

          <div class="result-actions">
            <button class="find-btn" type="button" @click="goFindCare">
              <svg viewBox="0 0 24 24" aria-hidden="true">
                <circle cx="11" cy="11" r="7" />
                <path d="m20 20-4-4" />
              </svg>
              Find aged care now
            </button>
            <button class="restart-btn" type="button" @click="startOver">
              <svg viewBox="0 0 24 24" aria-hidden="true">
                <path d="M4 12a8 8 0 1 0 3-6.2" />
                <path d="M4 4v6h6" />
              </svg>
              Start over
            </button>
          </div>

          <p class="result-note">
            This is not an official wait-time decision or guarantee. It is an estimated guide based on AIHW cohort patterns,
            and actual wait times depend on individual circumstances, local availability, assessment details and provider decisions.
            <a href="https://www.aihw.gov.au/reports/aged-care/aged-care-services-access/contents/technical-notes" target="_blank" rel="noreferrer">
              AIHW technical notes
            </a>
          </p>
        </div>
      </section>
    </main>

    <FooterSection />
  </div>
</template>

<script setup>
import { computed, onBeforeUnmount, ref } from 'vue'
import { useRouter } from 'vue-router'
import Header from '../components/Header.vue'
import FooterSection from '../components/FooterSection.vue'
import { estimateWaitTime } from '../services/facilitiesApi'

const PREFER_NOT_TO_SAY = null
const AUTO_ADVANCE_DELAY_MS = 180

const OUTCOME_DISPLAY = {
  less_than_median: {
    text: 'Likely less than average',
    label: 'Estimated shorter wait',
    tone: 'tone-shorter'
  },
  around_median: {
    text: 'Likely around average',
    label: 'Estimated average wait',
    tone: 'tone-average'
  },
  more_than_median: {
    text: 'Likely more than average',
    label: 'Estimated longer wait',
    tone: 'tone-longer'
  }
}

const questions = [
  {
    id: 'sex',
    field: 'sex',
    required: true,
    section: 'ABOUT YOU',
    title: 'Gender',
    prompt: 'Which best describes you?',
    icon: 'user',
    tooltip: 'AIHW uses sex recorded in assessment data as male or female. Records marked intersex, indeterminate or unknown were excluded from the AIHW model.',
    options: [
      { label: 'Woman', value: 'Women' },
      { label: 'Man', value: 'Men' }
    ]
  },
  {
    id: 'age',
    field: 'age',
    required: true,
    section: 'ABOUT YOU',
    title: 'Age group',
    prompt: 'What is your age range?',
    icon: 'calendar',
    tooltip: 'Age group is based on age at the first completed comprehensive assessment. AIHW groups ages as 50-69, 70-79, 80-89 and 90 or over.',
    options: [
      { label: '50-69 years', value: '50–69' },
      { label: '70-79 years', value: '70–79' },
      { label: '80-89 years', value: '80–89' },
      { label: '90 years or older', value: '90+' }
    ]
  },
  {
    id: 'first_nations_status',
    field: 'first_nations_status',
    section: 'ABOUT YOU',
    title: 'First Nations status',
    prompt: 'Do you identify as Aboriginal and/or Torres Strait Islander?',
    icon: 'people',
    tooltip: 'First Nations status means whether a person is Aboriginal and/or Torres Strait Islander, as recorded in assessment data.',
    options: [
      { label: 'First Nations', value: 'First Nations' },
      { label: 'Non-Indigenous', value: 'Non-Indigenous' },
      { label: 'Prefer not to say', value: PREFER_NOT_TO_SAY }
    ]
  },
  {
    id: 'cald_status',
    field: 'cald_status',
    required: true,
    section: 'ABOUT YOU',
    title: 'Cultural background',
    prompt: 'Do you identify as culturally and linguistically diverse?',
    icon: 'globe',
    tooltip: 'CALD means culturally and linguistically diverse. In AIHW data this is based on country of birth and preferred language recorded by the assessor.',
    options: [
      { label: 'CALD', value: 'CALD' },
      { label: 'Non-CALD', value: 'Non-CALD' }
    ]
  },
  {
    id: 'country_of_birth',
    field: 'country_of_birth',
    section: 'ABOUT YOU',
    title: 'Country of birth',
    prompt: 'Were you born in Australia?',
    icon: 'globe',
    tooltip: 'Country of birth records whether the person was born in Australia or overseas, based on the country of birth field recorded during assessment.',
    options: [
      { label: 'Born in Australia', value: 'Born in Australia' },
      { label: 'Born overseas', value: 'Born overseas' },
      { label: 'Prefer not to say', value: PREFER_NOT_TO_SAY }
    ]
  },
  {
    id: 'remoteness',
    field: 'remoteness',
    section: 'LOCATION',
    title: 'Location type',
    prompt: 'Which best describes where you live?',
    icon: 'map',
    tooltip: 'Location type uses the Modified Monash Model for the person’s primary address. AIHW groups this as metropolitan, regional centres, or rural and remote areas.',
    options: [
      { label: 'Metropolitan (MM 1)', value: 'Metropolitan (MM 1)' },
      { label: 'Regional centres (MM 2)', value: 'Regional centres (MM 2)' },
      { label: 'Rural and remote (MM 3-7)', value: 'Rural and remote (MM 3–7)' },
      { label: 'Prefer not to say', value: PREFER_NOT_TO_SAY }
    ]
  },
  {
    id: 'aged_care_service_use',
    field: 'aged_care_service_use',
    section: 'CARE HISTORY',
    title: 'Prior aged care use',
    prompt: 'Have you previously used any aged care service?',
    icon: 'list',
    tooltip: 'Prior aged care use means whether the person had used aged care services before their first comprehensive assessment, including home support, home care, respite, residential, transition or restorative care.',
    options: [
      { label: 'Yes, I have used aged care before', value: 'Has previously used aged care services' },
      { label: 'No, this would be my first time', value: 'Has not previously used aged care services' },
      { label: 'Prefer not to say', value: PREFER_NOT_TO_SAY }
    ]
  },
  {
    id: 'caring_arrangement',
    field: 'caring_arrangement',
    required: true,
    section: 'CARE HISTORY',
    title: 'Informal carer',
    prompt: 'Do you have an informal carer, such as family or a friend?',
    icon: 'people',
    tooltip: 'An informal carer is help from a carer, family member, friend or neighbour who is not a paid service provider, as recorded in the NSAF assessment.',
    options: [
      { label: 'Yes, I have an informal carer', value: 'Has an informal carer' },
      { label: 'No, I do not have an informal carer', value: 'Does not have an informal carer' }
    ]
  },
  {
    id: 'living_arrangement',
    field: 'living_arrangement',
    section: 'LIVING SITUATION',
    title: 'Living arrangement',
    prompt: 'Do you live alone?',
    icon: 'home',
    tooltip: 'Living arrangement indicates whether the person lives alone or not, generated from the “lives with” information recorded by the assessor.',
    options: [
      { label: 'I live alone', value: 'Lives alone' },
      { label: 'I do not live alone', value: 'Does not live alone' },
      { label: 'Prefer not to say', value: PREFER_NOT_TO_SAY }
    ]
  },
  {
    id: 'priority_level',
    field: 'priority_level',
    required: true,
    section: 'ASSESSMENT',
    title: 'Priority level',
    prompt: 'What priority level was recorded for your aged care assessment?',
    icon: 'flag',
    tooltip: 'Priority level is the urgency level for the highest approved service. For people approved for both home care and permanent residential care, AIHW uses the permanent residential care priority level.',
    options: [
      { label: 'Low', value: 'Low' },
      { label: 'Medium', value: 'Medium' },
      { label: 'High', value: 'High' }
    ]
  },
  {
    id: 'assessment_location',
    field: 'assessment_location',
    required: true,
    section: 'ASSESSMENT',
    title: 'Assessment location',
    prompt: 'Where was your assessment completed?',
    icon: 'hospital',
    tooltip: 'Assessment location indicates whether the assessment setting was hospital, including public hospitals, private hospitals and clinics.',
    options: [
      { label: 'Assessed in hospital', value: 'Assessed in hospital' },
      { label: 'Assessed outside hospital', value: 'Assessed outside hospital' }
    ]
  },
  {
    id: 'dementia_status',
    field: 'dementia_status',
    section: 'HEALTH',
    title: 'Dementia status',
    prompt: 'Has dementia been recorded as part of your care needs?',
    icon: 'health',
    tooltip: 'Dementia status is based on dementia recorded in assessed or primary health condition fields. AIHW notes these health conditions affect daily living or social participation.',
    options: [
      { label: 'Dementia', value: 'Dementia' },
      { label: 'No dementia', value: 'No dementia' },
      { label: 'Prefer not to say', value: PREFER_NOT_TO_SAY }
    ]
  },
  {
    id: 'mental_health_status',
    field: 'mental_health_status',
    section: 'HEALTH',
    title: 'Mental health condition',
    prompt: 'Do you have a recorded mental health condition?',
    icon: 'health',
    tooltip: 'Mental health condition is based on assessed or primary health condition fields in NSAF. AIHW includes conditions that affect daily living or social participation.',
    options: [
      { label: 'Has a mental health condition', value: 'Has a mental health condition' },
      { label: 'Does not have a mental health condition', value: 'Does not have a mental health condition' },
      { label: 'Prefer not to say', value: PREFER_NOT_TO_SAY }
    ]
  },
  {
    id: 'morbidity',
    field: 'morbidity',
    section: 'HEALTH',
    title: 'Other health conditions',
    prompt: 'Roughly how many other ongoing health conditions do you have?',
    icon: 'clipboard',
    tooltip: 'Other health conditions are counted from primary and assessed health condition records. AIHW groups the count as no or 1, 2-3, 4-5, or 6 or more conditions.',
    options: [
      { label: 'None or 1 condition', value: 'Having no or 1 health conditions' },
      { label: '2-3 conditions', value: 'Having 2–3 health conditions' },
      { label: '4-5 conditions', value: 'Having 4–5 health conditions' },
      { label: '6 or more conditions', value: 'Having 6 health conditions or more' },
      { label: 'Prefer not to say', value: PREFER_NOT_TO_SAY }
    ]
  }
]

const estimatorInsights = [
  {
    title: '41 days',
    copy: 'AIHW reports this as the median elapsed time for people approved for permanent residential aged care only.',
    icon: 'clock',
    tone: 'primary'
  },
  {
    title: '8-9 months',
    copy: 'Median elapsed time is longer for people approved for a home care package.',
    icon: 'home',
    tone: 'green'
  },
  {
    title: 'Location can matter',
    copy: 'For residential aged care only, people in rural or remote areas may wait longer.',
    icon: 'map',
    tone: 'blue'
  },
  {
    title: 'A guide only',
    copy: 'This estimator uses AIHW cohort patterns. Your actual wait depends on local availability and personal circumstances.',
    icon: 'spark',
    tone: 'light'
  }
]

const router = useRouter()
const currentIndex = ref(0)
const reviewing = ref(false)
const answers = ref({})
const openTooltip = ref(null)
const submitting = ref(false)
const error = ref('')
const result = ref(null)
let autoAdvanceTimer = null

const currentQuestion = computed(() => questions[currentIndex.value])
const isLastQuestion = computed(() => currentIndex.value === questions.length - 1)
const answeredCount = computed(() => questions.filter(question => isAnswered(question.id)).length)
const allAnswered = computed(() => answeredCount.value === questions.length)
const isReviewStep = computed(() => reviewing.value)
const resultDisplay = computed(() => OUTCOME_DISPLAY[result.value?.outcome] || OUTCOME_DISPLAY.around_median)

const estimateText = computed(() => (result.value ? resultDisplay.value.text : ''))

const outcomeLabel = computed(() => (result.value ? resultDisplay.value.label : ''))

const estimateToneClass = computed(() => (result.value ? resultDisplay.value.tone : ''))

function isAnswered(questionId) {
  return Object.prototype.hasOwnProperty.call(answers.value, questionId)
}

function isSelected(questionId, value) {
  return isAnswered(questionId) && answers.value[questionId] === value
}

function selectAnswer(questionId, value) {
  answers.value = {
    ...answers.value,
    [questionId]: value
  }
}

function handleAnswerSelect(question, value) {
  selectAnswer(question.id, value)
  error.value = ''

  clearAutoAdvanceTimer()

  autoAdvanceTimer = setTimeout(() => {
    if (result.value || reviewing.value || currentQuestion.value.id !== question.id) return
    advanceFromCurrentQuestion()
  }, AUTO_ADVANCE_DELAY_MS)
}

function getAnswerLabel(question) {
  if (!isAnswered(question.id)) return ''
  const selected = question.options.find(option => option.value === answers.value[question.id])
  return selected?.label || ''
}

function displayAnswer(question) {
  return getAnswerLabel(question) || 'Not answered'
}

function hasPreferNotToSay(question) {
  return question.options.some(option => option.value === PREFER_NOT_TO_SAY)
}

function answerPreferNotToSay(question) {
  if (isAnswered(question.id) || !hasPreferNotToSay(question)) return
  selectAnswer(question.id, PREFER_NOT_TO_SAY)
}

function clearAutoAdvanceTimer() {
  if (autoAdvanceTimer) {
    clearTimeout(autoAdvanceTimer)
    autoAdvanceTimer = null
  }
}

function goToQuestion(index) {
  clearAutoAdvanceTimer()
  currentIndex.value = index
  reviewing.value = false
  openTooltip.value = null
}

function previousQuestion() {
  if (reviewing.value) {
    reviewing.value = false
    currentIndex.value = questions.length - 1
    return
  }

  if (currentIndex.value > 0) {
    goToQuestion(currentIndex.value - 1)
  }
}

function nextQuestion() {
  if (currentQuestion.value.required && !isAnswered(currentQuestion.value.id)) {
    error.value = `Please answer "${currentQuestion.value.title}" before continuing.`
    return
  }

  answerPreferNotToSay(currentQuestion.value)
  error.value = ''
  advanceFromCurrentQuestion()
}

function advanceFromCurrentQuestion() {
  if (currentIndex.value < questions.length - 1) {
    goToQuestion(currentIndex.value + 1)
  } else {
    clearAutoAdvanceTimer()
    reviewing.value = true
    openTooltip.value = null
  }
}

function toggleTooltip(questionId) {
  openTooltip.value = openTooltip.value === questionId ? null : questionId
}

function closeTooltip() {
  openTooltip.value = null
}

function buildPayload() {
  return questions.reduce((payload, question) => {
    const value = answers.value[question.id]
    payload[question.field] = value === PREFER_NOT_TO_SAY ? null : value
    return payload
  }, {})
}

async function submitEstimate() {
  if (!allAnswered.value || submitting.value) return

  clearAutoAdvanceTimer()
  submitting.value = true
  error.value = ''

  try {
    result.value = await estimateWaitTime(buildPayload())
    window.scrollTo({ top: 0, behavior: 'smooth' })
  } catch (err) {
    console.error('Failed to estimate wait time:', err)
    if (err?.message === 'Failed to fetch') {
      error.value = 'Unable to reach the wait-time service. Please make sure the backend is running and try again.'
    } else {
      error.value = err?.message
      ? `Unable to calculate your estimate right now. ${err.message}`
      : 'Unable to calculate your estimate right now. Please try again.'
    }
  } finally {
    submitting.value = false
  }
}

function startOver() {
  clearAutoAdvanceTimer()
  answers.value = {}
  currentIndex.value = 0
  reviewing.value = false
  result.value = null
  error.value = ''
  openTooltip.value = null
}

function goFindCare() {
  router.push('/find-bed')
}

onBeforeUnmount(() => {
  clearAutoAdvanceTimer()
})
</script>

<style scoped>
.wait-page {
  min-height: 100vh;
  overflow: hidden;
  background: #f7f4ee;
  color: #22332e;
  overflow-x: hidden;
}

.wait-main {
  width: min(100%, 1120px);
  margin: 0 auto;
  padding: 132px 24px 58px;
  box-sizing: border-box;
}

.wait-intro,
.result-view {
  text-align: center;
}

.wait-kicker,
.result-kicker {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  border-radius: 999px;
  background: #e7ebe6;
  color: #25665b;
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  padding: 8px 16px;
}

.wait-kicker svg,
.result-kicker svg {
  width: 16px;
  height: 16px;
  fill: none;
  stroke: currentColor;
  stroke-width: 1.8;
  stroke-linecap: round;
  stroke-linejoin: round;
}

.wait-intro h1,
.result-view h1 {
  margin: 18px 0 14px;
  font-family: var(--font-display);
  font-size: 44px;
  font-weight: 800;
  line-height: 1.08;
  color: #1f2d2a;
}

.wait-intro p {
  max-width: 760px;
  margin: 0 auto;
  color: #687777;
  font-size: 18px;
  line-height: 1.65;
}

.insight-grid {
  margin: 42px auto 0;
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 16px;
}

.insight-card {
  min-height: 128px;
  border: 1.5px solid #ddd8cf;
  border-radius: 8px;
  background: #ffffff;
  box-shadow: 0 8px 18px rgba(31, 45, 42, 0.06);
  padding: 20px 18px;
  display: flex;
  align-items: center;
  gap: 14px;
  text-align: left;
  box-sizing: border-box;
}

.insight-card h2 {
  margin: 0;
  font-family: var(--font-display);
  font-size: 24px;
  line-height: 1.1;
  color: #22332e;
}

.insight-card p {
  margin: 8px 0 0;
  font-size: 13px;
  line-height: 1.45;
  color: #5f746f;
}

.insight-icon {
  width: 42px;
  height: 42px;
  color: #4f7d6f;
  flex: 0 0 auto;
  display: flex;
  align-items: center;
  justify-content: center;
}

.insight-icon svg {
  width: 34px;
  height: 34px;
  fill: none;
  stroke: currentColor;
  stroke-width: 1.8;
  stroke-linecap: round;
  stroke-linejoin: round;
}

.insight-primary {
  border-color: #cfded8;
  background: #f8fcfa;
}

.insight-green {
  border-color: #d7e1d1;
  background: #f7faf2;
}

.insight-blue {
  border-color: #cadfe4;
  background: #f5fbfc;
}

.insight-light {
  background: #fbfaf6;
}

.insight-primary .insight-icon,
.insight-primary h2 {
  color: #2d6a5f;
}

.insight-green .insight-icon,
.insight-green h2 {
  color: #4e8133;
}

.insight-blue .insight-icon,
.insight-blue h2 {
  color: #2f7f91;
}

.progress-wrap {
  margin: 56px auto 28px;
  text-align: center;
}

.progress-text {
  color: #617270;
  font-size: 14px;
  margin-bottom: 16px;
}

.progress-text span {
  color: #2d6a5f;
}

.progress-dots {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  flex-wrap: wrap;
}

.progress-dot {
  width: 12px;
  height: 12px;
  border-radius: 999px;
  border: none;
  background: #e2dfd8;
  padding: 0;
  cursor: pointer;
  transition: background 0.15s, transform 0.15s, width 0.15s;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.progress-dot:hover {
  background: #98b5ad;
  transform: translateY(-1px);
}

.progress-dot.active {
  width: 36px;
  background: #2d6a5f;
}

.progress-dot.answered {
  background: #83a29b;
}

.progress-dot svg {
  width: 8px;
  height: 8px;
  fill: none;
  stroke: white;
  stroke-width: 3;
  stroke-linecap: round;
  stroke-linejoin: round;
}

.question-card,
.review-card,
.result-card {
  background: #ffffff;
  border: 1px solid #ddd8cf;
  border-radius: 22px;
  box-shadow: 0 2px 10px rgba(31, 45, 42, 0.06);
  box-sizing: border-box;
}

.question-card,
.review-card {
  --question-icon-size: 58px;
  --question-icon-gap: 20px;
  padding: 48px 56px;
}

.question-header {
  display: flex;
  justify-content: space-between;
  gap: 24px;
  align-items: flex-start;
}

.question-section {
  text-align: left;
  color: #2d6a5f;
  font-size: 12px;
  letter-spacing: 0.32em;
  font-weight: 700;
  margin-bottom: 16px;
}

.question-title-row {
  display: flex;
  align-items: center;
  gap: var(--question-icon-gap);
  text-align: left;
}

.question-icon {
  width: var(--question-icon-size);
  height: var(--question-icon-size);
  border-radius: 16px;
  background: #e8eeee;
  color: #2d6a5f;
  display: flex;
  align-items: center;
  justify-content: center;
  flex: 0 0 auto;
}

.question-icon svg {
  width: 30px;
  height: 30px;
  fill: none;
  stroke: currentColor;
  stroke-width: 1.9;
  stroke-linecap: round;
  stroke-linejoin: round;
}

.question-title-row h2 {
  margin: 0;
  font-family: var(--font-display);
  color: #1f2d2a;
  font-size: 32px;
  line-height: 1.15;
}

.question-title-row p {
  margin: 8px 0 0;
  color: #3f4b4a;
  font-size: 18px;
  line-height: 1.45;
}

.tooltip-wrap {
  position: relative;
  flex: 0 0 auto;
  margin-top: 34px;
}

.info-btn {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  border: 1px solid #ddd8cf;
  background: #f7f6f2;
  color: #657573;
  font-weight: 800;
  cursor: pointer;
  transition: border-color 0.15s, color 0.15s, background 0.15s;
}

.info-btn:hover {
  border-color: #9eb7af;
  color: #2d6a5f;
  background: #eef4f1;
}

.tooltip-card {
  position: absolute;
  right: 0;
  top: 50px;
  width: min(340px, 70vw);
  padding: 18px 20px;
  border-radius: 8px;
  background: white;
  border: 1px solid #ddd8cf;
  box-shadow: 0 10px 24px rgba(31, 45, 42, 0.16);
  z-index: 5;
  text-align: left;
  color: #4f5f5d;
  line-height: 1.55;
  font-size: 14px;
}

.tooltip-card strong {
  display: block;
  margin-bottom: 8px;
  color: #1f2d2a;
  font-size: 15px;
}

.answer-list {
  margin-top: 42px;
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.answer-option {
  min-height: 64px;
  width: 100%;
  border-radius: 14px;
  border: 1.5px solid #dedbd4;
  background: #f8f7f2;
  color: #1f2d2a;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  padding: 0 28px;
  font-size: 18px;
  font-family: var(--font-sans);
  cursor: pointer;
  text-align: left;
  transition: border-color 0.15s, background 0.15s, box-shadow 0.15s;
}

.answer-option:hover {
  border-color: #8fb0a8;
  background: #fbfcf8;
  box-shadow: 0 0 0 1px rgba(45, 106, 95, 0.1);
}

.answer-option.selected {
  border-color: #2d6a5f;
  background: #f1f8f5;
}

.answer-option .muted {
  color: #6f7a78;
  font-style: italic;
}

.radio {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  border: 2px solid #dedbd4;
  background: #faf9f5;
  flex: 0 0 auto;
  display: flex;
  align-items: center;
  justify-content: center;
}

.answer-option.selected .radio {
  border-color: #2d6a5f;
}

.radio span {
  width: 14px;
  height: 14px;
  border-radius: 50%;
  background: #2d6a5f;
}

.review-heading h2 {
  margin: 0;
  font-family: var(--font-display);
  color: #1f2d2a;
  font-size: 32px;
  line-height: 1.15;
}

.review-heading p {
  margin: 8px 0 0;
  color: #536260;
  font-size: 16px;
  line-height: 1.5;
}

.review-list {
  margin-top: 28px;
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px;
}

.review-row {
  min-height: 76px;
  border: 1.5px solid #dedbd4;
  border-radius: 14px;
  background: #f8f7f2;
  color: #1f2d2a;
  padding: 14px 18px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  text-align: left;
  cursor: pointer;
  transition: border-color 0.15s, background 0.15s, box-shadow 0.15s;
}

.review-row:hover {
  border-color: #8fb0a8;
  background: #fbfcf8;
  box-shadow: 0 0 0 1px rgba(45, 106, 95, 0.1);
}

.review-row strong,
.review-row small {
  display: block;
}

.review-row strong {
  font-size: 14px;
  color: #617270;
  margin-bottom: 6px;
}

.review-row small {
  color: #1f2d2a;
  font-size: 15px;
  line-height: 1.35;
}

.review-row svg {
  width: 18px;
  height: 18px;
  fill: none;
  stroke: #2d6a5f;
  stroke-width: 2.3;
  stroke-linecap: round;
  stroke-linejoin: round;
  flex: 0 0 auto;
}

.wizard-actions {
  margin-top: 28px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
}

.back-btn,
.next-btn,
.skip-btn,
.find-btn,
.restart-btn {
  min-height: 50px;
  border-radius: 999px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  padding: 0 28px;
  font-size: 16px;
  font-weight: 600;
  font-family: var(--font-sans);
  cursor: pointer;
  transition: background 0.15s, color 0.15s, border-color 0.15s, opacity 0.15s;
}

.back-btn,
.skip-btn,
.restart-btn {
  border: 1.5px solid #ddd8cf;
  background: #fbfaf6;
  color: #24332f;
}

.back-btn:hover:not(:disabled),
.skip-btn:hover,
.restart-btn:hover {
  border-color: #9eb7af;
  color: #2d6a5f;
}

.next-btn,
.find-btn {
  border: none;
  background: #2d6a5f;
  color: #ffffff;
}

.next-btn:hover:not(:disabled),
.find-btn:hover {
  background: #24584f;
}

.back-btn:disabled,
.next-btn:disabled {
  opacity: 0.45;
  cursor: not-allowed;
}

.next-btn:disabled {
  background: #89aaa2;
}

.back-btn svg,
.next-btn svg,
.skip-btn svg,
.find-btn svg,
.restart-btn svg {
  width: 20px;
  height: 20px;
  fill: none;
  stroke: currentColor;
  stroke-width: 2.4;
  stroke-linecap: round;
  stroke-linejoin: round;
}

.completion-hint,
.error-message {
  margin: 18px 0 0;
  text-align: center;
  font-size: 13px;
  color: #687777;
}

.error-message {
  color: #b94040;
}

.result-view h1 {
  margin-bottom: 54px;
}

.result-card {
  padding: 52px 56px;
  text-align: center;
}

.result-card h2 {
  margin: 24px 0 18px;
  font-family: var(--font-display);
  font-size: 32px;
  color: #1f2d2a;
}

.estimate-value {
  color: #52736b;
  font-family: var(--font-display);
  font-size: 48px;
  line-height: 1.16;
  font-weight: 800;
}

.estimate-value.tone-shorter {
  color: #2f9b67;
}

.estimate-value.tone-average {
  color: #b7791f;
}

.estimate-value.tone-longer {
  color: #bf4f4f;
}

.estimate-pill {
  display: inline-flex;
  margin-top: 18px;
  padding: 10px 20px;
  border-radius: 999px;
  border: 1px solid #c7d5d0;
  background: #f3f6f4;
  color: #52736b;
  font-weight: 700;
}

.estimate-pill.tone-shorter {
  border-color: #b8dac8;
  background: #f0faf5;
  color: #2e9660;
}

.estimate-pill.tone-average {
  border-color: #ead2a6;
  background: #fff8e8;
  color: #a66a17;
}

.estimate-pill.tone-longer {
  border-color: #efc2c2;
  background: #fff1f1;
  color: #ae3f3f;
}

.result-copy {
  margin: 26px auto 0;
  color: #6a7674;
  font-size: 15px;
  line-height: 1.6;
}

.result-actions {
  margin-top: 46px;
  display: flex;
  justify-content: center;
  gap: 16px;
  flex-wrap: wrap;
}

.result-note {
  max-width: 780px;
  margin: 36px auto 0;
  color: #71807d;
  font-size: 12px;
  line-height: 1.6;
}

.result-note a {
  color: #546763;
  text-decoration: underline;
  text-underline-offset: 3px;
}

@media (max-width: 768px) {
  .wait-main {
    padding: 118px 16px 42px;
  }

  .wait-intro h1,
  .result-view h1 {
    font-size: 34px;
  }

  .wait-intro p {
    font-size: 15px;
  }

  .progress-wrap {
    margin-top: 38px;
  }

  .insight-grid {
    grid-template-columns: 1fr;
    margin-top: 30px;
  }

  .insight-card {
    min-height: auto;
    padding: 16px;
  }

  .insight-card h2 {
    font-size: 20px;
  }

  .question-card,
  .review-card,
  .result-card {
    padding: 28px 20px;
    border-radius: 16px;
  }

  .question-copy {
    text-align: left;
  }

  .question-card,
  .review-card {
    --question-icon-size: 50px;
    --question-icon-gap: 14px;
  }

  .question-header {
    gap: 12px;
  }

  .question-icon {
    border-radius: 14px;
  }

  .question-title-row h2 {
    font-size: 26px;
  }

  .question-title-row p {
    font-size: 15px;
  }

  .tooltip-wrap {
    margin-top: 32px;
  }

  .answer-option {
    min-height: 58px;
    padding: 0 18px;
    font-size: 15px;
  }

  .review-heading h2 {
    font-size: 26px;
  }

  .review-heading p {
    font-size: 14px;
  }

  .review-list {
    grid-template-columns: 1fr;
  }

  .wizard-actions {
    align-items: center;
  }

  .back-btn,
  .next-btn,
  .skip-btn {
    padding: 0 20px;
  }

  .estimate-value {
    font-size: 34px;
  }

  .result-card h2 {
    font-size: 25px;
  }
}
</style>
