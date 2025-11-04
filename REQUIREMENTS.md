# REQUIREMENTS.md - MVP Acceptance Criteria

## Functional Requirements (MVP)

### FR1: Data Ingestion
**Requirement:** System loads insurance claims data
- Load CSV file with at least 50K claims
- Parse required fields: id, date, amount, status, provider
- Handle missing/invalid data gracefully
- Cache data in memory for fast access

**Acceptance Criteria:**
- CSV imports without errors
- Data is queryable within 2 seconds
- Can handle up to 500K records
- Invalid rows are logged, not fatal

---

### FR2: Claims Dashboard
**Requirement:** Display real-time claims summary
- Show total claims count
- Show approval rate (%)
- Show pending claims count
- Show flagged claims count

**Acceptance Criteria:**
- Dashboard loads in <3 seconds
- All 4 metrics are accurate
- Metrics update when data changes
- Mobile-responsive layout

---

### FR3: Claims Table & Filtering
**Requirement:** List and filter claims
- Display claims in sortable table
- Filter by status (pending, approved, denied, flagged)
- Filter by date range
- Paginate results (100 rows per page)

**Acceptance Criteria:**
- Table displays first 100 claims
- Sort works on all columns
- Filters update table <500ms
- Can navigate between pages

---

### FR4: Risk Intelligence
**Requirement:** Identify high-risk claims
- Calculate risk score for each claim (0.0-1.0)
- Highlight claims with risk > 0.7
- Show risk reason on hover
- API returns top 10 high-risk claims

**Acceptance Criteria:**
- Risk scoring is rule-based (not ML)
- High-risk claims show in red
- Hover shows risk reason
- API response <500ms

---

### FR5: Charts & Visualization
**Requirement:** Visualize claims data
- Line chart: approval trends over time
- Pie chart: status distribution (approved/pending/flagged)
- Charts are interactive (hover for details)
- Charts render smoothly with 500K records

**Acceptance Criteria:**
- Charts render without lag
- Hover shows data point values
- Charts update when data changes
- Works with 500K+ claims

---

### FR6: API Integration
**Requirement:** Provide HTTP API for external access
- GET /api/claims/summary
- GET /api/claims (with filters)
- GET /api/analytics/risks
- All endpoints return valid JSON

**Acceptance Criteria:**
- All 3 endpoints accessible
- Responses match schema
- All endpoints <500ms (p95)
- CORS enabled for local testing

---

## Non-Functional Requirements (MVP)

### NFR1: Performance

#### 1.1 Dashboard Load Time
**Target:** <3 seconds
**Measurement:** Time from page load to content visible
**Implementation:** Pagination, lazy loading charts

#### 1.2 API Response Time
**Target:** <500ms (p95)
**Measurement:** Time from request to response
**Implementation:** Database indexing, simple queries

#### 1.3 Data Ingestion
**Target:** <2 seconds for 500K records
**Measurement:** Time from CSV upload to data queryable
**Implementation:** Bulk insert, in-memory caching

#### 1.4 Chart Rendering
**Target:** <1 second
**Measurement:** Time from data load to chart visible
**Implementation:** Limit data points, client-side rendering

---

### NFR2: Scalability

#### 2.1 Claims Volume
**Target:** Handle 500K claims
**Implementation:** SQLite can handle this size
**Limitation:** Beyond 1M, upgrade to PostgreSQL

#### 2.2 Concurrent Users
**Target:** 1 user (no multi-user concurrency for MVP)
**Note:** Replit is single-process

#### 2.3 Data Size
**Target:** Up to 10GB
**Note:** SQLite limit is fine for MVP scope

---

### NFR3: Reliability

#### 3.1 Error Handling
**Requirement:** Handle errors gracefully
- Invalid CSV format → show error message
- Missing required fields → skip row, log warning
- Database query fails → return 500 error with message
- API timeout → return 504 with retry advice

**Acceptance Criteria:**
- No unhandled exceptions
- User-friendly error messages
- Errors logged to file

#### 3.2 Data Integrity
**Requirement:** Data remains consistent
- No data loss on page refresh
- Filtering doesn't corrupt data
- Multiple filters compose correctly

**Acceptance Criteria:**
- Refresh doesn't lose data
- Multiple filters work together
- Undo is not required

