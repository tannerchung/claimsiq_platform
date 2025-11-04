# TECH.md - Technical Architecture (MVP)

## Technology Stack - MVP Only

| Layer | Technology | Version | Why |
|-------|-----------|---------|-----|
| **Frontend** | Reflex | 0.3+ | Python→React, fast dev |
| **Backend** | FastAPI | 0.104+ | Async, auto-docs, fast |
| **Data Processing** | Pandas | 2.1+ | Easy filtering & analysis |
| **Database** | SQLite | 3.44+ | Zero setup, MVP-perfect |
| **Deployment** | Replit | N/A | Simple, shareable link |

**NOT INCLUDED:** PostgreSQL, Redis, Docker, Alembic, Kubernetes, monitoring services

---

## Architecture Diagram (Simple)

```
┌────────────────────────────────────────────────────┐
│           CLIENT BROWSER                           │
│      (Reflex App - Compiled React)                │
└────────────────┬─────────────────────────────────┘
                 │ HTTP/REST
                 ▼
┌────────────────────────────────────────────────────┐
│         FASTAPI BACKEND                            │
│  - Route handlers                                  │
│  - Request validation                              │
│  - Business logic                                  │
└────────────┬──────────────────┬────────────────────┘
             │                  │
             ▼                  ▼
      ┌─────────────┐    ┌──────────────┐
      │  SQLite DB  │    │In-Memory Cache│
      │(claimsiq.db)│    │(Pandas DF)    │
      └─────────────┘    └──────────────┘
             │
             ▼
    ┌────────────────────┐
    │Analytics Engine    │
    │- Risk Scoring      │
    │- Filtering         │
    │- Aggregation       │
    └────────────────────┘
```

---

## Frontend Architecture (Reflex)

### Component Hierarchy

```
App (index.py)
├── Navbar
├── Sidebar (optional for MVP)
└── Main Content
    ├── Dashboard (pages/dashboard.py)
    │   ├── MetricCards (components/cards.py)
    │   ├── ClaimsTable (components/tables.py)
    │   ├── Filters (components/filters.py)
    │   └── Charts (components/charts.py)
    │
    └── (Other pages - optional for MVP)
```

### State Management (Simple)

```python
class State(rx.State):
    # Data from API
    claims_data: list[dict] = []
    summary_stats: dict = {}
    
    # UI state
    is_loading: bool = False
    error_message: str = ""
    selected_status: str = "all"
    
    # Methods trigger re-renders
    async def load_summary(self):
        try:
            # Call API
            ...
        except Exception as e:
            self.error_message = str(e)
```

### Simple Component Pattern

```python
def dashboard() -> rx.Component:
    return rx.box(
        rx.vstack(
            metric_cards_row(),
            claims_table_with_filters(),
            charts_section(),
            spacing="4",
        ),
        padding="6",
    )
```

---

## Backend Architecture (FastAPI)

### Request Flow

```
HTTP Request
    ↓
FastAPI Route Handler
    ↓
Input Validation (Pydantic)
    ↓
Service Layer (Business Logic)
    ├── Query Cache
    ├── Query Database
    └── Calculate Results
    ↓
Output Validation
    ↓
HTTP Response (JSON)
```

### Service Layer Structure

```
backend/services/
├── data_service.py
│   ├── load_claims_from_csv()
│   ├── cache_dataframe()
│   └── get_cached_data()
├── claims_service.py
│   ├── get_claims()
│   ├── filter_claims()
│   └── get_claims_summary()
└── analytics_service.py
    ├── calculate_risk_scores()
    ├── identify_high_risk()
    └── get_risk_distribution()
```

---

## Data Model (Minimal)

### Claims Table

```sql
CREATE TABLE claims (
    id TEXT PRIMARY KEY,
    policy_id TEXT,
    claim_date DATE,
    claim_amount DECIMAL,
    approved_amount DECIMAL,
    status TEXT,           -- pending, approved, denied, flagged
    provider_id TEXT,
    procedure_codes TEXT,  -- JSON array
    created_at TIMESTAMP
);
```

### Policies Table

```sql
CREATE TABLE policies (
    id TEXT PRIMARY KEY,
    plan_type TEXT,        -- HMO, PPO, etc
    premium DECIMAL,
    start_date DATE,
    end_date DATE
);
```

### Providers Table

```sql
CREATE TABLE providers (
    id TEXT PRIMARY KEY,
    npi TEXT,
    name TEXT,
    type TEXT,             -- Hospital, Clinic, etc
    specialty TEXT
);
```

---

## API Endpoints (3 Core)

