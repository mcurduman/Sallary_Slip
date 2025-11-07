# PaySlip Project

## Overview
A full-stack payroll management system with FastAPI backend and React (Vite) frontend. Supports employee management, payroll generation, CSV export, and email sending.

## Check Wiki for more details about the implementation

## Structure
- `payslip-backend/` — FastAPI backend (Python)
- `payslip-frontend/` — React frontend (TypeScript, Vite)
- `docker-compose.yml` — Multi-service orchestration (frontend, backend, db, redis)

## Quick Start
1. **Build & Run All Services:**
   ```sh
   docker-compose up --build -d
   ```
2. **Frontend:**
   - Dev mode: http://localhost:5173
   - Production (Nginx): http://localhost:3000
3. **Backend API:**
   - http://localhost:5050
4. **Database:**
   - Postgres on port 5543
5. **Redis:**
   - Redis on default port 6379

## Features
- Employee & manager dashboards
- Payroll slip generation & CSV export
- Email sending (Mailtrap)
- Dockerized for easy deployment

## Development
- Frontend: `npm run dev` in `payslip-frontend`
- Backend: `uvicorn app.main:app --reload --port 5050` in `payslip-backend`

## Notes
- Generated files (reports, slips) are saved in `payslip-backend/manager_reports`.
- Environment variables are set in `.env` files.
