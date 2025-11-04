# AGENTS.md - MVP Coding Instructions for ClaimsIQ

This document provides context and instructions for developers working on the ClaimsIQ MVP (Minimum Viable Product).

## Mission - MVP ONLY (7 Days)

Build a fully functional, demo-ready health insurance claims intelligence platform in 7 days using Python backend + Reflex frontend. Deployable to Replit with a shareable link.

**CRITICAL:** This is MVP only. See "DO NOT BUILD" section below for features to skip entirely.

## Quick Reference

| Item | Value |
|------|----------|
| **Repo Name** | claimsiq-platform |
| **Product Name** | ClaimsIQ |
| **Backend** | Python 3.10+, FastAPI |
| **Frontend** | Reflex (Python-based React) |
| **Database** | SQLite (MVP only) |
| **Deployment** | Replit |
| **Timeline** | 7 days to MVP |

## Core Principles

### 1. **Shipping > Perfection**
- Focus on functional MVP features over polish
- 80% working today beats 20% perfect tomorrow
- Simple solutions that work now beat complex ones for later

### 2. **Demo-Driven Development**
- Every component must show in the demo
- If it can't be shown, don't build it
- Visual impact matters

### 3. **Data-First**
- Load real insurance data (Kaggle dataset) immediately
- Every feature works with actual claims data
- Test with sample data, showcase with real data

### 4. **DRY & Maintainable**
- Write reusable components
- Keep backend logic separate from frontend
- Use consistent patterns throughout

---

## DO NOT BUILD - Enterprise Features

**These are completely out of scope for MVP. Do not implement them.**

❌ Authentication / JWT tokens  
❌ Role-based access control (RBAC)  
❌ TLS/HTTPS security layers  
❌ Audit logging framework  
❌ Multi-tenant support  
❌ Database migrations (Alembic)  
❌ Redis caching  
❌ Advanced clustering algorithms  
❌ Provider comparison page  
❌ Policy performance page  
❌ PDF/CSV export functionality  
❌ Docker containerization  
❌ Error handling framework (beyond basic)  
❌ Monitoring/observability systems  
❌ Webhooks  
❌ Real-time WebSocket updates  
❌ Auto-approval workflows  
❌ Alerts & notifications  
❌ Email integrations  
❌ Mobile support  
❌ Slack integration  

**Note:** For the demo presentation, you CAN say these features exist or are coming. But do NOT implement them.

---

## Implementation Tasks - 6 Core Tasks

### Task 1: Project Setup (Day 1 morning, ~2 hours)
- Initialize Reflex project structure
- Set up FastAPI backend
- Create SQLite database schema (simple, no migrations)
- Create requirements.txt with essential packages only
- Get local dev environment running

**Deliverable:** `reflex run` and `uvicorn backend.app:app --reload` both work

### Task 2: Data Ingestion (Day 1 afternoon, ~3 hours)
- Load Kaggle insurance CSV with Pandas
- Validate required columns exist
- Convert data types (dates, numbers)
- Store in SQLite using simple INSERT statements
- Cache DataFrame in memory for fast access

**Deliverable:** 50K-100K claims loaded and queryable

### Task 3: Backend API - 3 Core Endpoints (Day 2, ~4 hours)
```
GET /api/claims/summary
  → {total_claims, approved_count, pending_count, flagged_count, approval_rate}

GET /api/claims?status=pending&limit=100
  → List of claims with optional filtering

GET /api/analytics/risks
  → {high_risk_count, risk_distribution, top_10_high_risk_claims}
```

**Deliverable:** All 3 endpoints return correct data

### Task 4: Frontend Dashboard Layout (Day 3, ~3 hours)
- Create main dashboard page
- Add 4 metric cards (total, approved%, pending, flagged)
- Add navbar with title
- Connect to API and display real data
- No authentication needed

**Deliverable:** Dashboard loads with real data in <3 seconds

### Task 5: Claims Table + Filtering (Day 4, ~4 hours)
- Display table of claims with columns: ID, Amount, Status, Provider, Date
- Make columns sortable (click to sort)
- Add filters: Status dropdown, Date range picker
- Filters update table instantly
- Show paginated view (100 rows per page)

**Deliverable:** Filtering and sorting work smoothly

