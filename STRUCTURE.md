# STRUCTURE.md - Production Project File Organization

## Complete Production Project Structure

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
│       ├── analytics.py             # /api/analytics endpoints
│       └── data.py                  # /api/data endpoints (Kaggle, sample, clear)
│
├── claimsiq/                        # Reflex frontend application
│   ├── __init__.py
│   ├── config.py                    # Frontend config
│   ├── state.py                     # Advanced state management (filters, pagination, export)
│   ├── theme.py                     # Design system (colors, shadows, gradients, transitions)
│   │
│   ├── pages/
│   │   ├── __init__.py
│   │   └── dashboard.py             # Main dashboard (charts, tables, modals, toasts)
│   │
│   └── components/
│       ├── __init__.py
│       ├── cards.py                 # Enhanced metric cards (icons, trends, hover effects)
│       ├── charts.py                # Plotly visualizations (area, donut, bar charts)
│       ├── data_management.py       # Data loading UI (Kaggle, sample, clear)
│       ├── tables.py                # Advanced table (search, sort, pagination, badges)
│       ├── filters.py               # Advanced filters panel (date, amount, risk)
│       ├── modals.py                # Claim details modal with actions
│       ├── notifications.py         # Toast notification system
│       ├── navbar.py                # Navigation bar (dark mode, search, user menu)
│       └── ui_helpers.py            # Reusable utilities (empty states, skeletons, headers)
│
├── rxconfig.py                      # Reflex configuration (ports, plugins)
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
    ├── README.md                          # Documentation index
    ├── UI_PHASE1_COMPLETE.md              # Phase 1 features documentation
    ├── UI_PHASE2_COMPLETE.md              # Phase 2 analytics documentation
    ├── UI_PHASE3_COMPLETE.md              # Phase 3 enterprise documentation
    ├── REPLIT_TROUBLESHOOTING.md          # Deployment and debugging guide
    └── SITEMAP_CONFIGURATION.md           # SEO sitemap setup
