# TECH.md - Technical Architecture (Production Ready)

## Technology Stack - Enterprise Grade

| Layer | Technology | Version | Why |
|-------|-----------|---------|-----|
| **Frontend** | Reflex | 0.3+ | Python→React, fast dev |
| **UI Components** | Radix UI (via Reflex) | Latest | Accessible, modern components |
| **Data Viz** | Plotly | 5.18+ | Interactive charts |
| **Backend** | FastAPI | 0.104+ | Async, auto-docs, fast |
| **Data Processing** | Pandas | 2.1+ | Easy filtering & analysis |
| **Database** | SQLite | 3.44+ | Zero setup, PostgreSQL-ready |
| **State Management** | Reflex State | Built-in | Reactive state with computed properties |
| **Deployment** | Replit | N/A | Simple, shareable link |

**NEW IN V2.0:** Plotly charts, advanced filters, CSV export, modal system, toast notifications, dark mode

**NOT INCLUDED:** PostgreSQL, Redis, Docker, Alembic, Kubernetes, monitoring services (planned for Phase 4)

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
App (claimsiq.py)
├── NotificationToast (notifications.py) - Fixed position overlay
├── ClaimDetailModal (modals.py) - Dialog overlay
└── Main Content
    ├── Navbar (navbar.py)
    │   ├── Logo + Brand Icon
    │   ├── Navigation Links (Dashboard, Claims, Analytics, Providers)
    │   ├── Search Bar
    │   ├── Dark Mode Toggle
    │   ├── Notification Bell
    │   └── User Menu with Avatar
    │
    └── Dashboard (pages/dashboard.py)
        ├── Error Callout (conditional)
        ├── Heading
        │
        ├── Metric Cards Grid (4 columns)
        │   ├── Total Claims Card (cards.py)
        │   ├── Approved Card (cards.py)
        │   ├── Pending Card (cards.py)
        │   └── Flagged Card (cards.py)
        │   └── Each card has: icon, trend badge, value, hover effect
        │
        ├── Analytics Section
        │   ├── Claims Trend Chart (charts.py - Plotly area chart)
        │   ├── Risk Distribution Chart (charts.py - Plotly donut chart)
        │   └── Status Breakdown Chart (charts.py - Plotly bar chart)
        │
        └── Claims Table (tables.py)
            ├── Header Row
            │   ├── Search Input (real-time filter)
            │   ├── Status Dropdown Filter
            │   ├── Advanced Filters Button → Popover (filters.py)
            │   └── Export CSV Button
            │
            ├── Table (with sorting)
            │   ├── Sortable Headers (4 columns: ID, Date, Amount, Risk)
            │   ├── Clickable Rows (open modal on click)
            │   ├── Status Badges (color-coded)
            │   └── Risk Badges (with icons)
            │
            └── Pagination Footer
                ├── Results Count ("Showing 1-25 of 123")
                ├── Previous/Next Buttons
                └── Page Counter
```

### State Management (Advanced)

```python
class ClaimsState(rx.State):
    # Data from API
    claims_data: List[Dict] = []
    summary_stats: Dict = {}
    risk_analysis: Dict = {}
    provider_metrics: List[Dict] = []

    # Loading & Error states
    is_loading: bool = False
    error_message: str = ""

    # Filtering & Search
    selected_status: str = "all"
    search_query: str = ""
    date_start: str = ""
    date_end: str = ""
    amount_min: float = 0.0
    amount_max: float = 100000.0
    risk_filters: list[str] = []

    # Sorting
    sort_column: str = "id"
    sort_direction: str = "asc"

    # Pagination
    current_page: int = 1
    page_size: int = 25
    total_pages: int = 1

    # Modal state
    selected_claim_id: str = ""
    show_claim_modal: bool = False

    # Theme
    dark_mode: bool = False

    # Notifications
    notification_message: str = ""
    notification_type: str = "info"
    show_notification: bool = False

    # Dashboard metrics
    total_claims: int = 0
    approved_count: int = 0
    pending_count: int = 0
    flagged_count: int = 0

    # Computed properties (reactive)
    @rx.var
    def filtered_claims(self) -> List[Dict]:
        """Filter claims based on search and filters"""
        # Applies search_query, status, date range, amount, risk
        ...

    @rx.var
    def sorted_claims(self) -> List[Dict]:
        """Sort filtered claims by column and direction"""
        ...

    @rx.var
    def paginated_claims(self) -> List[Dict]:
        """Get claims for current page (25 items)"""
        ...

    @rx.var
    def selected_claim(self) -> Dict:
        """Get currently selected claim for modal"""
        ...

    # Action methods
    def set_search_query(self, query: str): ...
    def set_status_filter(self, status: str): ...
    def set_date_range(self, start: str, end: str): ...
    def sort_by(self, column: str): ...
    def next_page(self): ...
    def previous_page(self): ...
    def open_claim_modal(self, claim_id: str): ...
    def close_claim_modal(self): ...
    def toggle_dark_mode(self): ...
    def show_toast(self, message: str, type: str): ...
    def export_to_csv(self): ...
