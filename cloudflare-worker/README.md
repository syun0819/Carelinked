# CareLinked Cloudflare Worker API

This Worker is a free-tier replacement for the retired DigitalOcean FastAPI demo backend.
It keeps the frontend-facing API paths compatible with the existing Vue app:

- `GET /api/v1/facilities/recommended`
- `GET /api/v1/facilities/search`
- `GET /api/v1/facilities/map`
- `GET /api/v1/facilities/:id`
- `GET /api/v1/facilities/:id/similar`
- `GET /api/v1/search/autocomplete`
- `POST /api/v1/waittime/estimate`
- basic heatmap endpoints used by the map overlays

## Local Development

```bash
cd cloudflare-worker
npm install
npm run dev
```

Point the frontend at the local Worker:

```bash
cd ../frontend
echo VITE_API_BASE_URL=http://localhost:8787 > .env.local
npm run dev
```

## Deploy

```bash
cd cloudflare-worker
npm install
npx wrangler login
npm run deploy
```

After deploy, set the frontend production environment variable to your Worker URL:

```text
VITE_API_BASE_URL=https://carelinked-api.<your-cloudflare-subdomain>.workers.dev
```

Alternatively, if you route `carelinked.page/api/*` to this Worker in Cloudflare, leave `VITE_API_BASE_URL` empty and the frontend will call same-origin `/api/...`.