### Task 6: Charts + Risk Highlighting (Day 5-6, ~5 hours)
- Add line chart showing approval trends over time
- Add pie chart showing status distribution (approved/pending/flagged)
- Highlight high-risk claims in red on table
- Simple risk score: Flag if amount > $5,000 OR pending > 30 days
- Show risk reason on hover

**Deliverable:** Charts render without lag, risk highlighting works

### Task 7: Testing & Polish (Day 6-7, ~3 hours)
- Verify all features work end-to-end
- Check performance targets met
- Test with different data sizes (100K, 500K claims)
- Deploy to Replit
- Test deployment link works

**Deliverable:** Shareable Replit link that works flawlessly

---

## Architecture Overview (Simple)

```
┌──────────────────────────────────────────────────────┐
│                  REFLEX FRONTEND                     │
│              (Python compiles to React)              │
└──────────────────┬───────────────────────────────────┘
                   │ HTTP/REST
                   ▼
┌──────────────────────────────────────────────────────┐
│              FASTAPI BACKEND                         │
│        (Python async HTTP server)                    │
│  - Route handlers for 3 API endpoints                │
│  - Request/response validation                       │
│  - Business logic (risk scoring, filtering)          │
└──────────┬─────────────────────────┬────────────────┘
           │                         │
           ▼                         ▼
    ┌─────────────┐          ┌────────────────┐
    │ SQLite DB   │          │ In-Memory Cache│
    │ (claimsiq.  │          │ (Pandas DF)    │
    │  db)        │          │                │
    └─────────────┘          └────────────────┘
```

---

## Technology Stack (MVP Only)

| Layer | Tech | Why |
|-------|------|-----|
| **Frontend** | Reflex | Python-native, compiles to React |
| **Backend** | FastAPI | Async, fast, auto-docs |
| **Data Processing** | Pandas | Easy filtering & analysis |
| **Database** | SQLite | Zero setup, file-based |
| **Deployment** | Replit | Simple, shareable link |

**NOT INCLUDED:** Redis, Docker, PostgreSQL, authentication, migrations

---

## File Structure (Simplified)

```
claimsiq-platform/
│
├── backend/
│   ├── app.py                   # FastAPI application
│   ├── config.py                # Configuration
│   ├── models/
│   │   ├── claim.py             # Claim data model
│   │   └── schema.py            # Pydantic schemas
│   ├── services/
│   │   ├── data_service.py      # Load & cache data
│   │   ├── analytics_service.py # Risk scoring
│   │   └── claims_service.py    # Claim queries
│   └── routes/
│       ├── claims.py            # /api/claims endpoints
│       └── analytics.py         # /api/analytics endpoints
│
├── frontend/claimsiq/
│   ├── state.py                 # Reflex state management
│   ├── index.py                 # Homepage
│   ├── pages/
│   │   └── dashboard.py         # Main dashboard view
│   ├── components/
│   │   ├── cards.py             # Metric cards
│   │   ├── tables.py            # Data tables
│   │   ├── charts.py            # Recharts integration
│   │   ├── filters.py           # Filter controls
│   │   └── navbar.py            # Top navigation
│   └── rxconfig.py              # Reflex config
│
├── scripts/
│   ├── init_db.py               # Initialize database
│   └── load_sample_data.py      # Load Kaggle dataset
│
├── data/
│   ├── sample/
│   │   └── claims_sample.csv    # Sample data (10K rows)
│   └── processed/
│       └── claims_cache.pkl     # Cached dataframe
│
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment template
└── README.md                    # Quick start guide
```

---

## Reflex Patterns (MVP Only)

### Simple State Management

```python
# frontend/claimsiq/state.py
class State(rx.State):
    """Central state for the app"""
    
    # Data
    claims_data: list[dict] = []
    summary_stats: dict = {}
    
    # Filters
    selected_status: str = "all"
    date_range: tuple[str, str] = ("2020-01-01", "2024-12-31")
    
    # UI
    is_loading: bool = False
    error_message: str = ""
    
    # Methods
    def load_summary(self):
        """Fetch summary from API"""
        self.is_loading = True
        try:
            response = rx.client.get("http://localhost:8000/api/claims/summary")
            self.summary_stats = response.json()
        except Exception as e:
            self.error_message = str(e)
        finally:
            self.is_loading = False
    
    def filter_claims(self):
        """Apply filters locally"""
        pass
```

