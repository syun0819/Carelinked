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
          <p class="care-tags-label">Or browse by care type</p>
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
  grid-template-columns: minmax(0, 0.95fr) minmax(0, 1.05fr);
  gap: 16px;
  max-width: 1540px;
  margin: 0 auto;
  padding: 56px 12px;
  align-items: center;
  min-height: 78vh;
}

.hero-left{
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  justify-content: center;
  gap: 24px;
  text-align: left;
  max-width: 620px;
}

.hero-left h1 {
  font-size: 58px;
  font-weight: 900;
  line-height: 1.2;
  color: #1a1a1a;
  margin: 0;
  max-width: 620px;
}

.hero-left h1 span {
  color: #5d8b72;
}

.hero-description {
  margin: 0;
  font-size: 19px;
  line-height: 1.7;
  color: #4e5f59;
  max-width: 580px;
}

.hero-actions {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 24px;
  margin: 0;
}

.primary-btn {
  background: #5d8b72;
  color: white;
  border: none;
  padding: 20px 40px;
  border-radius: 12px;
  font-size: 22px;
  font-weight: 700;
  cursor: pointer;
  box-shadow: 0 10px 24px rgba(93, 139, 114, 0.22);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.primary-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 14px 28px rgba(93, 139, 114, 0.28);
}

.care-tags-label {
  margin: 0;
  font-size: 15px;
  font-weight: 600;
  color: #4e6258;
  margin-bottom: -12px;
}

.care-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 10px 22px;
  max-width: 620px;
}

.care-tag-btn {
  padding: 0;
  border-radius: 0;
  background-color: transparent;
  color: #305447;
  border: none;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  line-height: 1.4;
  text-decoration: underline;
  text-underline-offset: 4px;
  text-decoration-thickness: 1.5px;
  transition: color 0.2s ease, text-decoration-color 0.2s ease;
}

.care-tag-btn:hover {
  color: #1f3e34;
  text-decoration-color: #1f3e34;
}

.hero-right {
  display: flex;
  justify-content: center;
}

.hero-image-card {
  position: relative;
  overflow: hidden;
  width: 100%;
  max-width: 680px;
  height: 440px;
  background: white;
  border-radius: 16px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.12);
  display: flex;
  align-items: center;
  justify-content: center;
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
  padding: 6px 10px;
  border-radius: 999px;
  background: rgba(19, 46, 41, 0.72);
  color: #f4f5f1;
  font-size: 11px;
  line-height: 1;
  backdrop-filter: blur(8px);
}

</style>