---

### NFR4: Usability

#### 4.1 Intuitive Interface
**Requirement:** New user can navigate without training
- Clear dashboard layout
- Obvious navigation
- Consistent styling
- Helpful labels

**Acceptance Criteria:**
- Navigation clear without help text
- Filters are obvious
- Chart legend is readable
- Error messages are helpful

#### 4.2 Responsive Design
**Requirement:** Works on all screen sizes
- Desktop (1920x1080)
- Laptop (1366x768)
- Tablet (768x1024)

**Acceptance Criteria:**
- Layout works on all sizes
- Touch-friendly buttons
- Readable text on mobile

#### 4.3 Accessibility (Basic)
**Requirement:** Basic accessibility support
- Keyboard navigation works
- Color not only indicator (use icons/text)
- Alt text on images

**Acceptance Criteria:**
- Can navigate with Tab key
- Red highlights have icons too
- No purely color-coded info

---

### NFR5: Deployability

#### 5.1 Quick Start
**Requirement:** Setup in <5 minutes
- Git clone
- pip install
- Run command
- App loads

**Acceptance Criteria:**
- README is accurate
- No missing dependencies
- No configuration needed
- Works on Windows/Mac/Linux

#### 5.2 Replit Deployment
**Requirement:** Deploy to Replit with one click
- Push code to Replit
- Automatic build & deploy
- Shareable URL
- Works from URL

**Acceptance Criteria:**
- Replit link works
- No console errors in logs
- Can import new CSV
- Link is shareable

---

## Success Criteria

### MVP Success = All of These
- ✅ Dashboard loads <3 seconds
- ✅ Can filter and sort claims
- ✅ Risk highlighting works
- ✅ Charts display correctly
- ✅ All 3 API endpoints work
- ✅ Deployable to Replit
- ✅ Works with 500K claims
- ✅ No critical errors

### NOT Required for MVP
- ❌ Multi-user login
- ❌ Role-based permissions
- ❌ TLS/security features
- ❌ Disaster recovery
- ❌ Audit logging
- ❌ Mobile app
- ❌ Email notifications
- ❌ Auto-approval workflows
- ❌ Advanced ML models

---

## Test Scenarios

### Scenario 1: First-Time User
1. Load app → Dashboard appears
2. See 4 metrics and claims table
3. Click "filter by status" → options appear
4. Select "pending" → table updates
5. Click chart → see tooltip

**Expected:** All steps work smoothly

### Scenario 2: Large Dataset
1. Import 500K claims CSV
2. Dashboard loads
3. Filter to show 10K pending claims
4. Sort by amount
5. Scroll through pages

**Expected:** No lag, responsive UI

### Scenario 3: Edge Cases
1. Upload empty CSV → Error message shown
2. Filter with no results → "No claims" message
3. Invalid date range → Shows validation error
4. API returns slow response → Spinner shows

**Expected:** Graceful handling

---

## Performance Benchmarks

| Operation | Target | Method to Test |
|-----------|--------|-----------------|
| Page load | <3s | Browser dev tools |
| API response | <500ms | curl + time command |
| Data import | <2s for 500K | Script timer |
| Chart render | <1s | Browser perf tools |
| Sorting 100 rows | <100ms | Browser console |
| Filtering | <500ms | User interaction test |

---

## Data Requirements

### Required Fields (Every Claim)
- `id` - Unique claim ID
- `claim_date` - Date claimed
- `claim_amount` - Dollar amount
- `status` - pending/approved/denied/flagged
- `provider_id` - Provider identifier

### Optional Fields (Enhance Features)
- `approved_amount` - Amount actually approved
- `policy_id` - Policy reference
- `procedure_codes` - Medical codes
- `diagnosis_codes` - Diagnosis codes

---

## Definition of Done (For Each Feature)

A feature is "done" when:
- ✅ Code is written
- ✅ Tests pass (manual testing OK)
- ✅ Acceptance criteria met
- ✅ Performance targets met
- ✅ No console errors
- ✅ Documented in README
- ✅ Works on Replit

---

**Version:** 2.0 (MVP Only)
**Last Updated:** 2025-11-03
**Focus:** 5 core requirements, performance targets, no enterprise features