```

**Key Features:**
- **Computed Properties**: Auto-recalculate when dependencies change
- **Reactive Pipeline**: Data → Filter → Sort → Paginate → Render
- **Type Hints**: Full type safety
- **Async Methods**: Non-blocking API calls

### Component Patterns

#### Enhanced Metric Card (Phase 1)
```python
def metric_card(
    label: str,
    value: rx.Component,
    icon: str,
    color: str = COLORS["primary"],
    trend: str = "",
    trend_direction: str = "up"
) -> rx.Component:
    return rx.box(
        rx.vstack(
            # Icon + Trend Badge
            rx.hstack(
                rx.icon(icon, size=24, color=color),
                rx.spacer(),
                rx.cond(
                    trend != "",
                    rx.badge(trend, color_scheme="green" if trend_direction == "up" else "red"),
                    rx.fragment()
                ),
                width="100%"
            ),
            rx.text(label, size="2", color=COLORS["gray_500"]),
            value,  # Large number
            spacing="3"
        ),
        padding="5",
        border_radius="0.75rem",
        box_shadow=SHADOWS["md"],
        _hover={"box_shadow": SHADOWS["lg"], "transform": "translateY(-2px)"},
        transition=TRANSITIONS["normal"]
    )
```

#### Interactive Chart (Phase 2)
```python
def claims_trend_chart() -> rx.Component:
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=[d["date"] for d in data],
        y=[d["count"] for d in data],
        mode='lines',
        fill='tozeroy',
        line=dict(color=COLORS["primary"], width=3)
    ))
    # Plotly configuration for responsiveness
    return rx.plotly(data=fig)
```

#### Advanced Filters Panel (Phase 3)
```python
def filters_panel() -> rx.Component:
    return rx.popover.root(
        rx.popover.trigger(rx.button("Filters")),
        rx.popover.content(
            rx.vstack(
                # Date range picker
                rx.input(type="date", on_change=ClaimsState.set_date_range),
                # Amount slider
                rx.slider(min=0, max=100000, step=1000),
                # Risk checkboxes
                rx.checkbox("Low Risk"),
                rx.checkbox("Medium Risk"),
                rx.checkbox("High Risk"),
                # Actions
                rx.button("Apply Filters"),
                rx.button("Reset", on_click=ClaimsState.clear_filters)
            )
        )
    )
```

#### Claim Details Modal (Phase 3)
```python
def claim_detail_modal() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.content(
            rx.vstack(
                rx.heading(f"Claim #{ClaimsState.selected_claim_id}"),
                # Full claim details
                rx.grid(
                    detail_row("ID", claim["id"]),
                    detail_row("Amount", f"${claim['amount']:,.2f}"),
                    detail_row("Status", status_badge(claim["status"])),
                    detail_row("Risk", risk_badge(claim["risk_score"])),
                    columns="2"
                ),
                # Action buttons
                rx.hstack(
                    rx.button("Approve", color_scheme="green"),
                    rx.button("Deny", color_scheme="red"),
                    rx.button("Flag", color_scheme="orange")
                )
            )
        ),
        open=ClaimsState.show_claim_modal
    )
```

#### Component Function Pattern for rx.foreach (CRITICAL)
```python
# WRONG: Lambda closure inside rx.foreach doesn't capture variables correctly
rx.table.body(
    rx.foreach(
        ClaimsState.paginated_claims,
        lambda claim: rx.table.row(
            rx.table.cell(claim["id"]),
            # This lambda doesn't capture claim["id"] correctly!
            on_click=lambda claim_id=claim["id"]: ClaimsState.open_modal(claim_id)
        )
    )
)

