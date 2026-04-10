<template>
  <section id="how-it-works" class="how-it-works-section">
    <div class="section-divider"></div>

    <div class="section-header">
      <h2>How It Works</h2>
      <p>Three simple steps to find the right aged care placement.</p>
    </div>

    <div class="how-cards">
      <div class="how-card">
        <div class="how-icon">🔍</div>
        <div class="how-step">STEP 1</div>
        <h3>Search</h3>
        <p>
          Enter a suburb or postcode and<br />
          choose the type of care. No<br />
          account needed.
        </p>
      </div>

      <div class="how-card">
        <div class="how-icon">📊</div>
        <div class="how-step">STEP 2</div>
        <h3>Compare</h3>
        <p>
          View available beds, estimated<br />
          wait times, and facility features<br />
          side by side.
        </p>
      </div>

      <div class="how-card">
        <div class="how-icon">📞</div>
        <div class="how-step">STEP 3</div>
        <h3>Connect</h3>
        <p>
          Call the facility directly or<br />
          request more information<br />
          with one click.
        </p>
      </div>
    </div>
  </section>
</template>

<style scoped>
.how-it-works-section {
  padding: 28px 44px 40px;
  background: #f7f4ee;
}

.section-divider {
  width: 100%;
  height: 1px;
  background: #d9d6cf;
  margin-bottom: 56px;
}

.section-header {
  text-align: center;
  margin-bottom: 28px;
}

.section-header h2 {
  margin: 0 0 10px;
  font-size: 32px;
  line-height: 1.1;
  font-weight: 700;
  color: #22332e;
}

.section-header p {
  margin: 0;
  font-size: 14px;
  line-height: 1.4;
  color: #8aa19a;
  font-family: 'Inter', sans-serif;
}

.how-cards {
  display: grid;
  grid-template-columns: repeat(3, 320px);
  justify-content: center;
  gap: 50px;
}

.how-card {
  background: #fbfbfa;
  border: 1.5px solid #d9d6cf;
  border-radius: 18px;
  min-height: 180px;
  padding: 10px 10px 10px;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  box-sizing: border-box;
}

.how-icon {
  font-size: 30px;
  line-height: 1;
  margin-bottom: 16px;
}

.how-step {
  margin-bottom: 8px;
  font-size: 12px;
  line-height: 1.2;
  font-weight: 700;
  letter-spacing: 0.02em;
  color: #6f8880;
  font-family: 'Inter', sans-serif;
}

.how-card h3 {
  margin: 0 0 10px;
  font-size: 20px;
  line-height: 1.15;
  font-weight: 700;
  color: #22332e;
}

.how-card p {
  margin: 0;
  font-size: 10px;
  line-height: 1.45;
  color: #8aa19a;
  font-family: 'Inter', sans-serif;
}

@media (max-width: 1024px) {
  .how-it-works-section {
    padding: 24px 24px 36px;
  }

  .section-divider {
    margin-bottom: 40px;
  }

  .section-header h2 {
    font-size: 36px;
  }

  .how-cards {
    grid-template-columns: 1fr;
    gap: 20px;
  }

  .how-card {
    min-height: auto;
    padding: 24px 20px;
  }

  .how-card h3 {
    font-size: 26px;
  }

  .how-card p {
    font-size: 16px;
  }
}
</style>