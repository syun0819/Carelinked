import { createApp } from 'vue'
import { createPinia } from 'pinia'
import './style.css'
import App from './App.vue'
import router from './router'
import 'leaflet/dist/leaflet.css'
import * as Sentry from "@sentry/vue"

const app = createApp(App)
const pinia = createPinia()

Sentry.init({
  app,
  dsn: "https://ad3e8fbbed93ed94b51f7f649ea5ad67@o4511408645734400.ingest.us.sentry.io/4511408777003008",
  integrations: [
    Sentry.browserTracingIntegration({ router }),
    Sentry.replayIntegration()
  ],
  tracesSampleRate: 0.5,
  replaysSessionSampleRate: 0.1,
  replaysOnErrorSampleRate: 1.0,
  tracePropagationTargets: ["localhost", /^https:\/\/carelinked-api\.carelinked-yujie\.workers\.dev/],
  environment: "production"
})


app.use(pinia)
app.use(router)
app.mount('#app')
