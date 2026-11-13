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

The clean-room deployment was verified on November 10, 2026 with the following initial records:

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

The same authentication protection applies to the technician, appointment and assignment API routes.

**Verify clean-room deployment**

The application was also deployed in an isolated clean-room environment using separate Docker containers and a separate SQLite volume.

Clean-room verification endpoints:

- Frontend: `http://localhost:15173/`
- Backend healthcheck: `http://localhost:18000/health`
- Nginx proxy healthcheck: `http://localhost:15173/api/health`

The clean-room deployment passed frontend availability, backend healthcheck, Nginx proxy, Manager authentication and database isolation checks.

**Run regression tests**

From the project root:

```bash
python -m pytest -q
```

Verified result: 87 tests passed, with one deprecation warning.

**Deployment limitations**

- The provided credentials are for demonstration purposes only.
- HTTPS, login rate limiting and additional production security hardening are not configured.
- The Docker deployment is intended for local development and academic demonstration.

## 6. Release Status

The Docker deployment and clean-room verification have been completed locally.

The `v1.0` release tag has been published on GitHub. Final documentation updates must be included in the submitted release.
