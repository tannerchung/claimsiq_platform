# ClaimsIQ - Health Insurance Claims Platform

## Overview
ClaimsIQ is a health insurance claims processing platform built with Python. It provides real-time insights into claims data with risk scoring, filtering, and analytics capabilities.

## Technology Stack
- **Frontend**: Reflex (Python framework that compiles to React)
- **Backend**: FastAPI (Python async web framework)
- **Database**: PostgreSQL (Replit database)
- **Data Processing**: Pandas
- **Port Configuration**: Frontend on 5000, Backend on 8001

## Project Structure
```
claimsiq-platform/
├── backend/                 # FastAPI backend
│   ├── models/              # Data models and schemas
│   ├── services/            # Business logic
│   └── routes/              # API endpoints
├── claimsiq/                # Reflex frontend
│   ├── components/          # Reusable UI components
│   └── pages/               # Page components
├── scripts/                 # Database initialization scripts
├── data/sample/             # Sample data files
└── rxconfig.py              # Reflex configuration
```

## Features
- **Dashboard**: Real-time claims metrics and KPIs
- **Claims Table**: Sortable, filterable claims list with pagination
- **Risk Scoring**: Automatic high-risk claim detection
- **Provider Analytics**: Provider performance metrics
- **API Endpoints**: RESTful API for claims and analytics data

## Recent Changes
- 2025-11-04: Initial setup in Replit environment
  - Configured PostgreSQL database integration
  - Set up Reflex on port 5000 with proper host settings (0.0.0.0)
  - Loaded 1000 sample claims and 50 providers into database
  - Backend API running on port 8001

## Architecture
The application uses Reflex which combines frontend and backend in a single Python codebase:
- Reflex compiles Python components to React
- Built-in WebSocket connection between frontend and backend
- FastAPI backend integrated with Reflex state management

## Database
- Using Replit's managed PostgreSQL database
- Tables: `claims`, `providers`
- Sample data loaded via scripts/load_sample_data.py

## User Preferences
None specified yet.

## Configuration Notes
- Frontend runs on 0.0.0.0:5000 (required for Replit proxy)
- Backend runs on 0.0.0.0:8001
- Database URL configured via environment variable
