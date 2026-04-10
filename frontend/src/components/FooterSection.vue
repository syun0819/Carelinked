<template>
  <footer class="footer">
    <div class="footer-inner">
      <div class="footer-brand">
        <h3>CareLink</h3>
        <p>
          Helping Australians find aged care beds faster,<br />
          built with open government data.
        </p>
      </div>

      <div class="footer-links">
        <h4>Quick Links</h4>
        <a href="#">Find a Bed</a>
        <a href="#">How It Works</a>
        <a href="#">My Aged Care</a>
      </div>
    </div>
  </footer>
</template>

<style scoped>
.footer {
  background: #16352f;
  color: white;
  padding: 40px 80px;
  margin-top: 30px;
}

.footer-inner {
  max-width: 1100px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  gap: 40px;
}

.footer-brand h3,
.footer-links h4 {
  margin-bottom: 12px;
}

.footer-brand p,
.footer-links a {
  font-family: 'Inter', sans-serif;
  font-size: 14px;
  color: #d7dfda;
  text-decoration: none;
  display: block;
  margin-bottom: 8px;
}

@media (max-width: 1024px) {
  .footer {
    padding-left: 24px;
    padding-right: 24px;
  }

  .footer-inner {
    display: grid;
    grid-template-columns: 1fr;
  }
}
</style>