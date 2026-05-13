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
            Wait time estimator
          </div>
          <h1>Wait Time Estimator</h1>
          <p>
            Get a guided estimate of whether your wait may be shorter, moderate, or longer compared with
            published AIHW residential aged care wait-time patterns.
          </p>
        </section>

        <section class="wait-landing">
          <article class="benchmark-card">
            <div class="benchmark-label">
              <svg viewBox="0 0 24 24" aria-hidden="true">
                <circle cx="12" cy="12" r="8" />
                <path d="M12 7v5l3 2" />
              </svg>
              Key benchmark
            </div>
            <div class="benchmark-value">
              <strong>41</strong>
              <span>days</span>
            </div>
            <p>Median elapsed time for people approved for permanent residential aged care.</p>
            <div class="benchmark-chart" aria-hidden="true">
              <span v-for="bar in benchmarkBars" :key="bar.index" :class="{ median: bar.median }" :style="{ height: `${bar.height}%` }"></span>
            </div>
            <div class="benchmark-axis" aria-hidden="true">
              <span>0D</span>
              <strong>↑ Median</strong>
              <span>180D</span>
            </div>
            <a class="benchmark-source" href="https://www.aihw.gov.au/reports/aged-care/aged-care-services-access/contents/technical-notes" target="_blank" rel="noreferrer">
              Source: AIHW ↗
            </a>
          </article>

          <article class="landing-disclaimer">
            <div class="safe-icon" aria-hidden="true">
              <svg viewBox="0 0 24 24">
                <path d="M12 3 19 6v5c0 4.6-3 8-7 10-4-2-7-5.4-7-10V6l7-3Z" />
                <path d="m9 12 2 2 4-5" />
              </svg>
            </div>
            <h2>Before you start</h2>
            <p>A quick, private estimation.</p>
            <ul class="start-checklist">
              <li>
                <span class="check-icon">✓</span>
                <span>Estimate only - not a live vacancy or guaranteed placement.</span>
              </li>
              <li>
                <span class="check-icon">✓</span>
                <span>About 2 minutes. Skip any sensitive question.</span>
              </li>
              <li>
                <span class="check-icon">✓</span>
                <span>Built on published AIHW cohort patterns.</span>
              </li>
              <li class="privacy-note">
                <span class="check-icon">✓</span>
                <span>Your answers stay on this device.</span>
              </li>
            </ul>
          </article>

          <button class="start-estimate-btn" type="button" @click="openEstimator">
            Get my estimate
            <span aria-hidden="true">→</span>
          </button>
        </section>

        <Teleport to="body">
          <div v-if="estimatorOpen" class="estimator-overlay" role="dialog" aria-modal="true" aria-labelledby="estimator-modal-title">
            <section class="estimator-modal">
              <header class="estimator-modal-header">
                <div>
                  <div class="wait-kicker">
                    <svg viewBox="0 0 24 24" aria-hidden="true">
                      <path d="M12 3l1.8 5.2L19 10l-5.2 1.8L12 17l-1.8-5.2L5 10l5.2-1.8L12 3Z" />
                      <path d="M5 14l.8 2.2L8 17l-2.2.8L5 20l-.8-2.2L2 17l2.2-.8L5 14Z" />
                    </svg>
                    Guided estimate
                  </div>
                  <h2 id="estimator-modal-title">Answer a few questions</h2>
                  <p>Complete the Background, Care, and Health sections to calculate your estimate.</p>
                </div>
                <button class="modal-close-btn" type="button" aria-label="Close estimator" @click="closeEstimator">
                  ×
                </button>
              </header>

              <div class="estimator-modal-body">
                <section class="progress-wrap" aria-label="Estimator progress">
                  <div class="progress-text">
                    Category {{ currentStep + 1 }} of {{ categories.length }}
                    <span>· {{ currentCategoryAnsweredCount }} of {{ currentCategory.questions.length }} answered</span>
                  </div>
                  <div class="progress-dots">
                    <button
                      v-for="(category, index) in categorySteps"
                      :key="category.id"
                      class="progress-dot"
                      :class="{
                        active: index === currentStep,
                        answered: isCategoryComplete(category) && index !== currentStep,
                        locked: !canNavigateToCategory(index)
                      }"
                      type="button"
                      :disabled="!canNavigateToCategory(index)"
                      :aria-label="`Go to category ${index + 1}`"
                      :title="!canNavigateToCategory(index) ? 'Complete earlier sections first' : undefined"
                      @click="goToCategory(index)"
                    >
                      <span class="progress-number">{{ index + 1 }}</span>
                      <span class="progress-label">{{ category.shortLabel }}</span>
                    </button>
                  </div>
                </section>

                <section ref="categoryCardRef" class="question-card category-card">
                  <div class="category-header">
                    <div class="question-section">{{ currentCategory.eyebrow }}</div>
                    <h2>{{ currentCategory.title }}</h2>
                    <p>{{ currentCategory.description }}</p>
                  </div>

                  <div class="category-question-list">
                    <article
                      v-for="question in currentCategory.questions"
                      :key="question.id"
                      class="category-question"
                      :class="{ invalid: shouldShowQuestionError(question.id) }"
                    >
                      <div class="question-header">
                        <div class="question-copy">
                          <div class="question-title-row">
                            <div class="question-icon" aria-hidden="true">
                              <svg viewBox="0 0 24 24">
                                <template v-if="question.icon === 'user'">
                                  <circle cx="12" cy="8" r="3" />
                                  <path d="M6 20v-1a6 6 0 0 1 12 0v1" />
                                </template>
                                <template v-else-if="question.icon === 'calendar'">
                                  <rect x="4" y="5" width="16" height="15" rx="2" />
                                  <path d="M8 3v4M16 3v4M4 10h16" />
                                </template>
                                <template v-else-if="question.icon === 'people'">
                                  <circle cx="9" cy="8" r="3" />
                                  <path d="M3 20v-1a6 6 0 0 1 12 0v1" />
                                  <path d="M16 6.5a3 3 0 0 1 0 5" />
                                  <path d="M21 20v-1a5 5 0 0 0-3-4.6" />
                                </template>
                                <template v-else-if="question.icon === 'globe'">
                                  <circle cx="12" cy="12" r="8" />
                                  <path d="M4 12h16M12 4a12 12 0 0 1 0 16M12 4a12 12 0 0 0 0 16" />
                                </template>
                                <template v-else-if="question.icon === 'map'">
                                  <path d="M9 18 3 21V6l6-3 6 3 6-3v15l-6 3-6-3Z" />
                                  <path d="M9 3v15M15 6v15" />
                                </template>
                                <template v-else-if="question.icon === 'list'">
                                  <path d="M9 6h11M9 12h11M9 18h11" />
                                  <path d="m4 6 1 1 2-2M4 12l1 1 2-2M4 18l1 1 2-2" />
                                </template>
                                <template v-else-if="question.icon === 'home'">
                                  <path d="M4 11 12 4l8 7v9a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1v-9Z" />
                                  <path d="M9 21v-7h6v7" />
                                </template>
                                <template v-else-if="question.icon === 'flag'">
                                  <path d="M6 21V4h11l-2 4 2 4H6" />
                                </template>
                                <template v-else-if="question.icon === 'hospital'">
                                  <rect x="4" y="4" width="16" height="16" rx="2" />
                                  <path d="M12 8v8M8 12h8" />
                                </template>
                                <template v-else-if="question.icon === 'health'">
                                  <path d="M12 21s-7-4.6-9-10a4.8 4.8 0 0 1 8-5 4.8 4.8 0 0 1 8 5c-2 5.4-9 10-9 10Z" />
                                </template>
                                <template v-else>
                                  <rect x="6" y="3" width="12" height="18" rx="2" />
                                  <path d="M9 8h6M9 12h6M9 16h3" />
                                </template>
                              </svg>
                            </div>
                            <div>
                              <h3>{{ question.title }}</h3>
                              <p>{{ question.prompt }}</p>
                            </div>
                          </div>
                        </div>

                        <div
                          class="tooltip-wrap"
                          @mouseenter="openTooltipFor(question.id)"
                          @mouseleave="scheduleTooltipClose"
                        >
                          <button
                            class="info-btn"
                            type="button"
                            :aria-expanded="openTooltip === question.id"
                            :aria-label="`Why we ask about ${question.title}`"
                            @click="toggleTooltip(question.id)"
                          >
                            i
                          </button>
                          <div
                            v-if="openTooltip === question.id"
                            class="tooltip-card"
                            @mouseenter="openTooltipFor(question.id)"
                            @mouseleave="scheduleTooltipClose"
                          >
                            <strong>Why we ask</strong>
                            <span>{{ question.tooltip }}</span>
                            <a
                              v-if="question.tooltipLink"
                              class="tooltip-link"
                              :href="question.tooltipLink.href"
                              target="_blank"
                              rel="noreferrer"
                            >
                              {{ question.tooltipLink.label }}
                            </a>
                          </div>
                        </div>
                      </div>

                      <div class="answer-list">
                        <button
                          v-for="option in question.options"
                          :key="option.label"
                          class="answer-option"
                          :class="{ selected: isSelected(question.id, option.value) }"
                          type="button"
                          @click="handleAnswerSelect(question, option.value)"
                        >
                          <span>{{ option.label }}</span>
                          <span class="radio" aria-hidden="true">
                            <span v-if="isSelected(question.id, option.value)"></span>
                          </span>
                        </button>
                      </div>
                    </article>
                  </div>
                </section>

                <section class="wizard-actions">
                  <button
                    class="back-btn"
                    type="button"
                    :disabled="currentStep === 0"
                    @click="previousQuestion"
                  >
                    <svg viewBox="0 0 24 24" aria-hidden="true">
                      <path d="M19 12H5M12 19l-7-7 7-7" />
                    </svg>
                    Back
                  </button>

                  <button
                    class="next-btn"
                    type="button"
                    :disabled="submitting"
                    @click="nextQuestion"
                  >
                    {{ currentStep === categories.length - 1 ? (submitting ? 'Calculating...' : 'See my estimate') : 'Next category' }}
                    <svg viewBox="0 0 24 24" aria-hidden="true">
                      <path d="M5 12h14M13 6l6 6-6 6" />
                    </svg>
                  </button>
                </section>

                <p v-if="error" class="error-message">{{ error }}</p>
              </div>
            </section>
          </div>
        </Teleport>

        <section class="did-you-know" aria-label="AIHW wait time context">
          <div class="did-you-know-header">
            <div class="question-section">DID YOU KNOW?</div>
            <h2>Helpful context before you compare options</h2>
          </div>
          <div class="insight-grid">
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
                <h3>{{ insight.title }}</h3>
                <p>{{ insight.copy }}</p>
              </div>
            </article>
          </div>
        </section>
      </template>

      <section v-else class="result-view">
        <div class="wait-kicker">
          <svg viewBox="0 0 24 24" aria-hidden="true">
            <path d="M12 3l1.8 5.2L19 10l-5.2 1.8L12 17l-1.8-5.2L5 10l5.2-1.8L12 3Z" />
            <path d="M5 14l.8 2.2L8 17l-2.2.8L5 20l-.8-2.2L2 17l2.2-.8L5 14Z" />
          </svg>
          Answer a few questions
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
            This estimate compares your answers with AIHW-reported elapsed-time patterns for aged care access.
            It is intended as a guide for planning conversations.
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
            This result is based on AIHW data and is not a guaranteed wait time. It does not represent live vacancies,
            confirmed waiting time, or guaranteed placement. Actual wait times depend on individual circumstances,
            local availability, assessment details and provider decisions.
            <a href="https://www.aihw.gov.au/reports/aged-care/aged-care-services-access/contents/technical-notes" target="_blank" rel="noreferrer">
              AIHW technical notes
            </a>
          </p>
        </div>

        <section class="did-you-know did-you-know-result" aria-label="AIHW wait time context">
          <div class="did-you-know-header">
            <div class="question-section">DID YOU KNOW?</div>
            <h2>More context behind your estimate</h2>
          </div>
          <div class="insight-grid">
            <article
              v-for="insight in estimatorInsights"
              :key="`result-${insight.title}`"
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
                <h3>{{ insight.title }}</h3>
                <p>{{ insight.copy }}</p>
              </div>
            </article>
          </div>
        </section>
      </section>
    </main>

    <FooterSection />
  </div>
