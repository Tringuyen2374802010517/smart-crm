
# Smart CRM – Deployment Guide

**Project:** Smart CRM – Mekong Mobile (L4)
**Deployment Method:** Docker Compose
**Release:** v1.0

## 1. Requirements

The following tools are required to deploy Smart CRM:

- Git
- Docker Desktop with Docker Compose v2
- Available ports 8000 and 5173
- Internet connection for downloading Docker images and dependencies

Python and Node.js do not need to be installed directly on the host machine when deploying through Docker.

## 2. Setup Steps

**Step 1: Clone the repository**

To deploy from the published v1.0 release tag:

```bash
git clone https://github.com/Tringuyen2374802010517/smart-crm.git
cd smart-crm
git checkout v1.0
```

**Step 2: Configure environment variables**

```bash
cp .env.example .env
```

Edit `.env` and replace the sample Manager password with a strong, private password before the first deployment.

**Step 3: Build and start the application**

```bash
docker compose up -d --build --wait
```

Docker Compose builds and starts two services:

- **Backend:** FastAPI with Uvicorn, running on port 8000.
- **Frontend:** Nginx serving the built Vite application on port 5173.

The frontend uses Nginx to forward `/api/` requests to the backend service.

**Step 4: Check service status**

```bash
docker compose ps
```

Both services should report a healthy status.

**Step 5: Access the application**

- Frontend: http://localhost:5173/
- Backend healthcheck: http://localhost:8000/health
- Nginx proxy healthcheck: http://localhost:5173/api/health

**Step 6: Stop the application**

```bash
docker compose down
```

This command stops and removes the containers without deleting the persistent database volume.

Do not run `docker compose down -v` unless deleting the Docker-managed database volume is intentional.

## 3. Environment Variables

| Variable | Description | Docker Deployment |
|---|---|---|
| `DEMO_ADMIN_USERNAME` | Username for the initial Manager account | Required |
| `DEMO_ADMIN_PASSWORD` | Password for the initial Manager account (minimum 8 characters) | Required |
| `DATABASE_URL` | Example database connection configuration | Not passed to the current Docker containers |
| `APP_HOST` | Example application host configuration | Not passed to the current Docker containers |
| `APP_PORT` | Example application port configuration | Not passed to the current Docker containers |
| `SECRET_KEY` | Reserved example configuration | Not passed to the current Docker containers |

The application stores SQLite data in `/app/data/smartcrm.db`, using the Docker named volume `crm_data`.

The backend accesses the same database through `/app/smartcrm.db`.

The initialization script creates the Manager account only if the configured username does not already exist. Changing `DEMO_ADMIN_PASSWORD` later does not automatically update an existing account.

The password in `.env.example` is a placeholder. Replace it with a strong, private password in `.env` before deployment.

## 4. Sample Data

During startup, the initialization script applies:

- `docs/schema.sql` to create database tables.
- `docs/seed.sql` to initialize sample records.
- Manager account initialization using the configured credentials.

The previously recorded clean-room deployment on November 10, 2026 reported the following initial records:

| Database Table | Record Count |
|---|---:|
| `ticket` | 3 |
| `technician` | 3 |
| `technician_skill` | 3 |
| `assignment` | 0 |
| `appointment` | 0 |
| `crm_user` | 1 |

The Manager account is stored in the `crm_user` table with a hashed password.

These counts represent the initial demonstration dataset. They may change after application usage.

The final release should be checked again in a fresh environment to confirm these counts.

## 5. Verify It Works

**Check container health**

```bash
docker compose ps
```

Expected result: both backend and frontend containers are healthy.

**Verify backend connectivity**

```bash
curl -i http://localhost:8000/health
```

Expected HTTP status: `200 OK`.

Expected JSON response:

```json
{"status":"healthy","database":"connected"}
```

**Verify Nginx reverse proxy**

Run:

```bash
curl -i http://localhost:5173/api/health
```

Expected result: HTTP 200 with the same healthcheck response.

**Verify authentication protection**

Run:

```bash
curl -i http://localhost:8000/tickets
```