```

---

## File Organization by Layer

### Frontend Layer (Reflex)

| File | Purpose | Lines |
|------|---------|-------|
| `state.py` | Advanced state management (30+ state vars, computed properties, filters, pagination, export) | 250-350 |
| `pages/dashboard.py` | Main dashboard with charts, tables, modals, toasts | 130 |
| `components/cards.py` | Enhanced metric cards with icons, trends, hover effects | 80-100 |
| `components/charts.py` | Plotly visualizations (area, donut, bar charts) | 180-220 |
| `components/data_management.py` | Data loading panel (Kaggle, sample, clear buttons) | 80-100 |
| `components/tables.py` | Advanced table (search, sort, pagination, badges, export) | 240-260 |
| `components/filters.py` | Advanced filters panel (date, amount, risk) | 120-150 |
| `components/modals.py` | Claim details modal with action buttons | 100-130 |
| `components/notifications.py` | Toast notification system (4 types) | 60-80 |
| `components/navbar.py` | Navigation bar with dark mode, search, user menu | 120-150 |
| `components/ui_helpers.py` | Reusable utilities (empty states, skeletons, sortable headers) | 80-110 |
| `theme.py` | Design system (25+ colors, shadows, gradients, transitions) | 90-120 |

**Total:** ~1,530-1,900 lines of frontend code

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
| `routes/data.py` | Data management endpoints (Kaggle, sample, clear) | 80-100 |

**Total:** ~480-700 lines of backend code

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

## File Descriptions (Production Ready)

### Frontend Files

**`state.py`** - Advanced State Management
- 30+ state variables for comprehensive UI control
- 10+ computed properties for derived data (@rx.var)
- Advanced filtering pipeline (search, date, amount, risk)
- Pagination system (25 items per page)
- Sorting logic (4 sortable columns)
- CSV export functionality
- Modal state management
- Dark mode toggle
- Toast notification state
- ~300 lines

**`pages/dashboard.py`** - Main Dashboard
- Assembles all components (cards, charts, table, modal, toast)
- Grid layout for metric cards (4 columns)
- Analytics section with 3 Plotly charts
- Integrated notification toast system
- Integrated claim details modal
- Calls ClaimsState.load_all_data on mount
- ~130 lines

**`components/cards.py`** - Enhanced Metric Cards
- Icon support (lucide-react icons)
- Trend indicators (+12%, -3%, etc.)
- Trend direction badges (up/down arrows)
- Hover effects (shadow lift, translateY)
- Color-coded by metric type
- Smooth transitions
- ~90 lines

**`components/charts.py`** - Plotly Visualizations
- **Claims Trend Chart**: Area chart with gradient fill, last 6 months
- **Risk Distribution Chart**: Donut chart with low/medium/high segments
- **Status Breakdown Chart**: Bar chart for approved/pending/denied/flagged
- Interactive hover tooltips
- Responsive design
- Color-coded data points
- ~200 lines

**`components/data_management.py`** - Data Loading Panel
- One-click data loading from Kaggle
- One-click synthetic data generation (1,000 claims)
- Clear all data functionality
- Loading states with spinners
- Integration with toast notification system
- Help text with setup instructions
- Color-coded action buttons (blue/green/red)
- No command line required
- ~90 lines

**`components/tables.py`** - Advanced Claims Table
- Real-time search across ID, patient name, status
- Status dropdown filter
- 4 sortable columns (ID, Date, Amount, Risk Score)
- Pagination (25 items per page, previous/next buttons)
- Risk badges with icons (alert-triangle, alert-circle, check-circle)
- Status badges with color schemes
- Clickable rows to open modal
- Export to CSV button
- Advanced filters button
- Empty state for no results
- Loading spinner state
- ~247 lines

**`components/filters.py`** - Advanced Filters Panel
- Date range picker (start/end dates)
- Amount range slider ($0 - $100,000)
- Risk level checkboxes (low/medium/high)
- Apply/Reset action buttons
- Popover-based panel
- Connected to ClaimsState filter methods
- ~140 lines

**`components/modals.py`** - Claim Details Modal
- Dialog-based modal overlay
- Full claim information display
- 2-column grid layout
- Color-coded status badge
- Risk score badge with icon
- Action buttons (Approve/Deny/Flag for Review)
- Close button and backdrop dismiss
- Connected to ClaimsState.selected_claim
- ~120 lines

**`components/notifications.py`** - Toast Notification System
- 4 notification types (success, error, warning, info)
- Fixed position (top-right corner)
- Auto-show on actions
- Manual close button
- Color-coded borders and icons
- Slide-in animation
- ~70 lines

**`components/navbar.py`** - Navigation Bar
- Logo with brand icon
- Navigation links (Dashboard, Claims, Analytics, Providers)
- Search bar input
- Dark mode toggle (moon/sun icon)
- Notification bell icon
- User menu with avatar dropdown
- Sticky positioning
- ~140 lines

**`components/ui_helpers.py`** - Reusable UI Utilities
- **empty_state()**: Friendly "no data" displays with icon, title, description
- **loading_skeleton()**: Skeleton screens for cards and tables
- **sortable_header()**: Table headers with sort indicators
- **centered_spinner()**: Loading spinner with text
- Reduces code duplication
- ~90 lines

**`theme.py`** - Design System
- **COLORS**: 25+ colors (primary, success, warning, danger, grays, backgrounds)
- **SHADOWS**: 5 shadow levels (sm, md, lg, xl, inner)
- **GRADIENTS**: 4 gradient presets (primary, success, warning, danger)
- **TRANSITIONS**: 3 speed levels (fast, normal, slow)
- **FONT_SIZES**: Text size scale
- **SPACING**: Consistent spacing values
- Central design token source
- ~110 lines

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

## Code Size Summary (Production Ready)

- `backend/` - ~480-700 lines total
- `claimsiq/` (frontend) - ~1,530-1,900 lines total
- `scripts/` - ~100-150 lines total
- **Total production code:** ~2,110-2,750 lines

**Enterprise features added (Phases 1-3+):** ~1,435-1,475 lines
- Phase 1 (Foundation): ~325 lines
- Phase 2 (Analytics): ~425 lines
- Phase 3 (Enterprise): ~525 lines
- Phase 3+ (Data Management): ~160-200 lines

---

## Creation Order

1. Create `backend/` structure first
2. Create `frontend/` structure
3. Create `scripts/` utilities
4. Create `data/` folders for sample data
5. Create `logs/` for app logs

---

**Version:** 2.0 (Production Ready - Enterprise Grade)
**Last Updated:** 2025-11-03
**Status:** 🚀 Production-ready with enterprise features (Phases 1-3+ complete, Data Management UI added)
**Components:** 11 frontend components, 3 Plotly charts, advanced state management, design system