</template>

<script setup>
import { computed, nextTick, ref } from 'vue'
import { useRouter } from 'vue-router'
import Header from '../components/Header.vue'
import FooterSection from '../components/FooterSection.vue'
import { estimateWaitTime } from '../services/facilitiesApi'

const OUTCOME_DISPLAY = {
  less_than_median: {
    text: 'Shorter Wait',
    label: 'Estimated shorter than the benchmark',
    tone: 'tone-shorter'
  },
  around_median: {
    text: 'Moderate Wait',
    label: 'Estimated around the benchmark',
    tone: 'tone-average'
  },
  more_than_median: {
    text: 'Longer Wait',
    label: 'Estimated longer than the benchmark',
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
      { label: 'Prefer not to say', value: null }
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
      { label: 'Prefer not to say', value: null }
    ]
  },
  {
    id: 'remoteness',
    field: 'remoteness',
    required: true,
    section: 'LOCATION',
    title: 'Location type',
    prompt: 'Which best describes where you live?',
    icon: 'map',
    tooltip: 'Location type uses the Modified Monash Model for the person’s primary address. AIHW groups this as metropolitan, regional centres, or rural and remote areas.',
    tooltipLink: {
      label: 'Find yours here',
      href: 'https://www.health.gov.au/resources/apps-and-tools/health-workforce-locator'
    },
    options: [
      { label: 'Metropolitan (MM 1)', value: 'Metropolitan (MM 1)' },
      { label: 'Regional centres (MM 2)', value: 'Regional centres (MM 2)' },
      { label: 'Rural and remote (MM 3-7)', value: 'Rural and remote (MM 3–7)' }
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
      { label: 'Prefer not to say', value: null }
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
      { label: 'Prefer not to say', value: null }
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
      { label: 'Prefer not to say', value: null }
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
      { label: 'Prefer not to say', value: null }
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
      { label: 'Prefer not to say', value: null }
    ]
  }
]