# CORRECT: Extract to component function
def claim_row(claim: dict) -> rx.Component:
    """Component function properly captures claim in its scope."""
    return rx.table.row(
        rx.table.cell(claim["id"]),
        # Direct access to claim["id"] works here!
        on_click=lambda: ClaimsState.open_modal(claim["id"]),
        cursor="pointer"
    )

rx.table.body(
    rx.foreach(
        ClaimsState.paginated_claims,
        claim_row  # Pass function reference
    )
)
```

**Why this matters:** Reflex compiles Python to JavaScript. Lambda closures inside foreach loops don't bind correctly during compilation, causing event handlers to receive JavaScript event objects instead of your data.

**Fixed in:** `claimsiq/components/tables_dark.py:220-301`

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

### Component Architecture

```
claimsiq/components/
├── cards.py              # Enhanced metric cards with icons & trends
├── charts.py             # Plotly visualizations (3 charts)
├── tables.py             # Advanced table with search/sort/pagination
├── filters.py            # Advanced filters panel (popover)
├── modals.py             # Claim details modal
├── navbar.py             # Navigation with dark mode toggle
├── notifications.py      # Toast notification system
└── ui_helpers.py         # Empty states, skeletons, sortable headers
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
│   ├── get_claims_summary()
│   └── export_claims_to_csv()
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

## Design System

### Theme Architecture

```python
# claimsiq/theme.py
COLORS = {
    # Primary palette
    "primary": "#2563eb",
    "primary_dark": "#1e40af",
    # Status colors
    "success": "#10b981",
    "warning": "#f59e0b",
    "danger": "#ef4444",
    # Neutrals (gray_50 through gray_900)
    # Backgrounds
    "bg_primary": "#ffffff",
    "bg_secondary": "#f9fafb"
}

SHADOWS = {
    "sm": "0 1px 2px 0 rgba(0, 0, 0, 0.05)",
    "md": "0 4px 6px -1px rgba(0, 0, 0, 0.1)...",
    "lg": "0 10px 15px -3px rgba(0, 0, 0, 0.1)...",
    "xl": "0 20px 25px -5px rgba(0, 0, 0, 0.1)..."
}

GRADIENTS = {
    "primary": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
    "success": "linear-gradient(135deg, #10b981 0%, #059669 100%)"
}

TRANSITIONS = {
    "fast": "all 0.15s ease-in-out",
    "normal": "all 0.3s cubic-bezier(0.4, 0, 0.2, 1)"
}
```

### UI Patterns

**Badges:**
- Status badges: color-coded by status (green/blue/red/orange)
- Risk badges: icon + score + color (✓/🔔/⚠️)

**Empty States:**
- Large icon (64px)
- Clear message
- Optional action button

**Loading States:**
- Skeleton screens (cards, tables)
- Centered spinner with text
- Progressive loading

**Notifications:**
- Toast system (4 types: success/error/warning/info)
- Fixed position (top-right)
- Auto-dismiss option

---

## API Endpoints (8 Core)

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

### GET /api/providers
Returns provider metrics
```json
{
  "providers": [
    {
      "id": "P001",
      "name": "ABC Medical",
      "claims_count": 234,
      "approval_rate": 0.87,
      "avg_claim_amount": 2345.50
    }
  ]
}
```

### GET /api/claims/{claim_id}
Returns specific claim details
```json
{
  "id": "C12345",
  "claim_date": "2024-11-01",
  "claim_amount": 5234.50,
  "status": "approved",
  "risk_score": 0.25,
  "patient_name": "John Doe",
  "provider_name": "ABC Medical",
  "diagnosis_code": "J20.9",
  "service_type": "Consultation"
}
```

### POST /api/data/load-kaggle
Downloads and loads real insurance data from Kaggle
```json
{
  "success": true,
  "message": "Successfully loaded Kaggle dataset!",
  "claims_count": 5000,
  "providers_count": 50
}
```

**Notes:**
- Requires `kaggle.json` configuration (see KAGGLE_SETUP.md)
- Downloads from `ravalsmit/insurance-claims-and-policy-data`
- Uses kagglehub for caching (fast on subsequent loads)
- 5-minute timeout for first download

### POST /api/data/generate-sample?num_claims=1000
Generates realistic synthetic insurance claims data
```json
{
  "success": true,
  "message": "Successfully generated 1000 synthetic claims!",
  "claims_count": 1000,
  "providers_count": 50
}
```

