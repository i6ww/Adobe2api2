# adobe2api

---

### ✨ Ad Spot (o゜▽゜)o☆

This is my independently built and actively maintained personal website: [**Pixelle Labs**](https://www.pixellelabs.com/)

I share **AI creative tools**, image/video mini-products, and fun experiments here. You are welcome to explore, try everything out, and play around (๑•̀ㅂ•́)و✧. Feedback, ideas, and collaboration discussions are always appreciated! ヾ(≧▽≦*)o

---

Adobe Firefly/OpenAI-compatible gateway service.

Chinese README: `README.md`

## Overview

- External unified entry: `/v1/chat/completions` (image + video)
- Optional image-only endpoint: `/v1/images/generations`
- Token pool management (manual token + auto-refresh token)
- Admin web UI: token/config/logs/refresh profile import

## 1) Deployment

### A. Local Run

1. **Install dependencies**:

```bash
pip install -r requirements.txt
```

2. **Start service** (run in `adobe2api/`):

```bash
uvicorn app:app --host 0.0.0.0 --port 6001 --reload
```

3. **Access Admin UI**:

- URL: `http://127.0.0.1:6001/`
- Default login: `admin / admin`
- You can change credentials in "System Config" or edit `config/config.json`

### B. Docker Deployment (Recommended)

This project provides Docker support. It is recommended to use Docker Compose for one-click deployment:

```bash
docker compose up -d --build
```

## 2) Auth to this service

Service API key is configured in `config/config.json` (`api_key`).

- If set, call with either:
  - `Authorization: Bearer <api_key>`
  - `X-API-Key: <api_key>`

Admin UI and admin APIs require login session cookie via `/api/v1/auth/login`.

## 3) Supported Models

### 3.0 List all models

```bash
curl -X GET "http://127.0.0.1:6001/v1/models" \
  -H "Authorization: Bearer <service_api_key>"
```

### 3.1 Image Models

| Model ID | Description |
|----------|-------------|
| `flux` | Flux standard model |
| `fluxPro` | Flux Pro model |
| `fluxUltra` | Flux Ultra model |
| `dall-e-3` | DALL-E 3 model |
| `stable-diffusion-3` | Stable Diffusion 3 model |
| `image-3` | Adobe Image 3 model |
| `firefly` | Adobe Firefly standard model |
| `firefly-3` | Adobe Firefly 3 model |
| `firefly-real` | Adobe Firefly photorealistic model |
| `firefly-style` | Adobe Firefly style model |
| `firefly-structure` | Adobe Firefly structure model |

**Nano Banana Series** (legacy-compatible naming):

- Pattern: `firefly-nano-banana-{resolution}-{ratio}`
- Resolution: `1k` / `2k` / `4k`
- Ratio suffix: `1x1` / `16x9` / `9x16` / `4x3` / `3x4`
- Examples:
  - `firefly-nano-banana-2k-16x9`
  - `firefly-nano-banana-4k-1x1`

**Nano Banana 2 Series**:

- Pattern: `firefly-nano-banana2-{resolution}-{ratio}`
- Resolution: `1k` / `2k` / `4k`
- Ratio suffix: `1x1` / `16x9` / `9x16` / `4x3` / `3x4` / `21x9` / `3x2` / `5x4` / `4x5` / `2x3` / `8x1` / `1x4` / `1x8`
- Examples:
  - `firefly-nano-banana2-2k-16x9`
  - `firefly-nano-banana2-4k-1x1`

**Nano Banana Pro Series** (recommended):

- Pattern: `firefly-nano-banana-pro-{resolution}-{ratio}`
- Resolution: `1k` / `2k` / `4k`
- Ratio suffix: `1x1` / `16x9` / `9x16` / `4x3` / `3x4` / `21x9` / `5x4` / `4x5`
- Examples:
  - `firefly-nano-banana-pro-2k-16x9`
  - `firefly-nano-banana-pro-4k-1x1`

### 3.2 Video Models

**Sora2 Series**:

- Pattern: `firefly-sora2-{duration}-{ratio}`
- Duration: `4s` / `8s` / `12s`
- Ratio: `9x16` / `16x9`
- Examples:
  - `firefly-sora2-4s-16x9`
  - `firefly-sora2-8s-9x16`

**Sora2 Pro Series**:

- Pattern: `firefly-sora2-pro-{duration}-{ratio}`
- Duration: `4s` / `8s` / `12s`
- Ratio: `9x16` / `16x9`
- Examples:
  - `firefly-sora2-pro-4s-16x9`
  - `firefly-sora2-pro-8s-9x16`

**Veo31 Series**:

- Pattern: `firefly-veo31-{duration}-{ratio}-{resolution}`
- Duration: `4s` / `6s` / `8s`
- Ratio: `16x9` / `9x16`
- Resolution: `1080p` / `720p`
- Supports up to 2 reference images:
  - 1 image: first-frame reference
  - 2 images: first-frame + last-frame reference
- Audio defaults to enabled
- Examples:
  - `firefly-veo31-4s-16x9-1080p`
  - `firefly-veo31-6s-9x16-720p`

**Veo31 Ref Series** (reference-image mode):

- Pattern: `firefly-veo31-ref-{duration}-{ratio}-{resolution}`
- Duration: `4s` / `6s` / `8s`
- Ratio: `16x9` / `9x16`
- Resolution: `1080p` / `720p`
- Always uses reference image mode (not first/last frame mode)
- Supports up to 3 reference images
- Examples:
  - `firefly-veo31-ref-4s-9x16-720p`
  - `firefly-veo31-ref-6s-16x9-1080p`
  - `firefly-veo31-ref-8s-9x16-1080p`

**Veo31 Fast Series**:

- Pattern: `firefly-veo31-fast-{duration}-{ratio}-{resolution}`
- Duration: `4s` / `6s` / `8s`
- Ratio: `16x9` / `9x16`
- Resolution: `1080p` / `720p`
- Supports up to 2 reference images:
  - 1 image: first-frame reference
  - 2 images: first-frame + last-frame reference
- Audio defaults to enabled
- Examples:
  - `firefly-veo31-fast-4s-16x9-1080p`
  - `firefly-veo31-fast-6s-9x16-720p`

## 4) API Usage

### 4.1 Unified endpoint: `/v1/chat/completions`

Text-to-image:

```bash
curl -X POST "http://127.0.0.1:6001/v1/chat/completions" \
  -H "Authorization: Bearer <service_api_key>" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "flux",
    "messages": [{"role":"user","content":"a cinematic mountain sunrise"}]
  }'
```

Image-to-image (pass image in latest user message):

```bash
curl -X POST "http://127.0.0.1:6001/v1/chat/completions" \
  -H "Authorization: Bearer <service_api_key>" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "flux",
    "messages": [{
      "role":"user",
      "content":[
        {"type":"text","text":"turn this photo into watercolor style"},
        {"type":"image_url","image_url":{"url":"https://example.com/input.jpg"}}
      ]
    }]
  }'
```

Text-to-video:

```bash
curl -X POST "http://127.0.0.1:6001/v1/chat/completions" \
  -H "Authorization: Bearer <service_api_key>" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "firefly-sora2-4s-16x9",
    "messages": [{"role":"user","content":"a drone shot over snowy forest"}]
  }'
```

Image-to-video:

```bash
curl -X POST "http://127.0.0.1:6001/v1/chat/completions" \
  -H "Authorization: Bearer <service_api_key>" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "firefly-sora2-8s-9x16",
    "messages": [{
      "role":"user",
      "content":[
        {"type":"text","text":"animate this character walking forward"},
        {"type":"image_url","image_url":{"url":"https://example.com/character.png"}}
      ]
    }]
  }'
```

### 4.2 Image endpoint: `/v1/images/generations`

```bash
curl -X POST "http://127.0.0.1:6001/v1/images/generations" \
  -H "Authorization: Bearer <service_api_key>" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "flux",
    "prompt": "futuristic city skyline at dusk"
  }'
```

### 4.3 Video Reference Image Semantics

| Model Type | 1 Image | 2 Images | 3 Images |
|-------------|---------|----------|----------|
| `firefly-veo31-*` / `firefly-veo31-fast-*` | First frame | First + last frame | Not supported |
| `firefly-veo31-ref-*` | Reference | Reference | Reference |

## 5) Cookie Import

### Step 1: Export using the Browser Extension (Recommended)

This project includes a companion browser extension to help you easily export required cookies from the Adobe Firefly page.

- Extension source: `browser-cookie-exporter/`
- Exports a minimal `cookie_*.json` (containing only the `cookie` field)
- Detailed instructions: `browser-cookie-exporter/README.md`

**Important: Use incognito window for better results.**

- In the same browser's regular window, if you log into multiple Adobe accounts and export repeatedly, the later login typically invalidates the earlier account's cookies
- This means: cookies exported first may expire quickly, showing as refresh failures, account disconnections, or only keeping the last exported account
- **Safest approach: Log in and export each account in a separate incognito window, then import separately**

**Installation & Usage:**

1. Open Chrome or Edge extension management: `chrome://extensions`
2. Enable "Developer mode" in the top right
3. Click "Load unpacked" and select the `browser-cookie-exporter/` directory from this project
4. Open the extension details and enable "Allow in incognito"
5. Open a new incognito window for each Adobe account
6. Log in to [Adobe Firefly](https://firefly.adobe.com/) in the corresponding incognito window
7. Click the extension icon in your browser toolbar and select the export scope
8. Click "Export Minimal JSON" and save the file

### Step 2: Import into the Project

Once you have the exported JSON file, follow these steps to import it:

1. Access and log in to the admin UI (default `http://127.0.0.1:6001/`)
2. Navigate to the "Token 管理" (Token Management) tab
3. Click the "导入 Cookie" (Import Cookie) button
4. **Option A:** Paste the JSON content into the text box; **Option B:** Upload the exported `.json` file directly
5. Click "Confirm Import" (the service will verify the cookies and run an initial refresh)
6. Upon success, the token will appear in the list with `自动刷新` (Auto Refresh) set to "Yes"

**Batch Import:** The import dialog supports uploading multiple files at once or pasting a JSON array containing multiple account credentials.

## 6) Storage Paths

- Generated media: `data/generated/`
- Request logs: `data/request_logs.jsonl`
- Token pool: `config/tokens.json`
- Service config: `config/config.json`
- Refresh profile (local private): `config/refresh_profile.json`

**Generated Media Retention Policy:**

- Files under `data/generated/` are preserved and served via `/generated/*`
- Auto-prune is enabled by size threshold (oldest files first)
  - `generated_max_size_mb` (default `1024`)
  - `generated_prune_size_mb` (default `200`)
- When total generated file size exceeds `generated_max_size_mb`, service deletes old files until at least `generated_prune_size_mb` is reclaimed and total size falls back under threshold

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=leik1000/adobe2api&type=Date)](https://star-history.com/#leik1000/adobe2api&Date)