const categories = [
  {
    id: 'personal-background',
    eyebrow: 'STEP 1',
    shortLabel: 'Background',
    title: 'Personal background',
    description: 'Tell us about your background and where you live so we can compare you with the right AIHW cohort.',
    questionIds: ['sex', 'age', 'first_nations_status', 'cald_status', 'country_of_birth', 'remoteness']
  },
  {
    id: 'care-situation',
    eyebrow: 'STEP 2',
    shortLabel: 'Care',
    title: 'Care situation',
    description: 'These questions cover your care history, support network, and assessment details.',
    questionIds: ['aged_care_service_use', 'caring_arrangement', 'living_arrangement', 'priority_level', 'assessment_location']
  },
  {
    id: 'health-conditions',
    eyebrow: 'STEP 3',
    shortLabel: 'Health',
    title: 'Health conditions',
    description: 'Finally, we look at the health factors included in the AIHW wait-time model.',
    questionIds: ['dementia_status', 'mental_health_status', 'morbidity']
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

const benchmarkBars = [
  16, 22, 30, 42, 55, 66, 78, 90, 72, 58, 46, 34, 25, 18, 14
].map((height, index) => ({
  height,
  index,
  median: index === 7
}))

const router = useRouter()
const currentStep = ref(0)
const estimatorOpen = ref(false)
const answers = ref({})
const openTooltip = ref(null)
const submitting = ref(false)
const error = ref('')
const result = ref(null)
const invalidQuestionIds = ref([])
const categoryCardRef = ref(null)
let tooltipCloseTimer = null
const questionLookup = Object.fromEntries(questions.map((question) => [question.id, question]))
const categorySteps = categories.map((category) => ({
  ...category,
  questions: category.questionIds.map((questionId) => questionLookup[questionId])
}))

const currentCategory = computed(() => categorySteps[currentStep.value])
const currentCategoryAnsweredCount = computed(
  () => currentCategory.value.questions.filter((question) => isAnswered(question.id)).length
)
const resultDisplay = computed(() => OUTCOME_DISPLAY[result.value?.outcome] || OUTCOME_DISPLAY.around_median)

const estimateText = computed(() => (result.value ? resultDisplay.value.text : ''))

const outcomeLabel = computed(() => (result.value ? resultDisplay.value.label : ''))

const estimateToneClass = computed(() => (result.value ? resultDisplay.value.tone : ''))

function openEstimator() {
  estimatorOpen.value = true
  error.value = ''
}

function closeEstimator() {
  estimatorOpen.value = false
  openTooltip.value = null
  error.value = ''
}

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
  if (question.required) {
    invalidQuestionIds.value = invalidQuestionIds.value.filter((questionId) => questionId !== question.id)
  }
  error.value = ''
}

function isCategoryComplete(category) {
  return category.questions.every((question) => isAnswered(question.id))
}

function getRequiredUnansweredQuestions(category) {
  return category.questions.filter((question) => question.required && !isAnswered(question.id))
}

function isCategoryRequiredComplete(category) {
  return getRequiredUnansweredQuestions(category).length === 0
}

function canNavigateToCategory(index) {
  if (index <= currentStep.value) return true
  return categorySteps.slice(0, index).every(isCategoryRequiredComplete)
}

async function goToCategory(index) {
  if (!canNavigateToCategory(index)) {
    const firstIncompleteIndex = categorySteps.findIndex((category) => !isCategoryRequiredComplete(category))

    if (firstIncompleteIndex >= 0) {
      const unanswered = getRequiredUnansweredQuestions(categorySteps[firstIncompleteIndex])
      currentStep.value = firstIncompleteIndex
      invalidQuestionIds.value = unanswered.map((question) => question.id)
      error.value = 'Please complete earlier required questions before moving ahead.'
      await nextTick()
      categoryCardRef.value?.scrollIntoView({ behavior: 'smooth', block: 'start' })
    }

    return
  }

  currentStep.value = index
  openTooltip.value = null
  invalidQuestionIds.value = []
  error.value = ''
  await nextTick()
  categoryCardRef.value?.scrollIntoView({ behavior: 'smooth', block: 'start' })
}

function previousQuestion() {
  if (currentStep.value > 0) {
    goToCategory(currentStep.value - 1)
  }
}

function shouldShowQuestionError(questionId) {
  return invalidQuestionIds.value.includes(questionId)
}

function nextQuestion() {
  const unanswered = getRequiredUnansweredQuestions(currentCategory.value)
  if (unanswered.length > 0) {
    invalidQuestionIds.value = unanswered.map((question) => question.id)
    const names = unanswered.map((question) => `"${question.title}"`).join(', ')
    error.value = `Please answer ${names} before continuing.`
    return
  }

  invalidQuestionIds.value = []
  error.value = ''
  if (currentStep.value < categories.length - 1) {
    goToCategory(currentStep.value + 1)
  } else {
    submitEstimate()
  }
}

function clearTooltipCloseTimer() {
  if (tooltipCloseTimer) {
    clearTimeout(tooltipCloseTimer)
    tooltipCloseTimer = null
  }
}

function openTooltipFor(questionId) {
  clearTooltipCloseTimer()
  openTooltip.value = questionId
}

function toggleTooltip(questionId) {
  clearTooltipCloseTimer()
  openTooltip.value = openTooltip.value === questionId ? null : questionId
}

function scheduleTooltipClose() {
  clearTooltipCloseTimer()
  tooltipCloseTimer = setTimeout(() => {
    openTooltip.value = null
    tooltipCloseTimer = null
  }, 140)
}

function closeTooltip() {
  clearTooltipCloseTimer()
  openTooltip.value = null
}

function buildPayload() {
  return questions.reduce((payload, question) => {
    payload[question.field] = answers.value[question.id]
    return payload
  }, {})
}

async function submitEstimate() {
  if (submitting.value) return

  const firstIncompleteIndex = categorySteps.findIndex((category) => !isCategoryRequiredComplete(category))

  if (firstIncompleteIndex >= 0) {
    const unanswered = getRequiredUnansweredQuestions(categorySteps[firstIncompleteIndex])
    currentStep.value = firstIncompleteIndex
    invalidQuestionIds.value = unanswered.map((question) => question.id)
    const names = unanswered.map((question) => `"${question.title}"`).join(', ')
    error.value = `Please answer ${names} before seeing your estimate.`
    await nextTick()
    categoryCardRef.value?.scrollIntoView({ behavior: 'smooth', block: 'start' })
    return
  }

  submitting.value = true
  error.value = ''

  try {
    result.value = await estimateWaitTime(buildPayload())
    estimatorOpen.value = false
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
  answers.value = {}
  currentStep.value = 0
  result.value = null
  estimatorOpen.value = false
  error.value = ''
  invalidQuestionIds.value = []
  openTooltip.value = null
}

function goFindCare() {
  router.push('/find-bed')
}
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

.wait-landing {
  margin: 62px auto 0;
  max-width: 1060px;
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 32px;
  align-items: stretch;
}

.benchmark-card,
.landing-disclaimer {
  min-height: 520px;
  border: 1px solid #ddd8cf;
  border-radius: 32px;
  background: #fff;
  box-shadow: 0 22px 42px rgba(31, 45, 42, 0.1);
  padding: 52px;
  text-align: left;
  box-sizing: border-box;
}

.benchmark-card {
  position: relative;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  color: #fff;
  background:
    linear-gradient(rgba(255, 255, 255, 0.045) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255, 255, 255, 0.045) 1px, transparent 1px),
    #21685b;
  background-size: 32px 32px;
  border-color: #21685b;
}

.landing-disclaimer {
  position: relative;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.landing-disclaimer::after {
  content: "";
  position: absolute;
  top: -62px;
  right: -80px;
  width: 270px;
  height: 270px;
  border-radius: 50%;
  border: 2px solid rgba(45, 106, 95, 0.1);
  box-shadow:
    0 0 0 38px rgba(45, 106, 95, 0.055),
    0 0 0 76px rgba(45, 106, 95, 0.04);
  pointer-events: none;
}

.benchmark-label {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  color: rgba(255, 255, 255, 0.74);
  font-size: 14px;
  font-weight: 800;
  letter-spacing: 0.16em;
  text-transform: uppercase;
}

.benchmark-label svg {
  width: 18px;
  height: 18px;
  fill: none;
  stroke: currentColor;
  stroke-width: 1.9;
  stroke-linecap: round;
  stroke-linejoin: round;
}

.benchmark-value {
  display: flex;
  align-items: baseline;
  gap: 18px;
  margin-top: 34px;
}

.benchmark-card strong {
  font-family: var(--font-display);
  color: #fff;
  font-size: 106px;
  font-weight: 800;
  line-height: 1;
}

.benchmark-value span {
  color: rgba(255, 255, 255, 0.9);
  font-size: 42px;
}

.benchmark-card p,
.landing-disclaimer p {
  margin: 18px 0 0;
  color: #5f746f;
  font-size: 18px;
  line-height: 1.55;
}

.benchmark-card p {
  max-width: 390px;
  color: rgba(255, 255, 255, 0.82);
}

.benchmark-chart {
  height: 118px;
  margin-top: auto;
  display: flex;
  align-items: end;
  gap: 10px;
}

.benchmark-chart span {
  width: 18px;
  min-height: 12px;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.24);
}

.benchmark-chart span.median {
  background: #34bd82;
}

.benchmark-axis {
  display: flex;
  justify-content: space-between;
  color: rgba(255, 255, 255, 0.45);
  font-size: 13px;
}

.benchmark-axis strong {
  color: #62d59d;
  font-family: var(--font-sans);
  font-size: 13px;
  text-transform: uppercase;
}

.benchmark-source {
  margin: 28px -52px -52px;
  padding: 18px 52px;
  background: rgba(255, 255, 255, 0.06);
  color: rgba(255, 255, 255, 0.78);
  text-decoration: none;
  font-weight: 700;
}

.landing-disclaimer h2 {
  margin: 28px 0 0;
  color: #1f2d2a;
  font-family: var(--font-display);
  font-size: 36px;
  line-height: 1.08;
}

.safe-icon {
  width: 74px;
  height: 74px;
  border-radius: 20px;
  background: #dcefe8;
  color: #2ca878;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.safe-icon svg {
  width: 34px;
  height: 34px;
  fill: none;
  stroke: currentColor;
  stroke-width: 1.9;
  stroke-linecap: round;
  stroke-linejoin: round;
}

.start-checklist {
  position: relative;
  z-index: 1;
  display: flex;
  flex-direction: column;
  gap: 22px;
  margin: 34px 0 0;
  padding: 0;
  list-style: none;
}

.start-checklist li {
  display: grid;
  grid-template-columns: 34px minmax(0, 1fr);
  gap: 14px;
  align-items: start;
  color: #52625f;
  font-size: 18px;
  line-height: 1.45;
}

.check-icon,
.lock-icon {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background: #e1f2ed;
  color: #34a87a;
  font-weight: 900;
}

.lock-icon {
  background: transparent;
  color: #72807d;
  font-size: 24px;
}

.start-estimate-btn {
  grid-column: 1 / -1;
  justify-self: center;
  min-height: 54px;
  border: none;
  border-radius: 999px;
  background: #2d6a5f;
  color: #fff;
  display: inline-flex;
  align-items: center;
  gap: 28px;
  padding: 0 42px;
  font-size: 20px;
  font-weight: 800;
  cursor: pointer;
  box-shadow: 0 12px 28px rgba(45, 106, 95, 0.22);
}

.start-estimate-btn:hover {
  background: #23564d;
}

.estimator-overlay {
  position: fixed;
  inset: 0;
  z-index: 5000;
  background: rgba(31, 45, 42, 0.48);
  display: flex;
  align-items: stretch;
  justify-content: center;
  padding: 18px;
}

.estimator-modal {
  width: min(1120px, 100%);
  max-height: 100%;
  display: flex;
  flex-direction: column;
  background: #f7f4ee;
  border: 1px solid #ddd8cf;
  border-radius: 18px;
  box-shadow: 0 26px 80px rgba(31, 45, 42, 0.36);
  overflow: hidden;
}

.estimator-modal-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 20px;
  padding: 24px 28px;
  background: #fff;
  border-bottom: 1px solid #e7e1d7;
}

