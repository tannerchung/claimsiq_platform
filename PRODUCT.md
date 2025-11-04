# PRODUCT.md - MVP Features & User Flows

## Product Vision (MVP Phase)

**Transform health insurance claims processing from manual to intelligent in 7 days.**

Give claims teams superhuman visibility into their portfolio with instant filtering, risk detection, and visual insights—without slowing operations down.

---

## Core Value Propositions

### 1. **Speed: See All Your Claims Instantly**
- All claims in one place, searchable in <3 seconds
- Filter by status, date, amount, provider
- Find what matters in seconds, not hours

### 2. **Risk: Spot Red Flags Before Paying**
- Automatic risk scoring identifies suspicious claims
- High-risk claims highlighted in red
- Know why each claim is flagged

### 3. **Insight: Understand Your Portfolio at a Glance**
- See approval rates, pending counts, trend lines
- Compare provider performance
- Identify policy profit/loss instantly

### 4. **Simplicity: Works with Your Data Today**
- Upload CSV, get insights immediately
- No setup, no training, no waiting
- Demo-ready in seconds

---

## MVP Feature Set (5 Features)

### Feature 1: Claims Dashboard

**What it shows:**
- Total claims processed this period
- Approval rate (% of claims approved)
- Pending claims (waiting for review)
- Flagged claims (requires action)

**Visual Design:**
- 4 large metric cards, color-coded
- Clear numbers, readable at a glance
- Background colors for easy scanning (green=good, red=warning)

**Why it matters:**
Claims managers need 5-second visibility into portfolio health. This is their operations center.

**User Story:**
> As a claims manager, I want to see my claims summary at a glance so that I can quickly identify bottlenecks and report to leadership.

---

### Feature 2: Claims Intelligence Table

**Columns:**
- Claim ID (clickable)
- Claim Date (YYYY-MM-DD)
- Claim Amount ($)
- Provider Name
- Status (pending, approved, denied, flagged)
- Risk Score (0.0-1.0, color-coded)

**Interactive Capabilities:**
- **Sort:** Click any column header to sort ascending/descending
- **Paginate:** Browse 100 claims per page
- **Filter by status:** Dropdown to show pending/approved/flagged only
- **Filter by date range:** Date picker for custom ranges
- **Search:** Type to find claim IDs

**Why it matters:**
Reviewers need to prioritize their queue. Risk highlighting surfaces what matters first.

**User Story:**
> As a claims processor, I want to filter claims by status and risk level so that I can prioritize high-risk cases first.

**Example:** 
```
Claim ID | Date       | Amount  | Provider        | Status    | Risk Score
CLM-001  | 2024-10-15 | $2,400  | Main Hospital   | Pending   | 0.45 (yellow)
CLM-002  | 2024-10-14 | $45,000 | Unknown Clinic  | Flagged   | 0.92 (red)
CLM-003  | 2024-10-13 | $800    | Clinic A        | Approved  | 0.12 (green)
```

---

### Feature 3: Risk Intelligence

**What it detects:**
- High-risk claims (risk score > 0.7)
- Claims flagged for unusual patterns
- Identification of potential problem areas

**Risk Scoring Rules:**
```
Score increases if:
- Claim amount > $5,000 (+0.3)
- Claim pending > 30 days (+0.3)
- Unknown provider (+0.2)
- Unusual procedure code (+0.2)
Total capped at 1.0
```

**Visualization:**
- Risk score as color-coded number in table (green/yellow/red)
- Hover over score to see reason ("Amount > $5000")
- Top 10 high-risk claims in API response

**Why it matters:**
Fraud and overpayment hide in noise. Simple rules catch obvious red flags.

**User Story:**
> As a fraud investigator, I want to see high-risk claims highlighted so that I can investigate suspicious patterns before paying out.

**Example Usage:**
- Claims over $5,000 are auto-flagged (reasonable alert level)
- Provider claims older than 30 days show wear (payment delays add risk)
- Claims from new providers get extra scrutiny (unknown = riskier)

---

### Feature 4: Provider Analytics (Basic)

**What it shows:**
- Provider name
- Total claims submitted
- Approval rate for that provider
- Average claim amount
- Simple anomaly flag (if unusual)

**Visual:**
- Simple table, sortable by metric
- No complex comparisons (keep MVP)
- Basic color coding (normal vs. unusual)

**Why it matters:**
Underwriters need visibility into provider behavior. Are they outliers?

**User Story:**
> As an underwriter, I want to see provider metrics so that I can identify outliers for repricing conversations.

