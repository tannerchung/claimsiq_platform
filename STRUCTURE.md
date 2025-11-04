# STRUCTURE.md - MVP Project File Organization

## Complete MVP Project Structure

```
claimsiq-platform/
│
├── README.md                        # Quick start guide
├── requirements.txt                 # Python dependencies
├── .env.example                     # Environment template
├── .gitignore                       # Git ignore rules
│
├── backend/                         # Python FastAPI backend
│   ├── __init__.py
│   ├── app.py                       # Main FastAPI app
│   ├── config.py                    # Configuration
│   ├── main.py                      # Entry point
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── claim.py                 # Claim data model
│   │   └── schema.py                # Pydantic validation schemas
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── data_service.py          # Load & cache data
│   │   ├── analytics_service.py     # Risk scoring
│   │   └── claims_service.py        # Claim queries/filtering
│   │
│   └── routes/
│       ├── __init__.py
│       ├── claims.py                # /api/claims endpoints
│       └── analytics.py             # /api/analytics endpoints
│
├── frontend/                        # Reflex frontend
│   ├── claimsiq/
│   │   ├── __init__.py
│   │   ├── config.py                # Frontend config
│   │   ├── state.py                 # Reflex state management
│   │   ├── index.py                 # Homepage
│   │   │
│   │   ├── pages/
│   │   │   ├── __init__.py
│   │   │   └── dashboard.py         # Main dashboard view
│   │   │
│   │   ├── components/
│   │   │   ├── __init__.py
│   │   │   ├── cards.py             # Metric cards
│   │   │   ├── tables.py            # Claims table
│   │   │   ├── charts.py            # Recharts integration
│   │   │   ├── filters.py           # Filter controls
│   │   │   └── navbar.py            # Navigation bar
│   │   │
│   │   └── theme.py                 # Colors & styling
│   │
│   └── rxconfig.py                  # Reflex configuration
│
├── scripts/
│   ├── __init__.py
│   ├── init_db.py                   # Initialize database
│   └── load_sample_data.py          # Load sample CSV
│
├── data/
│   ├── sample/
│   │   └── claims_sample.csv        # Sample data (10K rows)
│   │
│   └── processed/
│       └── claims_cache.pkl         # Cached dataframe
│
├── logs/
│   └── app.log                      # Application logs
│
└── docs/
    └── README.md                    # Documentation index
```

---

## File Organization by Layer

### Frontend Layer (Reflex)

| File | Purpose | Lines |
|------|---------|-------|
| `state.py` | Central state management | 50-100 |
| `index.py` | App root/router | 20-40 |
| `pages/dashboard.py` | Main dashboard page | 100-150 |
| `components/cards.py` | Metric card components | 30-50 |
| `components/tables.py` | Claims table component | 100-150 |
| `components/charts.py` | Chart components | 80-120 |
| `components/filters.py` | Filter controls | 60-100 |
| `components/navbar.py` | Navigation bar | 30-50 |
| `theme.py` | Design tokens | 30-50 |

**Total:** ~500-700 lines of frontend code

---

### Backend Layer (FastAPI)

| File | Purpose | Lines |
|------|---------|-------|
| `app.py` | FastAPI application setup | 40-60 |
| `config.py` | Configuration/env vars | 20-30 |
| `models/schema.py` | Pydantic schemas | 30-50 |
| `models/claim.py` | Claim data model | 30-50 |
| `services/data_service.py` | Data loading/caching | 80-120 |
| `services/claims_service.py` | Claim queries/filters | 80-120 |
| `services/analytics_service.py` | Risk scoring | 60-100 |
| `routes/claims.py` | Claims API endpoints | 40-80 |
| `routes/analytics.py` | Analytics endpoints | 40-80 |

**Total:** ~400-600 lines of backend code

---

### Scripts

| File | Purpose |
|------|---------|
| `init_db.py` | Create database, load schema |
| `load_sample_data.py` | Load Kaggle CSV into DB |

---

### Data

| Location | Purpose |
|----------|---------|
| `data/sample/claims_sample.csv` | Sample 10K-100K claims |
| `data/processed/claims_cache.pkl` | Pickled Pandas DataFrame |

---

## File Descriptions (MVP Only)

### Frontend Files

**`state.py`** - Reflex State Machine
- Manages all UI state (data, filters, loading, errors)
- Methods that handle API calls
- Reactive: changes trigger re-renders
- Keep under 100 lines for MVP

**`pages/dashboard.py`** - Main Dashboard
- Assembles all components
- Calls state methods to load data
- Layout for cards + table + charts
- ~150 lines maximum

**`components/cards.py`** - Metric Cards
- Reusable metric card component
- Takes label, value, color as parameters
- Returns a styled box component
- ~30 lines