### Simple Component Pattern

```python
# frontend/claimsiq/components/cards.py
def metric_card(label: str, value: str, color: str = "blue") -> rx.Component:
    """Reusable metric card"""
    return rx.box(
        rx.vstack(
            rx.text(label, size="sm", color="gray"),
            rx.text(value, size="lg", weight="bold"),
            spacing="1",
        ),
        padding="4",
        border_width="1px",
        border_color=f"{color}.200",
        border_radius="md",
        bg=f"{color}.50",
    )
```

### Simple API Integration

```python
# frontend/claimsiq/state.py
import httpx

async def load_data_from_api(self):
    """Load data from backend"""
    async with httpx.AsyncClient() as client:
        response = await client.get("http://localhost:8000/api/claims/summary")
        if response.status_code == 200:
            self.summary_stats = response.json()
```

---

## API Endpoint Contracts (MVP Only)

### GET /api/claims/summary
```json
{
  "total_claims": 50000,
  "approved_count": 34000,
  "pending_count": 12000,
  "flagged_count": 4000,
  "approval_rate": 0.68
}
```

### GET /api/claims?status=pending&limit=100
```json
{
  "claims": [
    {
      "id": "CLM001",
      "policy_id": "POL123",
      "claim_date": "2024-10-15",
      "claim_amount": 2500.00,
      "status": "pending",
      "provider_id": "PROV456",
      "risk_score": 0.45
    }
  ],
  "total": 12000
}
```

### GET /api/analytics/risks
```json
{
  "high_risk_count": 1234,
  "medium_risk_count": 5678,
  "low_risk_count": 43088,
  "top_high_risk_claims": [
    {
      "id": "CLM999",
      "amount": 45000,
      "reason": "Amount > $5000",
      "risk_score": 0.92
    }
  ]
}
```

---

## Testing & QA Checklist

Before demo/deployment:

- [ ] App loads in <3 seconds
- [ ] Dashboard displays real data
- [ ] Filters update table instantly
- [ ] Charts render smoothly
- [ ] Can sort all table columns
- [ ] Risk highlighting works
- [ ] API endpoints return correct JSON
- [ ] No console errors
- [ ] Works on different screen sizes
- [ ] Can handle 500K claims without lag

---

## Deployment Checklist

Before sharing Replit link:

- [ ] All dependencies in requirements.txt
- [ ] Environment variables in .env
- [ ] Database initialized with sample data
- [ ] Both API and frontend running
- [ ] No hardcoded paths or credentials
- [ ] Link tested from fresh Replit load
- [ ] README.md is accurate

---

## Common Patterns (MVP)

### ✅ DO
- Use Reflex's reactive state system
- Keep backend logic in Python services
- Cache data in state to avoid repeated API calls
- Test with real data early
- Start with simple visualizations
- Handle API call failures gracefully

### ❌ DON'T
- Write custom JavaScript
- Pass huge data through state
- Make API calls directly from components
- Hardcode values
- Forget error handling
- Over-engineer initial features
- Use authentication/permissions

---

## Performance Targets (MVP)

| Operation | Target |
|-----------|--------|
| Page load | <3 seconds |
| API response | <500ms |
| Filter update | <500ms |
| Chart render | <1 second |
| Data ingestion (500K records) | <2 seconds |

---

## Debugging Tips

### "API not connecting"
```bash
curl http://localhost:8000/api/claims/summary
# Should return JSON, not error
```

### "Reflex app won't start"
```bash
reflex clean
pip install --upgrade reflex
reflex run
```

### "Data loading slowly"
- Check if CSV is huge (>100MB)
- Add caching: don't reload on every filter
- Use pagination: show 100 rows, not 50K

### "Charts not rendering"
- Verify data structure matches Recharts format
- Check browser console for JS errors
- Ensure data has required fields

---

## Emergency Contacts

- **Stuck on Reflex?** Check reflex.dev docs
- **API issues?** Test with curl first
- **Data questions?** Check Kaggle dataset docs
- **General?** Ask james@sixfold.ai

---

**Version:** 2.0 (MVP Focused)
**Last Updated:** 2025-11-03
**Focus:** 7-day MVP only, no enterprise features