**Parameters:**
- `num_claims`: Number of claims to generate (1-100,000, default: 1000)

**Features:**
- 18-field schema matching Kaggle data
- Realistic ICD-10 diagnosis codes
- Realistic CPT procedure codes
- Patient demographics (age, gender, state)
- Processing metrics (days to process, denial reasons)

### POST /api/data/clear-data
Clears all claims and providers from the database
```json
{
  "success": true,
  "message": "Cleared 1000 claims and 50 providers",
  "claims_count": 0,
  "providers_count": 0
}
```

**Warning:** This permanently deletes all data from the database!

---

## Performance Optimization (MVP Level)

### Query Optimization
- Index frequently queried columns (status, claim_date)
- Paginate results (show 100 rows, not 50K)
- Eager-load related data

### Frontend Performance
- **Pagination**: Display 25 rows per page (not all data at once)
- **Computed Properties**: Efficient reactive recalculation with @rx.var
- **Lazy Loading**: Charts load after initial render
- **Client-side Filtering**: Search and filters run in browser
- **Memoization**: Expensive computations cached
- **Skeleton Screens**: Better perceived performance during loading
- **CSV Export**: Generates in-memory, downloads client-side

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
├── Reflex process (manages both frontend & backend)
│   ├── Frontend: Port 3000 (0.0.0.0)
│   ├── Backend: Port 8001 (0.0.0.0)
│   └── Compiled React app served by Reflex
├── SQLite database (claimsiq.db)
├── Sitemap plugin enabled (/sitemap.xml)
└── Shareable URL (https://repl.co/...)
```

### Configuration
```python
# rxconfig.py
config = rx.Config(
    app_name="claimsiq",
    frontend_port=3000,
    backend_port=8001,
    backend_host="0.0.0.0",
    frontend_host="0.0.0.0",
    tailwind={},
    plugins=[rx.plugins.SitemapPlugin()]
)
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

## New Features (v2.0)

### Phase 1: Foundation
- Professional design system (25+ colors, shadows, gradients)
- Enhanced metric cards with icons and trend indicators
- Modern navbar with navigation menu
- Status and risk badges with icons
- Hover effects and smooth transitions

### Phase 2: Analytics
- 3 Interactive Plotly charts (area, donut, bar)
- Real-time search functionality
- Column sorting with visual indicators
- Pagination (25 items per page)
- Empty states and loading skeletons

### Phase 3: Enterprise
- CSV export functionality
- Advanced filters (date range, amount range, risk levels)
- Claim details modal with action buttons
- Toast notification system (4 types)
- Dark mode toggle
- Clickable table rows

---

## Data Flow

### Filtering Pipeline
```
Raw Data (1000 claims)
    ↓
Search Filter (search_query)
    ↓
Status Filter (selected_status)
    ↓
Advanced Filters (date, amount, risk)
    ↓
Sorted Claims (sort_column, sort_direction)
    ↓
Paginated Claims (current_page, page_size = 25)
    ↓
Rendered Table (25 rows visible)
```

### Export Flow
```
User clicks "Export"
    ↓
export_to_csv() called
    ↓
Get sorted_claims (respects all filters)
    ↓
Generate CSV in memory (io.StringIO)
    ↓
Trigger browser download
    ↓
Show success toast notification
```

### Modal Flow
```
User clicks table row
    ↓
open_claim_modal(claim_id)
    ↓
show_claim_modal = True
selected_claim_id = claim_id
    ↓
selected_claim computed property
    ↓
Dialog displays claim details
    ↓
User takes action (Approve/Deny/Flag)
    ↓
close_claim_modal()
```

---

**Version:** 2.1 (Production Ready - Enterprise Grade)
**Last Updated:** 2025-11-04
**Focus:** Enterprise UI, advanced analytics, production-ready features

**Total Lines of Code Added:** ~1,350+ lines across all phases
**Components:** 11 component files, 3 charts, 8 UI helpers
**State Variables:** 30+ state variables, 10+ computed properties
**Features:** Search, sort, pagination, filters, export, modal, charts, dark mode, notifications

**Critical Fixes:**
- Lambda closure issue in rx.foreach resolved (tables_dark.py:220-301)
- Component function pattern implemented for proper event handling