**Example:**
```
Provider         | Claims | Approval % | Avg Claim | Flag?
Main Hospital    | 500    | 68%        | $2,400    | No
Clinic A         | 300    | 72%        | $1,800    | No
Unknown Provider | 50     | 92%        | $8,000    | Yes (unusual)
```

---

### Feature 5: Charts & Trends

**Chart 1: Approval Rate Over Time**
- Line chart showing approval % by week/month
- Y-axis: 0-100% approval rate
- X-axis: Time (past 3 months)
- Interactive: Hover for exact values

**Chart 2: Status Distribution**
- Pie chart showing: Approved / Pending / Flagged
- Clear color coding (green/yellow/red)
- Shows counts and percentages

**Why it matters:**
Visual trends help spot problems. Declining approval rate = bottleneck.

**User Story:**
> As a manager, I want to see approval trends over time so that I can detect operational problems early.

---

## User Journeys

### Journey 1: Claims Manager Morning Routine

```
1. Open ClaimsIQ dashboard
   ↓
2. See: "50,000 claims | 68% approved | 12,000 pending | 4,000 flagged"
   ↓
3. Click on pie chart to drill down by status
   ↓
4. See approval rate trend (declining last 2 weeks = alert!)
   ↓
5. Filter table to "flagged claims" only
   ↓
6. Sort by "Risk Score" (high to low)
   ↓
7. See top 5 high-risk claims
   ↓
8. Report to leadership: "We have 4,000 flagged claims, up from 3,000 last week"
```

**Time:** ~5 minutes. **Outcome:** Actionable insights from raw data.

---

### Journey 2: Claims Processor Daily Work

```
1. Login to ClaimsIQ
   ↓
2. Filter table: Status = "Pending"
   ↓
3. See 12,000 pending claims
   ↓
4. Sort by Risk Score (high first)
   ↓
5. Click first high-risk claim
   ↓
6. See: Claim ID, Amount ($45K), Risk reason ("Amount > $5000")
   ↓
7. Approve/Deny from dashboard (or route to system)
   ↓
8. Move to next claim
```

**Time:** ~10 seconds per claim. **Outcome:** 5-10x faster review.

---

### Journey 3: Underwriter Repricing Review

```
1. Open ClaimsIQ Provider Analytics
   ↓
2. Sort providers by "Approval %"
   ↓
3. Spot provider with 92% approval on $8K average
   ↓
4. Flag as "unusual - requires review"
   ↓
5. Generate recommendation: "Increase copay from $250 to $350"
   ↓
6. Decision made: Reduce exposure
```

**Time:** ~10 minutes. **Outcome:** Data-driven pricing change saves $100K.

---

## Not Included (Phase 2+)

These features are intentionally NOT in MVP:

❌ Alerts & notifications  
❌ Auto-approval workflows  
❌ PDF/CSV export  
❌ Email integration  
❌ Predictive modeling  
❌ Provider comparison charts  
❌ Policy performance page  
❌ User accounts/login  
❌ Role-based permissions  
❌ Mobile app  

**Pitch strategy:** "We focus on core analytics in MVP. Phase 2 adds automation."

---

## Success Metrics (MVP)

| Metric | Target | How to Measure |
|--------|--------|-----------------|
| Dashboard load time | <3s | Browser stopwatch |
| Table sort/filter | <500ms | User interaction speed |
| Chart render | <1s | Visual timing |
| API response | <500ms | curl timing |
| Risk detection accuracy | >80% precision | Manual spot check |
| Data import | <2s for 500K | Script timer |

---

## Competitive Positioning

**vs. Manual Process:**
- Manual review: 10-15 min per claim = 5,000 hours/year on 500K claims
- ClaimsIQ: 2-3 min per claim = 1,500 hours/year
- **Savings: 3,500 hours = $150K-200K annually**

**vs. Competitors:**
- We go live in **30 days**, not 6 months
- We need **CSV day 1**, no API engineering
- We focus on **speed + risk**, not complexity
- We show **ROI immediately**, not later

---

## Design Principles

### MVP Design is:
- **Simple:** 5 features, not 20
- **Fast:** <3 second loads
- **Visual:** Charts over tables (when helpful)
- **Actionable:** Every number points to action
- **Honest:** Show what works, acknowledge limits

### MVP Design is NOT:
- ❌ Feature-complete
- ❌ Enterprise-grade
- ❌ Highly customizable
- ❌ Multi-tenant
- ❌ Fully automated

---

**Version:** 2.0 (MVP Only)
**Last Updated:** 2025-11-03
**Focus:** 5 core features, simple design, fast delivery