.estimator-modal-header h2 {
  margin: 14px 0 8px;
  font-family: var(--font-display);
  color: #1f2d2a;
  font-size: 34px;
}

.estimator-modal-header p {
  margin: 0;
  color: #687777;
  line-height: 1.5;
}

.modal-close-btn {
  width: 42px;
  height: 42px;
  border: none;
  border-radius: 50%;
  background: #f2efe8;
  color: #4d5b57;
  font-size: 28px;
  line-height: 1;
  cursor: pointer;
}

.estimator-modal-body {
  overflow: auto;
  padding: 0 28px 34px;
}

.insight-grid {
  margin: 22px auto 0;
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

.insight-card h3 {
  margin: 0;
  font-family: var(--font-display);
  font-size: 24px;
  line-height: 1.1;
  color: #22332e;
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
.insight-blue h2,
.insight-blue h3 {
  color: #2f7f91;
}

.insight-primary .insight-icon,
.insight-primary h3 {
  color: #2d6a5f;
}

.insight-green .insight-icon,
.insight-green h3 {
  color: #4e8133;
}

.did-you-know {
  margin-top: 56px;
  text-align: left;
}

.did-you-know-header {
  max-width: 720px;
}

.did-you-know-header h2 {
  margin: 0;
  font-family: var(--font-display);
  font-size: 32px;
  line-height: 1.12;
  color: #1f2d2a;
}

.did-you-know-result {
  margin-top: 36px;
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
  gap: 12px;
  flex-wrap: wrap;
}

.progress-dot {
  min-width: 124px;
  height: 42px;
  border-radius: 999px;
  border: none;
  background: #e2dfd8;
  color: #617270;
  padding: 0 16px;
  cursor: pointer;
  transition: background 0.15s, transform 0.15s, color 0.15s;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  font-weight: 700;
}

.progress-dot:hover:not(:disabled) {
  background: #98b5ad;
  transform: translateY(-1px);
  color: #1f2d2a;
}

.progress-dot.active {
  background: #2d6a5f;
  color: #ffffff;
}

.progress-dot.answered {
  background: #e2dfd8;
  color: #617270;
}

.progress-dot.answered .progress-number {
  background: rgba(45, 106, 95, 0.12);
  color: #2d6a5f;
}

.progress-dot:disabled,
.progress-dot.locked {
  cursor: not-allowed;
  opacity: 0.58;
}

.progress-dot:disabled {
  transform: none;
}

.progress-number {
  width: 24px;
  height: 24px;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.28);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-size: 13px;
  line-height: 1;
}

.progress-dot:not(.active):not(.answered) .progress-number {
  background: rgba(45, 106, 95, 0.12);
  color: #2d6a5f;
}

.progress-label {
  font-size: 14px;
  letter-spacing: 0.01em;
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

.category-card {
  text-align: left;
}

.category-header {
  max-width: 700px;
  margin-bottom: 28px;
}

.category-header h2 {
  margin: 0;
  font-family: var(--font-display);
  color: #1f2d2a;
  font-size: 34px;
  line-height: 1.12;
}

.category-header p {
  margin: 12px 0 0;
  color: #5f746f;
  font-size: 17px;
  line-height: 1.55;
}

.category-question-list {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.category-question {
  border-top: 1px solid #ebe5db;
  padding-top: 24px;
  border-radius: 18px;
  transition: box-shadow 0.15s, background 0.15s, border-color 0.15s;
}

.category-question:first-child {
  border-top: none;
  padding-top: 0;
}

.category-question.invalid {
  border-top-color: transparent;
  background: #fff6f6;
  box-shadow: 0 0 0 2px #d35c5c;
  padding: 20px;
}

.category-question.invalid:first-child {
  padding-top: 20px;
}

.category-question.invalid .question-icon {
  background: #fbe3e3;
  color: #b94040;
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

.question-title-row h2,
.question-title-row h3 {
  margin: 0;
  font-family: var(--font-display);
  color: #1f2d2a;
  font-size: 30px;
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

.tooltip-link {
  display: inline-block;
  margin-top: 10px;
  color: #2d6a5f;
  font-weight: 700;
  text-decoration: underline;
  text-underline-offset: 3px;
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

  .wait-landing {
    grid-template-columns: 1fr;
    margin-top: 30px;
  }

  .benchmark-card,
  .landing-disclaimer {
    min-height: auto;
    border-radius: 22px;
    padding: 24px;
  }

  .benchmark-card strong {
    font-size: 70px;
  }

  .benchmark-value span {
    font-size: 28px;
  }

  .benchmark-chart {
    height: 88px;
    gap: 6px;
  }

  .benchmark-chart span {
    width: 12px;
  }

  .benchmark-source {
    margin: 22px -24px -24px;
    padding: 16px 24px;
  }

  .landing-disclaimer h2 {
    font-size: 30px;
  }

  .start-checklist li {
    font-size: 16px;
  }

  .estimator-overlay {
    padding: 0;
  }

  .estimator-modal {
    border-radius: 0;
  }

  .estimator-modal-header {
    padding: 18px 16px;
  }

  .estimator-modal-header h2 {
    font-size: 27px;
  }

  .estimator-modal-body {
    padding: 0 16px 28px;
  }

  .progress-wrap {
    margin-top: 38px;
  }

  .progress-dots {
    gap: 10px;
  }

  .progress-dot {
    min-width: 96px;
    height: 38px;
    padding: 0 12px;
    gap: 8px;
  }

  .progress-label {
    font-size: 13px;
  }

  .insight-grid {
    grid-template-columns: 1fr;
    margin-top: 30px;
  }

  .did-you-know {
    margin-top: 42px;
  }

  .did-you-know-header h2 {
    font-size: 26px;
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

  .category-header h2 {
    font-size: 28px;
  }

  .category-header p {
    font-size: 15px;
  }

  .question-header {
    gap: 12px;
  }

  .question-icon {
    border-radius: 14px;
  }

  .question-title-row h2,
  .question-title-row h3 {
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
  .next-btn {
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
