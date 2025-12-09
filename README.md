# AI Agent Base — Gemini Multimodal Agent

This repository contains a full-stack prototype for a multimodal AI agent. The project includes a FastAPI-based backend that integrates with AI services (Gemini / Google GenAI) and MongoDB for persistence, plus a Vite + React frontend scaffold for the UI.

**Primary Focus**: backend development and AI tooling to generate and support backend logic. The frontend UI is scaffolded and intended to be enhanced using AI tools for design and components.

**Key Features**
- **Backend (FastAPI)**: REST API and endpoints for chat and authentication, CORS enabled, MongoDB connection management, and integration with AI LLM clients.
- **AI tooling**: Agents and clients in `app/agents` designed to orchestrate model calls and image handling.
- **Frontend (React + Vite)**: Minimal UI components to interact with the API (auth, chat, sidebar, profile).

**Repository Structure**
- **`Backend/`**: Python backend code (FastAPI)
  - `main.py` — FastAPI app (startup/shutdown hooks, router includes)
  - `app/api/v1/` — routers (e.g., `chat_router.py`, `auth_router.py`)
  - `app/agents/` — LLM clients, multimodal agents, image handler
  - `app/core/` — configuration and security helpers
  - `app/database/` — DB connection and models
  - `app/schemas/` — Pydantic schemas
  - `requirements.txt` — pinned Python dependencies
  - `.env` — environment variables (not committed)

- **`Frontend/`**: React + Vite application
  - `src/components/` — `AuthForm.jsx`, `ChatInterface.jsx`, `Sidebar.jsx`, `Profile.jsx`
  - `package.json`, `vite.config.js` — frontend tooling

**Backend Setup (Local)**
- Prerequisites: Python 3.11+ (or a compatible 3.10/3.12 runtime), Node/npm for frontend if using locally.

