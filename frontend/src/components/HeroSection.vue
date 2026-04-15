<template>
    <section class="hero-section">
      <div class="hero-content">
        <div class="hero-left">
        <h1>
            Helping you choose the right care,
            <span>with confidence.</span>
        </h1>
        <p class="hero-description">
            Search residential aged care and home care services across Victoria.
            See available beds, expected wait times, and funding options in one place.
        </p>

        <div class="hero-actions">
          <button class="primary-btn" @click="goToFindBed">
            Find available care
          </button>
          <p class="care-tags-label">Or browse by Care Type</p>
        </div>
        <div class="care-tags">
          <button
            v-for="option in careOptions"
            :key="option.value"
            class="care-tag-btn"
            @click="goToFindBedWithType(option.value)"
          >
            {{ option.label }}
          </button>
        </div>
        </div>

        <div class="hero-right">
        <div class="hero-image-card">
            <img
              class="hero-image"
              :src="heroImage"
              alt="Caregiver walking with an older adult in an aged care facility"
            />
            <p class="hero-image-credit">
              Photo by Jsme MILA on Pexels
            </p>
        </div>
        </div>
      </div>
    </section>
</template>

<script setup>
import { useRouter } from 'vue-router'
import heroImage from '../assets/hero-aged-care.jpg'

const router = useRouter()

const careOptions = [
  { value: 'Residential', label: 'Residential homes' },
  { value: 'Home Care', label: 'Home care services' },
  { value: 'Transition Care', label: 'Transition care' },
  { value: 'Short-Term Restorative Care (STRC)', label: 'Restorative care (STRC)' },
  { value: 'Multi-Purpose Service', label: 'Multi-purpose services' },
  {
    value: 'National Aboriginal and Torres Strait Islander Aged Care Program',
    label: 'Indigenous aged care'
  }
]

function goToFindBed() {
  router.push('/find-bed')
}

function goToFindBedWithType(careType) {
  router.push({
    path: '/find-bed',
    query: { careType }
  })
}
</script>

<style>
.hero-section {
  width: 100%;
  background: #dfe8e3;
}

.hero-content {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 110px;
  max-width: 1200px;
  margin: 0 auto;
  padding: 75px 40px;
  align-items: center;
  min-height: 75vh;
}

.hero-left {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  justify-content: center;
  gap: 28px;
  text-align: left;
}

.hero-left h1 {
  font-size: 42px;
  font-weight: 900;
  line-height: 1.2;
  color: #1a1a1a;
  margin: 0;
  font-family: 'Nunito', sans-serif;
}

.hero-left h1 span {
  color: #5d8b72;
}

.hero-description {
  margin: 0;
  font-size: 16px;
  line-height: 1.7;
  color: #4e5f59;
}

.hero-actions {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 35px;
  margin: 0;
}

.primary-btn {
  background: #5d8b72;
  color: white;
  border: none;
  padding: 14px 28px;
  border-radius: 12px;
  font-size: 17px;
  font-weight: 700;
  cursor: pointer;
  font-family: 'Nunito', sans-serif;
  box-shadow: 0 8px 20px rgba(93, 139, 114, 0.22);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.primary-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 12px 24px rgba(93, 139, 114, 0.28);
}

.care-tags-label {
  margin: 0;
  font-size: 14px;
  font-weight: 600;
  color: #4e6258;
}

.care-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px 18px;
}

.care-tag-btn {
  padding: 0;
  border-radius: 0;
  background-color: transparent;
  color: #305447;
  border: none;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  font-family: 'Nunito', sans-serif;
  text-decoration: underline;
  text-underline-offset: 4px;
  text-decoration-thickness: 1.5px;
  transition: color 0.2s ease;
}

.care-tag-btn:hover {
  color: #1f3e34;
}

.hero-right {
  display: flex;
  justify-content: center;
}

.hero-image-card {
  position: relative;
  overflow: hidden;
  width: 100%;
  max-width: 560px;
  height: 380px;
  background: white;
  border-radius: 16px;
  box-shadow: 0 16px 36px rgba(0, 0, 0, 0.12);
}

.hero-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center;
  display: block;
}

.hero-image-credit {
  position: absolute;
  left: 14px;
  bottom: 12px;
  margin: 0;
  padding: 5px 10px;
  border-radius: 999px;
  background: rgba(19, 46, 41, 0.72);
  color: #f4f5f1;
  font-size: 11px;
  line-height: 1;
  backdrop-filter: blur(8px);
}

/* Mobile responsive */
@media (max-width: 768px) {
  .hero-content {
    grid-template-columns: 1fr;
    padding: 80px 24px 48px;
    min-height: auto;
    gap: 32px;
  }

  .hero-left h1 {
    font-size: 30px;
  }

  .hero-description {
    font-size: 15px;
  }

  .primary-btn {
    font-size: 15px;
    padding: 12px 22px;
  }

  .hero-image-card {
    height: 260px;
    max-width: 100%;
  }
}
</style>