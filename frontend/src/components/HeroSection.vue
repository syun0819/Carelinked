<template>
    <section class="hero-section">
        <div class="hero-left">
        <p class="hero-badge">AGED CARE BED FINDER - VICTORIA</p>
        <h1>
            Find the right
            care place, <span>near you, right now</span>          
        </h1>
        <p class="hero-description">
            Search available beds across residential aged care and home care services in 
            Victoria, with real wait times and funding options explained clearly.
        </p>

        <button class="primary-btn">Search Care Places</button>

        <div class="care-tags">
            <span>Residential Care</span>
            <span>Home Care Package</span>
            <span>Memory Care</span>
            <span>Respite Care</span>
            <span>High-Level Care</span>
        </div>
        </div>

        <div class="hero-right">
        <div class="hero-image-card">
            Main Visual / Carousel
        </div>
        </div>
    </section>
</template>

<style>
.hero-section {
  display: grid;
  grid-template-columns: 1.1fr 1fr;
  gap: 40px;
  padding: 60px 80px;
  background: #dfe8e3;
  align-items: center;
}

.hero-left{
  text-align: left;
  padding-left: 72px;
}

.hero-left h1 {
  font-size: 50px;
  font-weight: 900;
  line-height: 1.5;
  color: #1a1a1a;
  margin: 16px 0;
  max-width: 420px;
  margin-bottom: 40px;
}

.hero-left h1 span {
  color: #5d8b72;
}

.hero-description {
  max-width: 500px;
  font-size: 14px;
  line-height: 1.7;
  color: #5f6d67;
  max-width: 450px;
  margin-bottom: 20px;
}

.hero-badge {
  display: inline-block;
  padding: 2px 12px;
  background: white;
  border-radius: 8px;
  font-size: 10px;
  color: #5f6d67;
  margin-top: 20px;
  margin-bottom: 15px;
}

.primary-btn {
  background: #5d8b72;
  color: white;
  border: none;
  padding: 8px 24px;
  border-radius: 8px;
  font-size: 14px;
  cursor: pointer;
  margin-bottom: 30px;
}

.care-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 25px;
  max-width: 550px;
}

.care-tags span {
  padding: 0px 20px;
  border: 1px solid #d4d4d4;
  background: white;
  border-radius: 8px;
  font-size: 10px;
}

.hero-right {
  display: flex;
  justify-content: center;
}

.hero-image-card {
  width: 100%;
  max-width: 520px;
  height: 320px;
  background: white;
  border-radius: 16px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.12);
  display: flex;
  align-items: center;
  justify-content: center;
}

</style>