1. Create and activate a virtual environment (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install --upgrade pip
pip install -r Backend\requirements.txt
```

3. Environment variables: copy or create `Backend\.env` and set variables for MongoDB, auth secrets, and AI keys (example keys):

- `MONGO_URI` — MongoDB connection string
- `JWT_SECRET` — secret for signing JWTs
- `GOOGLE_API_KEY` / `GENAI_KEY` — API keys for AI services

4. Run the backend development server:

```powershell
cd Backend
uvicorn main:app --reload
```

Then open `http://127.0.0.1:8000` to confirm the root message. The API docs are available at `http://127.0.0.1:8000/docs` (Swagger UI).

**Notable Endpoints**
- `GET /` — health / root message
- `POST /api/v1/...` — chat and auth routes provided under `app/api/v1/` (see router files for full details)

**Frontend Quick Start**
1. From repository root, install and run frontend:

```powershell
cd Frontend
npm install
npm run dev
```

2. Frontend will default to a Vite dev server (port shown in output). Configure `Frontend/src/utils/helpers.js` or the code to point at the backend API URL if cross-origin requests need a specific host or port.

**Development Notes & Recommendations**
- Use the `app/agents` folder as the main entry for AI logic. These modules orchestrate LLM calls, image handling, and multimodal flows.
- Keep API contracts (Pydantic schemas in `app/schemas`) synchronized with frontend forms/components.
- Add a `README-backend.md` inside `Backend/` if you expect more detailed ops notes (migrations, indexes, seed data).
- Consider adding tests for critical flows (auth, chat message storage, agent orchestration).

**Suggested Next Steps**
- Provide a sample `.env.example` with placeholder keys.
- Add a simple Postman/Insomnia collection or curl examples for common endpoints.
- Add CI to run linting and basic tests on PRs.

**Contact / Ownership**
- Backend: focus and main development area.
- Frontend: scaffolded; use AI tools to iterate on UI and components.
 
**Deployment**
- Use Render, GitHub Actions, or another hosting provider of your choice. Prefer managed services for production deployments and keep secrets in the provider's environment variables (do not commit `.env` files).

**Architecture Diagram**
- **Overview**: The application is organized as a two-tier app (API backend + SPA frontend) with MongoDB as the primary datastore. AI calls are made from `app/agents` to an external GenAI provider. Image uploads are proxied to Cloudinary for storage and CDN delivery.

  ASCII diagram:

  ```
  [Frontend (Vite/React)] <---> [FastAPI Backend (uvicorn)]
                                   |
                                   +--> [AI Services (Google GenAI / Gemini)]
                                   |
                                   +--> [Cloudinary (image storage)]
                                   |
                                   +--> [MongoDB (ConversationHistory, Users)]
  ```

- **Components**:
  - `Frontend` — React components call the backend's REST endpoints for auth and chat.
  - `Backend` — `app/agents` orchestrates model calls and image uploads; `app/api/v1` exposes routes; `app/database` manages persistence.
  - `AI Services` — external model provider used for generating responses. Keep API keys in secure env variables.

**Suggested Additional Files**
- `Backend/.env.example` — example env file (created in the repo) to document runtime variables.
- `Backend/postman_collection.json` — a Postman v2.1 collection with example requests for signup, login, and chat.
- `Backend/curl_examples.md` — curl commands demonstrating signup/login/chat flows.

**Postman Import Instructions**
- The repository includes a Postman collection and an environment file to speed up manual testing.

1. Import the collection:
  - In Postman, choose `File > Import` and select `Backend/postman_collection.json`.

2. Import the environment (optional but recommended):
  - Choose `Environments > Import` and select `Backend/postman_environment.json`.
  - Open the environment and set `base_url` to your backend URL (e.g., `http://127.0.0.1:8000` or your Render URL).

3. Run requests:
  - Use the `Signup` request to create a user, then use `Login` to obtain the `access_token`.
  - Copy the `access_token` value into the environment variable `auth_token` (no `Bearer ` prefix needed in the variable; the collection uses `Bearer {{auth_token}}`).

4. Test Chat endpoints (with or without an image):
  - Use `Chat (no image)` for text-only requests.
  - Use `Chat (with image)` to upload an image file.

Notes:
- If testing anonymously (no auth header), remove the `Authorization` header from the chat requests or leave `auth_token` empty.
- If you deploy to Render or another host, update the `base_url` environment variable to the published backend URL.

If you want, I can also create example deployment artifacts (for Docker, Render, or GitHub Actions) and add them to the repository. Tell me which option you prefer.
 
**Render Deployment (GitHub)**

- This project can be deployed directly from GitHub to Render (https://render.com). Below are concise steps and recommended settings for both backend and frontend services.

- Backend (FastAPI) — Service type: **Web Service**
  - Connect your GitHub repository to Render and create a new Web Service using the `Backend` directory as the root.
  - Build Command: `pip install -r Backend/requirements.txt`
  - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
  - Environment: Set the following Render environment variables (in Dashboard > Environment > Environment Variables):
    - `MONGO_URI` — e.g. `mongodb+srv://...` (your Mongo connection)
    - `MONGO_DB` — database name
    - `JWT_SECRET` — strong random value
    - `ACCESS_TOKEN_EXPIRE_MINUTES` — e.g. `60`
    - `GENAI_API_KEY` or `GOOGLE_API_KEY` — AI provider key
    - `CLOUDINARY_URL` (if used)
    - `FRONTEND_ORIGINS` — frontend URL (for CORS)
  - Health checks: Render will use the start command; verify the root path (`/`) responds.

- Frontend (Vite React) — Service type: **Static Site** (recommended) or **Web Service**
  - For a Static Site on Render:
    - Connect repo, point to `Frontend` as the root.
    - Build Command: `npm install && npm run build`
    - Publish Directory: `Frontend/dist`
  - If using a Web Service (Node) instead, use a start command that serves the built files (e.g., `serve -s dist`), and ensure `serve` is installed as a dependency.

- Auto-deploy: Enable auto-deploy from the branch you push to (e.g., `main` or `master`). Render will build on each push.

- Secrets & Security:
  - Use Render's environment variables for secrets (do not commit `.env` to repo).
  - Restrict CORS in production to the published frontend origin.

**Repository Ownership & Copyright**

All code and assets in this repository are copyrighted by

Keshav Chandra Pandit — GitHub: `keshavpandit92`

© Keshav Chandra Pandit


