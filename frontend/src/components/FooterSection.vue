<template>
  <footer class="footer">
    <div class="footer-container">
      <div class="footer-top">
        <div class="footer-brand">
          <h3>CareLink</h3>
          <span class="footer-location">VICTORIA</span>
          <p>
            Helping Australians find aged care beds faster.<br />
            Built with open government data.
          </p>
        </div>

        <div class="footer-links">
          <h4>Quick Links</h4>
          <router-link to="/find-bed">Find a Bed</router-link>
          <a href="#how-it-works">How It Works</a>
          <a href="#">My Aged Care</a>
        </div>
      </div>

      <div class="footer-divider"></div>

      <div class="footer-bottom">
        <p class="footer-source">
          Powered by open data from AIHW · GEN Aged Care Data
        </p>
        <p class="footer-copy">
          © 2025 CareLinkTE04. All rights reserved.
        </p>
      </div>
    </div>
  </footer>
</template>

<style scoped>
.footer {
  background: linear-gradient(90deg, #17352f 0%, #132e29 100%);
  color: #d7dfda;
  padding: 42px 0 56px;
  margin-top: 60px;
}

.footer-container {
  width: 100%;
  max-width: 1760px;
  margin: 0 auto;
  padding: 0 72px;
  box-sizing: border-box;
}

.footer-top {
  display: grid;
  grid-template-columns: 1fr 1fr;
  align-items: start;
}

.footer-brand {
  justify-self: center;
  text-align: left;
  width: 360px;
  padding-left: 300px;
}

.footer-brand h3 {
  margin: 0;
  font-size: 20px;
  line-height: 1.1;
  font-weight: 700;
  color: #f3f4ef;
  padding-left: 60px;
}

.footer-location {
  display: block;
  margin-top: 6px;
  margin-bottom: 18px;
  font-size: 10px;
  line-height: 1.2;
  letter-spacing: 0.04em;
  color: #a9b3ae;
  font-family: 'Inter', sans-serif;
  text-align: left;
  padding-left: 60px;
}

.footer-brand p {
  margin: 0;
  font-size: 10px;
  line-height: 1.45;
  color: #9aa7a2;
  font-family: 'Inter', sans-serif;
  text-align: left;
  max-width: 360px;
}

.footer-links {
  justify-self: center;
  text-align: left;
  width: 220px;
}

.footer-links h4 {
  margin: 0 0 12px;
  font-size: 14px;
  line-height: 1.2;
  font-weight: 700;
  color: #f3f4ef;
  font-family: 'Inter', sans-serif;
}

.footer-links a {
  display: block;
  margin-bottom: 10px;
  font-size: 12px;
  line-height: 0.8;
  color: #a9b3ae;
  text-decoration: none;
  font-family: 'Inter', sans-serif;
  transition: color 0.2s ease;
}

.footer-links a:hover {
  color: #ffffff;
}

.footer-divider {
  margin: 48px 0 22px;
  height: 1px;
  background: rgba(255, 255, 255, 0.08);
}

.footer-bottom {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 20px;
}

.footer-source,
.footer-copy {
  margin: 0;
  font-size: 10px;
  line-height: 1.3;
  color: #72817c;
  font-family: 'Inter', sans-serif;
}

@media (max-width: 1024px) {
  .footer {
    padding: 36px 0 44px;
  }

  .footer-container {
    padding: 0 24px;
  }

  .footer-top {
    grid-template-columns: 1fr;
    gap: 32px;
  }

  .footer-brand,
  .footer-links {
    justify-self: start;
    width: auto;
  }

  .footer-divider {
    margin: 32px 0 18px;
  }

  .footer-bottom {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>