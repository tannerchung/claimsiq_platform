# ClaimsIQ - MVP Edition

![Status](https://img.shields.io/badge/status-MVP-brightgreen)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![Framework](https://img.shields.io/badge/frontend-Reflex-blue)

ClaimsIQ transforms health insurance claims processing from manual to intelligent. Review claims 30-40% faster and detect fraud patterns in real-time.

## Quick Start (5 minutes)

### Prerequisites
- Python 3.10+
- pip or conda

### Installation

```bash
# Clone the repository
git clone https://github.com/insuretechai/claimsiq-platform.git
cd claimsiq-platform

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env

# Initialize database and load sample data
python scripts/init_db.py
python scripts/load_sample_data.py
```

### Running the Application

```bash
# Terminal 1: Start backend API
python -m uvicorn backend.app:app --reload --port 8000

# Terminal 2: Start frontend
cd frontend
reflex run

# Open browser to http://localhost:3000
```

---

## What's Included (MVP)

✅ **Claims Dashboard** - Real-time metrics and KPIs  
✅ **Claims Table** - Sortable, filterable claims list  
✅ **Risk Scoring** - Automatic high-risk claim detection  
✅ **Charts** - Approval trends and status distribution  
✅ **Provider Analytics** - Basic provider metrics  
✅ **CSV Import** - Load sample data with one command  
✅ **Simple API** - 3 core REST endpoints  

---

## Project Structure

```
claimsiq-platform/
├── backend/                 # FastAPI Python backend
│   ├── app.py              # Main API
│   ├── services/           # Business logic
│   ├── routes/             # API endpoints
│   └── models/             # Data models
├── frontend/               # Reflex React frontend
│   └── claimsiq/
│       ├── pages/          # Dashboard page
│       └── components/     # Reusable components
├── scripts/                # Setup scripts
├── data/                   # Sample data
└── requirements.txt        # Python dependencies
```

See [STRUCTURE.md](04_STRUCTURE.md) for complete file organization.

---

## Core Features

### 1. Dashboard
- Total claims count
- Approval rate (%)
- Pending claims
- Flagged claims
- Loads in <3 seconds

### 2. Claims Table
- Sortable by any column
- Filter by status, date range
- Risk score highlighting (green/yellow/red)
- Paginated (100 rows per page)
- Responsive design

### 3. Risk Intelligence
- Automatic risk scoring (0.0-1.0)
- High-risk claims highlighted in red
- Simple rules: amount, age, provider, procedure
- Top 10 high-risk via API

### 4. Charts
- Line chart: approval trends over time
- Pie chart: claims by status
- Interactive (hover for details)
- Works with 500K claims

### 5. Provider Analytics
- Provider metrics (claims, approval %, avg amount)
- Sortable by any metric
- Flags unusual providers

---

## API Endpoints

```
GET    /api/claims/summary
       → Dashboard metrics (total, approved, pending, flagged)

GET    /api/claims?status=pending&limit=100
       → List claims with optional filtering

GET    /api/analytics/risks
       → High-risk claims analysis
```

Full API docs available at `http://localhost:8000/docs`

---

## Configuration

### Environment Variables (.env)

```bash
# Backend
DATABASE_URL=sqlite:///claimsiq.db
API_PORT=8000
API_HOST=0.0.0.0
DEBUG=False

# Frontend
REFLEX_ENV=dev
API_URL=http://localhost:8000
```

---

## Performance Targets

| Operation | Target |
|-----------|--------|
| Dashboard load | <3 seconds |
| API response | <500ms |
| Table filtering | <500ms |
| Chart rendering | <1 second |
| Data import (500K) | <2 seconds |

---

## Data Model

### Required Fields
- `id` - Unique claim ID
- `claim_date` - Date claimed
- `claim_amount` - Dollar amount
- `status` - pending/approved/denied/flagged
- `provider_id` - Provider ID

### Optional Fields
- `approved_amount` - Amount approved
- `policy_id` - Policy reference
- `procedure_codes` - Medical codes

---

## Deployment

### Local Development
```bash
reflex run  # Starts both frontend and backend
```

### Replit Deployment
```bash
git push replit main
# Deployment automatic, available at: https://claimsiq.replit.dev
```

---

## Security & Privacy

- **Data Encryption:** TLS for connections
- **Database:** SQLite file-based storage
- **HIPAA:** Designed with HIPAA requirements in mind
- **Logging:** Basic file logging

**Note:** This is MVP. Enterprise security features (audit logging, role-based access, advanced encryption) available in Phase 2.

---

## Troubleshooting

### API not connecting
```bash
# Test API
curl http://localhost:8000/api/claims/summary
# Should return JSON
```

### Reflex won't start
```bash
reflex clean
pip install --upgrade reflex
reflex run
```

### Database errors
```bash
# Reinitialize
python scripts/init_db.py
python scripts/load_sample_data.py
```

---

## Development Workflow

### Running Tests (Optional)
```bash
pytest tests/
```

### Code Style
```bash
# Format code
black backend/ frontend/

# Lint
flake8 backend/
```

---

## What's NOT Included (Intentional)

❌ User authentication/login  
❌ Role-based permissions  
❌ Audit logging framework  
❌ Docker containerization  
❌ Advanced error handling  
❌ Monitoring/observability  
❌ Auto-approval workflows  
❌ PDF/CSV exports  
❌ Email integrations  
❌ Mobile app  

These are planned for Phase 2+.

---

## Roadmap

### Phase 1 (Current MVP)
- ✅ Dashboard & analytics
- ✅ Claims filtering & sorting
- ✅ Risk detection
- ✅ Basic API

### Phase 2 (Next)
- 📋 Auto-approval workflows
- 📋 Advanced ML models
- 📋 Email alerts
- 📋 Improved security

### Phase 3 (Future)
- 📋 Multi-tenant support
- 📋 White-label
- 📋 Mobile app

---

## Architecture

See [TECH.md](05_TECH.md) for detailed technical architecture.

**Simple Stack:**
- Frontend: Reflex (Python → React)
- Backend: FastAPI (Python)
- Database: SQLite
- Deployment: Replit

---

## Support

- **Documentation:** See `docs/` directory
- **Issues:** GitHub Issues
- **Questions:** james@sixfold.ai

---

## License

MIT License - See LICENSE file for details

---

**Version:** 1.0 (MVP)  
**Last Updated:** 2025-11-03  
**Status:** 🚀 Ready for Demo