**`components/tables.py`** - Claims Table
- Displays list of claims
- Supports sorting by column
- Shows pagination controls
- ~120 lines

**`components/charts.py`** - Charts
- Line chart for trends (Recharts)
- Pie chart for distribution
- Data transformation for chart format
- ~100 lines

**`components/filters.py`** - Filter Controls
- Status dropdown
- Date range picker
- Connected to state.filter_claims()
- ~80 lines

**`components/navbar.py`** - Navigation
- Simple header with logo/title
- Optional: Add refresh button
- ~40 lines

**`theme.py`** - Styling
- Color palette (green, yellow, red)
- Font sizes (sm, md, lg)
- Border radius, padding defaults
- ~50 lines

---

### Backend Files

**`app.py`** - FastAPI Application
```python
from fastapi import FastAPI
from routes import claims, analytics

app = FastAPI()
app.include_router(claims.router, prefix="/api")
app.include_router(analytics.router, prefix="/api")

@app.on_event("startup")
def startup():
    # Load data on app start
    data_service.load_all_data()
```

**`config.py`** - Configuration
```python
import os
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///claimsiq.db")
API_PORT = int(os.getenv("API_PORT", 8000))
DEBUG = os.getenv("DEBUG", "False") == "True"
```

**`models/schema.py`** - Pydantic Schemas
```python
from pydantic import BaseModel

class ClaimResponse(BaseModel):
    id: str
    claim_date: str
    claim_amount: float
    status: str
    risk_score: float
```

**`services/data_service.py`** - Data Loading
```python
import pandas as pd

class DataService:
    _claims_cache = None
    
    @staticmethod
    def load_claims_from_csv(filepath):
        df = pd.read_csv(filepath)
        DataService._claims_cache = df
        return df
    
    @staticmethod
    def get_claims():
        return DataService._claims_cache
```

**`services/claims_service.py`** - Claims Logic
```python
class ClaimsService:
    def get_summary(self):
        claims = data_service.get_claims()
        return {
            "total_claims": len(claims),
            "approved_count": len(claims[claims['status'] == 'approved']),
            ...
        }
    
    def filter_claims(self, status=None, start_date=None, end_date=None):
        claims = data_service.get_claims()
        # Apply filters
        return filtered_claims.to_dict('records')
```

**`services/analytics_service.py`** - Risk Scoring
```python
class AnalyticsService:
    def calculate_risk_score(self, claim):
        score = 0.0
        if claim['amount'] > 5000:
            score += 0.3
        if claim['days_pending'] > 30:
            score += 0.3
        # ... more rules
        return min(score, 1.0)
```

**`routes/claims.py`** - API Routes
```python
from fastapi import APIRouter
from services import claims_service

router = APIRouter()

@router.get("/claims/summary")
def get_summary():
    return claims_service.get_summary()

@router.get("/claims")
def get_claims(status: str = None, limit: int = 100):
    return claims_service.filter_claims(status=status)
```

---

## Naming Conventions (MVP)

### Python Files
- `snake_case_file_names.py`
- Service files end in `_service.py`
- Route files end in `.py` (just the resource name)

### Python Classes
- `PascalCase` for classes (e.g., `DataService`)
- `snake_case` for methods (e.g., `get_claims()`)
- `UPPER_CASE` for constants (e.g., `MAX_CLAIMS = 500000`)

### React Components (via Reflex)
- `PascalCase` for component functions (e.g., `MetricCard()`)
- Stored in `components/` folder

### Files to Git Ignore
```
*.pyc
__pycache__/
.env
*.db
*.log
.web/
node_modules/
venv/
.DS_Store
```

---

## Quick Navigation Guide

**"Where do I add a new API endpoint?"**
→ `backend/routes/` - create or add to existing router

**"Where do I add a new page?"**
→ `frontend/claimsiq/pages/` - create new `.py` file

**"Where do I add a new component?"**
→ `frontend/claimsiq/components/` - create reusable component

**"Where does business logic live?"**
→ `backend/services/` - keep routes thin, logic in services

**"Where do I load the data?"**
→ `scripts/load_sample_data.py` - load CSV here

---

## Folder Size Targets (MVP)

- `backend/` - ~400-600 lines total
- `frontend/` - ~500-700 lines total
- `scripts/` - ~100-150 lines total
- **Total MVP code:** ~1,000-1,500 lines

If any folder exceeds 1,000 lines, break it into smaller pieces.

---

## Creation Order

1. Create `backend/` structure first
2. Create `frontend/` structure
3. Create `scripts/` utilities
4. Create `data/` folders for sample data
5. Create `logs/` for app logs

---

**Version:** 2.0 (MVP Only)
**Last Updated:** 2025-11-03
**Focus:** Simple structure, MVP-only files, no enterprise folders