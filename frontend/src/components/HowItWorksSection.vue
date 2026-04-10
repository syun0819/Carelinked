<template>
  <section class="how-it-works-section">
    <h2>How It Works</h2>
    <p class="how-subtitle">
      Three simple steps to find the right aged care placement.
    </p>

    <div class="how-cards">
      <div class="how-card">
        <div class="how-step">STEP 1</div>
        <h3>Search</h3>
        <p>
          Enter a suburb or postcode and choose the type of care account needed.
        </p>
      </div>

      <div class="how-card">
        <div class="how-step">STEP 2</div>
        <h3>Compare</h3>
        <p>
          View estimated beds, wait times, and facility features side by side.
        </p>
      </div>

      <div class="how-card">
        <div class="how-step">STEP 3</div>
        <h3>Connect</h3>
        <p>
          Contact facilities directly or save your top choices for later.
        </p>
      </div>
    </div>
  </section>
</template>

<style scoped>
.how-it-works-section {
  padding: 72px 80px;
  text-align: center;
}

.how-it-works-section h2 {
  margin-bottom: 8px;
  font-size: 36px;
  color: #22332e;
}

.how-subtitle {
  margin-bottom: 32px;
  font-size: 14px;
  color: #8b948f;
  font-family: 'Inter', sans-serif;
}

.how-cards {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
  max-width: 980px;
  margin: 0 auto;
}

.how-card {
  background: white;
  border: 1px solid #e4ddd2;
  border-radius: 12px;
  padding: 28px 20px;
  min-height: 160px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.how-step {
  font-size: 11px;
  letter-spacing: 0.08em;
  color: #8e9a93;
  margin-bottom: 10px;
  font-family: 'Inter', sans-serif;
  font-weight: 700;
}

.how-card h3 {
  margin: 0 0 10px;
  font-size: 22px;
  color: #22332e;
}

.how-card p {
  margin: 0;
  font-size: 14px;
  line-height: 1.6;
  color: #6f7d76;
  font-family: 'Inter', sans-serif;
}

@media (max-width: 1024px) {
  .how-it-works-section {
    padding-left: 24px;
    padding-right: 24px;
  }

  .how-cards {
    grid-template-columns: 1fr;
  }
}
</style>