Expected result: HTTP 401 when no Bearer token is provided.

The same authentication protection is expected for protected technician, appointment and assignment API routes.

**Verify clean-room deployment**

A previous isolated deployment was recorded using separate Docker containers and a separate SQLite volume.

Clean-room verification endpoints:

- Frontend: `http://localhost:15173/`
- Backend healthcheck: `http://localhost:18000/health`
- Nginx proxy healthcheck: `http://localhost:15173/api/health`

The previous verification reported successful frontend availability, backend healthcheck, Nginx proxy, Manager authentication and database isolation checks.

A fresh clone of the previously published GitHub `v1.0` tag has been verified in an isolated Docker environment. After final documentation is committed and the release tag is synchronized, verify the final published tag again before claiming final release verification.

**Run regression tests**

From the project root, with Python and the project test dependencies installed:

```bash
python3 -m pytest -q
```

Previously recorded regression result: 100 tests passed, with one deprecation warning.

The final release should reproduce this result, and the corresponding test output should be retained as evidence.

**Deployment limitations**

- The provided credentials are for demonstration purposes only.
- HTTPS, login rate limiting and additional production security hardening are not configured.
- The Docker deployment is intended for local development and academic demonstration.

## 6. Release Status

The Docker deployment has previously been verified locally.

The `v1.0` release tag exists on GitHub, but the final documentation updates must be committed and included in the submitted release.

Before final submission:

1. Confirm that all final documentation is included in the release.
2. Verify the published `v1.0` tag points to the intended final commit.
3. Perform a fresh-clone deployment from that tag.
4. Confirm both Docker services are healthy.
5. Run the required regression tests and retain the output.
6. Capture clean-room deployment evidence for the final report.

Do not mark the final release as fully verified until these checks pass.

## 7. Optional Public Deployment – Render

This section documents the optional public deployment used for the BT3 bonus evaluation.

### 7.1. Deployment architecture

The Render deployment uses `Dockerfile.render` to build a single container containing the FastAPI backend and the Nginx-served frontend.

- Frontend build: Node.js 22, `npm ci`, `npm run build`.
- Backend runtime: Python 3.12 with application dependencies.
- Nginx listens on port `10000` and serves the frontend.
- Requests under `/api/` are forwarded to FastAPI at `127.0.0.1:8000`.
- SQLite database location: `/app/data/smartcrm.db`.
- Startup script: `scripts/render-start.sh`.
- Database initialization runs before the application starts.

### 7.2. Render configuration

Create a Render Web Service connected to the public GitHub repository.

1. Select the Docker runtime.
2. Use `Dockerfile.render` as the Dockerfile path.
3. Configure the application port as `10000`.
4. Configure the required environment variables in the Render dashboard, without committing their secret values to Git.
5. Attach persistent storage at `/app/data` if supported by the selected Render service plan.
6. Deploy and inspect the application logs and public URL.

Relevant environment variable names in the project configuration:

- `APP_HOST`
- `APP_PORT`
- `DATABASE_URL`
- `DEMO_ADMIN_USERNAME`
- `DEMO_ADMIN_PASSWORD`
- `SECRET_KEY`

The exact variables required by the Render service must be checked against its deployed configuration. Do not publish passwords or secret keys.

### 7.3. Public deployment verification

The following evidence has been retained under `evidence/Render/`:

1. `BT3_Render_01_Deployment_Live.png`
2. `BT3_Render_02_Public_Website.png`
3. `BT3_Render_03_Login_Success.png`
4. `BT3_Render_04_Eligible_Technicians.png`
5. `BT3_Render_05_Assignment_Success.png`
6. `BT3_Render_06_Assignment_Persisted_After_Refresh.png`
7. `BT3_Render_07_SQLite_Persistence_After_Restart.png`

The public website URL must be included on the final BT3 PDF cover page.

### 7.4. Limitations

- The local Docker Compose deployment and Render deployment use different container layouts.
- Public deployment evidence does not establish that every production security control is complete.
- SQLite persistence depends on the actual storage configuration and must not be assumed solely from the Dockerfile.
- Final availability should be verified before submission.