### GET /api/claims/summary
Returns dashboard metrics
```json
{
  "total_claims": 50000,
  "approved_count": 34000,
  "pending_count": 12000,
  "flagged_count": 4000,
  "approval_rate": 0.68
}
```

### GET /api/claims?status=pending&limit=100&offset=0
Returns paginated claims list
```json
{
  "claims": [...],
  "total": 12000,
  "page": 0,
  "page_size": 100
}
```

### GET /api/analytics/risks
Returns risk analysis
```json
{
  "high_risk_count": 1234,
  "distribution": {"low": 43088, "medium": 5678, "high": 1234},
  "top_risks": [...]
}
```

---

## Performance Optimization (MVP Level)

### Query Optimization
- Index frequently queried columns (status, claim_date)
- Paginate results (show 100 rows, not 50K)
- Eager-load related data

### Frontend Performance
- Pagination: display 100 rows at a time
- Lazy loading: load charts after table
- Client-side filtering where possible
- Memoize expensive computations

### Caching Strategy
- Load full dataset into memory on startup
- Cache as Pandas DataFrame
- Keep in-memory (no Redis)
- Refresh on data import only

---

## Risk Scoring Algorithm (Simple Rules)

```python
def calculate_risk_score(claim):
    score = 0.0
    
    # High amount = higher risk
    if claim['amount'] > 5000:
        score += 0.3
    
    # Pending > 30 days = higher risk
    days_pending = (today - claim['date']).days
    if days_pending > 30:
        score += 0.3
    
    # Unknown provider = higher risk
    if claim['provider_id'] not in known_providers:
        score += 0.2
    
    # Unusual procedure = higher risk
    if claim['procedure_code'] in unusual_codes:
        score += 0.2
    
    return min(score, 1.0)  # Cap at 1.0
```

Then flag as high-risk if score > 0.7

---

## Database Initialization

```python
# scripts/init_db.py
from sqlalchemy import create_engine
import pandas as pd

engine = create_engine('sqlite:///claimsiq.db')

# Load Kaggle CSV
claims_df = pd.read_csv('data/sample/claims_sample.csv')
claims_df.to_sql('claims', engine, if_exists='replace')

# Create indexes
with engine.connect() as conn:
    conn.execute('CREATE INDEX idx_status ON claims(status)')
    conn.execute('CREATE INDEX idx_date ON claims(claim_date)')
```

---

## Deployment Architecture

### Development
```
Local Machine
├── Python venv
├── FastAPI (port 8000)
├── Reflex dev server (port 3000)
├── SQLite database
└── Hot-reload enabled
```

### Production (Replit)
```
Replit Container
├── Single process
├── FastAPI + Reflex compiled
├── SQLite database (same file)
└── Shareable URL
```

---

## Error Handling (Basic)

```python
@app.get("/api/claims")
async def get_claims(status: str = None):
    try:
        if not status:
            claims = all_claims
        else:
            claims = [c for c in all_claims if c['status'] == status]
        return {"claims": claims, "total": len(claims)}
    except Exception as e:
        logger.error(f"Error: {e}")
        return {"error": "Failed to fetch claims"}, 500
```

---

## Logging (Simple)

```python
import logging

logging.basicConfig(
    filename='logs/app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)
logger.info(f"Loaded {len(claims)} claims")
logger.warning(f"Slow query: {duration}ms")
logger.error(f"Database error: {error}")
```

---

## Technology Rationale

### Why Reflex over React?
✅ Single language (Python)  
✅ Faster MVP development  
✅ No context switching  
❌ Smaller ecosystem than React

### Why FastAPI over Django?
✅ Async support  
✅ Auto-generated API docs  
✅ Lightweight  
✅ Great for simple APIs  
❌ Smaller ORM ecosystem

### Why SQLite over PostgreSQL?
✅ Zero setup  
✅ File-based storage  
✅ Perfect for MVP  
✅ No server needed  
❌ Single-user at a time  
❌ Not for production scale

### Why Pandas over SQL?
✅ Flexible transformations  
✅ Easy filtering & analysis  
✅ Built-in statistics  
✅ Familiar to data folks  
❌ Loads data into memory

---

## Scaling Limitations (Acknowledged)

**Current MVP capacity:**
- ~500K claims
- <3 second dashboard load
- <500ms API response
- Single user

**NOT BUILT FOR:**
- Real-time streaming
- 100+ concurrent users
- Multi-tenant isolation
- Disaster recovery
- 24/7 uptime SLA

**Future scaling:** PostgreSQL, Redis, microservices (Phase 2+)

---

**Version:** 2.0 (MVP Only)
**Last Updated:** 2025-11-03
**Focus:** Simple, fast MVP development, no enterprise features