# DOCUMENTATION INDEX - ClaimsIQ Complete Reference

This is your master index to all ClaimsIQ documentation. Start here to find what you need.

---

## ðŸ“‹ Quick Navigation

### For Sales Engineers (That's You)
- **Start Here:** [PRESENTATION_PREP.md](#presentationprepmd) - Your demo script and Q&A guide
- **Business Context:** [EXECUTIVE_SUMMARY_AND_PRD.md](#executive-summary-and-prdmd) - Business case and features
- **Product Overview:** [PRODUCT.md](#productmd) - User journeys and value props

### For Developers & AI Agents
- **Start Here:** [README.md](#readmemd) - Project overview and setup
- **Agent Instructions:** [AGENTS.md](#agentsmd) - What to build and how to build it
- **Project Structure:** [STRUCTURE.md](#structuremd) - File organization
- **Architecture:** [TECH.md](#techmd) - Technical decisions

### For Project Managers
- **Planning:** [REQUIREMENTS.md](#requirementsmd) - What needs to be built
- **Timeline:** [EXECUTIVE_SUMMARY_AND_PRD.md](#executive-summary-and-prdmd) - Phase breakdown
- **Tasks:** [AGENTS.md](#agentsmd) - Priority-ordered task list

---

## ðŸ“š Complete Documentation Library

### 1. EXECUTIVE_SUMMARY_AND_PRD.md
**Purpose:** Business justification and product requirements

**Contains:**
- Executive summary and business problem
- Product vision and value propositions
- Quantified ROI (30-40% time savings, $500K-$2M fraud detection)
- Core features and user stories
- Architecture overview
- Statement of Work (3-phase plan)
- Success metrics
- Go-to-market strategy
- Timeline and milestones

**When to Read:**
- Before the pitch (understand the business)
- When presenting to C-suite (have ROI numbers ready)
- When prioritizing features (reference user stories)
- When reporting progress (check against timeline)

**Key Takeaway:** ClaimsIQ saves $1.2-2.5M annually through faster processing, fraud detection, and smart repricing.

---

### 2. README.md
**Purpose:** Project setup and getting started guide

**Contains:**
- Quick start (installation in 5 minutes)
- Project structure overview
- Core features summary
- API endpoint list
- Configuration instructions
- Development workflow
- Data model overview
- Security and privacy summary
- Performance targets
- Deployment options
- Troubleshooting tips
- Roadmap and contributing guidelines

**When to Read:**
- First time setting up the project
- When onboarding new developers
- When deploying to new environment
- When reviewing project status

**Key Takeaway:** This is your one-stop shop for "how do I get this running?"

---

### 3. AGENTS.md
**Purpose:** Instructions for AI coding agents (Claude Code, Codex)

**Contains:**
- Mission and quick reference
- Core principles (shipping > perfection)
- Architecture overview
- Key files and responsibilities
- Implementation tasks (priority-ordered)
- Phase breakdown (Foundation â†’ Intelligence â†’ Polish)
- Reflex-specific guidance
- Common patterns and anti-patterns
- API endpoint contracts
- Testing & QA checklist
- Deployment checklist
- Debugging tips
- Performance targets
- Code review checklist
- Emergency contacts

**When to Read:**
- Before starting development
- When assigning coding tasks to agents
- When stuck on a technical decision
- When reviewing code from agents

**Key Takeaway:** Phase 1 tasks (foundation) must be done first. Everything else depends on them.

---

### 4. STRUCTURE.md
**Purpose:** Project directory organization and file purposes

**Contains:**
- Complete file tree (with descriptions)
- File organization by purpose
- File descriptions and responsibilities
- Creation order (what to build first)
- File size guidelines
- Naming conventions
- Git organization
- Dependencies organization
- Environment variables

**When to Read:**
- When creating a new file (find the right location)
- When looking for a specific feature (find the right file)
- When refactoring code (ensure it's in right place)
- When reviewing pull requests (check file organization)

**Key Takeaway:** Consistent structure = easier to navigate + easier to scale.

---

### 5. TECH.md
**Purpose:** Technical architecture and technology decisions

**Contains:**
- Technology stack overview (Python, Reflex, FastAPI, Pandas, SQLite)
- Architecture diagrams (data flow, component hierarchy)
- Frontend architecture (Reflex component patterns, state management)
- Backend architecture (request flow, service layer structure)
- Data models and schema (claims, policies, providers)
- API endpoint architecture
- Performance optimization strategy
- Security architecture
- Deployment architecture
- Database migration strategy
- Scaling considerations
- Technology decision rationale (why Reflex vs React, etc.)
- Monitoring and observability

**When to Read:**
- Before starting development (understand architecture)
- When making technical decisions (check rationale)
- When optimizing performance (review strategies)
- When planning production deployment
- When defending technology choices

**Key Takeaway:** Reflex â†’ Python; FastAPI â†’ async; SQLite â†’ MVP, PostgreSQL â†’ production.

---

### 6. PRODUCT.md
**Purpose:** Product features, user flows, and value propositions

**Contains:**
- Product vision and value propositions (4 key props)
- Feature set (dashboard, risk intelligence, provider analytics, etc.)
- Feature priority roadmap (MVP â†’ Phase 1 â†’ Phase 2 â†’ Phase 3)
- User journeys (3 detailed flows)
- Data-driven decision support
- Competitive differentiation
- Success metrics (operational, financial, adoption)
- Risk scoring algorithm
- Anomaly detection logic

**When to Read:**
- Before demo (know the features)
- When building UI (understand user flows)
- When setting priorities (reference roadmap)
- When justifying ROI (cite metrics)
- When comparing to competitors

**Key Takeaway:** MVP focuses on dashboard + filtering. Intelligence features (risk detection, clustering) in Phase 1.

---

### 7. REQUIREMENTS.md
**Purpose:** Detailed functional and non-functional requirements

**Contains:**
- Functional requirements (FR1-FR6)
  - Data ingestion
  - Dashboard & visualization
  - Risk detection & analytics
  - Search & discovery
  - Data export
  - User management
- Non-functional requirements (NFR1-NFR7)
  - Performance (page load, API response, queries, charts)
  - Scalability (data volume, concurrent users)
  - Security (encryption, authentication, authorization, audit logging, compliance)
  - Reliability (availability, error handling, data integrity, disaster recovery)
  - Usability (intuitive UI, responsive design, accessibility)
  - Maintainability (code quality, documentation, testing, logging)
  - Operations (containerization, configuration, deployment, monitoring)
- Data requirements (minimum fields for each table)
- Integration requirements (phase by phase)
- Compliance & standards (HIPAA, SOC 2, GDPR)
- Success criteria (MVP, Phase 1, Production)

**When to Read:**
- When planning sprints (reference requirements)
- When testing features (verify acceptance criteria)
- When auditing code (check non-functionals)
- When setting up monitoring (reference performance targets)

**Key Takeaway:** Dashboard <3s, API <500ms, handle 500K claims in MVP.

---

### 8. PRESENTATION_PREP.md â­ **READ THIS FIRST BEFORE DEMO**
**Purpose:** Complete guide for pitching to health insurance client

**Contains:**
- Presentation flow (20 minutes, script included)
- Demo checklist (what to prepare before demo)
- Anticipated questions & answers in 3 categories:
  
  **SECURITY QUESTIONS (Q1.1-Q1.5)**
  - HIPAA compliance
  - Breach response
  - On-premise deployment
  - Data access controls
  - Data residency
  
  **PERFORMANCE QUESTIONS (Q2.1-Q2.4)**
  - System capacity (2M+ claims)
  - Slow networks (satellite internet)
  - Dashboard optimization
  - Backup/recovery SLA
  
  **INTEGRATION QUESTIONS (Q3.1-Q3.5)**
  - Integration methods (CSV â†’ API â†’ Webhooks)
  - Replacing claims system (no, advisory layer)
  - Provider directory integration
  - Auto-approval workflow
  - EHR/billing system connection
  
- Handling tough questions (price, status quo, IT concerns)
- Post-demo conversation starters
- Closing techniques
- One-pagers to leave behind
- Post-demo email template

**When to Read:**
- **Before any demo or pitch** (mandatory)
- When preparing for client questions
- When practicing your pitch
- When preparing follow-up materials
- When closing a deal

**Key Takeaway:** You have answers for every likely question. Practice the flow once before demo.

---

### 9. UI_PHASE1_COMPLETE.md
**Purpose:** Documentation of Phase 1 UI enhancements (Foundation)

**Contains:**
- Enhanced theme system (25+ colors, shadows, gradients, transitions)
- Enhanced metric cards with icons and trend indicators
- Professional navigation bar with links, search, dark mode toggle
- Status and risk badge components
- Visual improvements and hover effects
- Implementation details for foundation features

**When to Read:**
- When understanding the design system
- When working with metric cards or badges
- When modifying the theme
- When reviewing Phase 1 deliverables

**Key Takeaway:** Phase 1 established the design foundation with professional visual polish.

---

### 10. UI_PHASE2_COMPLETE.md
**Purpose:** Documentation of Phase 2 UI enhancements (Analytics)

**Contains:**
- 3 interactive Plotly charts (area, donut, bar)
- Advanced state management (pagination, search, sorting)
- Real-time search functionality
- Pagination system (25 items per page)
- UI helpers (empty states, loading skeletons, sortable headers)
- Enhanced table with search and sort indicators

**When to Read:**
- When working with Plotly visualizations
- When modifying search or sorting logic
- When implementing pagination
- When adding empty states or loading indicators
- When reviewing Phase 2 deliverables

**Key Takeaway:** Phase 2 added interactive analytics with Plotly charts and advanced table features.

---

### 11. UI_PHASE3_COMPLETE.md
**Purpose:** Documentation of Phase 3 UI enhancements (Enterprise)

**Contains:**
- Advanced filters panel (date range, amount range, risk levels)
- Claim details modal with action buttons
- Toast notification system (4 types: success, error, warning, info)
- CSV export functionality with timestamps
- Dark mode implementation
- Enhanced navigation with dark mode toggle
- Enterprise-grade features integration

**When to Read:**
- When working with advanced filters
- When implementing modals or notifications
- When adding CSV export functionality
- When implementing dark mode
- When reviewing Phase 3 deliverables

**Key Takeaway:** Phase 3 completed enterprise features making the platform production-ready.

---

### 12. REPLIT_TROUBLESHOOTING.md
**Purpose:** Guide for debugging and deploying on Replit

**Contains:**
- Common deployment issues and solutions
- Port configuration (3000 frontend, 8001 backend)
- Dependency installation troubleshooting
- Database connection issues
- Reflex-specific debugging tips
- Environment variable setup
- Performance optimization on Replit

**When to Read:**
- When deploying to Replit
- When encountering deployment errors
- When debugging port or connection issues
- When setting up a new Replit environment

**Key Takeaway:** Reference guide for all Replit-specific deployment and troubleshooting needs.

---

### 13. SITEMAP_CONFIGURATION.md
**Purpose:** Guide for SEO sitemap setup in Reflex

**Contains:**
- SitemapPlugin configuration in rxconfig.py
- How sitemap generation works in Reflex
- SEO best practices for the platform
- Sitemap access and verification

**When to Read:**
- When configuring SEO for the application
- When adding SitemapPlugin to Reflex
- When verifying sitemap generation

**Key Takeaway:** SitemapPlugin is built into Reflex core, just add to rxconfig.py plugins list.

---

## ðŸ—ºï¸ By User Role

### Sales Engineers (You)
1. **Must Read:** PRESENTATION_PREP.md (master your pitch)
2. **Should Read:** EXECUTIVE_SUMMARY_AND_PRD.md (business context)
3. **Reference:** PRODUCT.md (feature details)
4. **Reference:** REQUIREMENTS.md (performance targets)

### Backend Developers
1. **Must Read:** AGENTS.md (what to build)
2. **Must Read:** README.md (setup)
3. **Should Read:** TECH.md (architecture)
4. **Should Read:** STRUCTURE.md (file organization)
5. **Reference:** REQUIREMENTS.md (acceptance criteria)

### Frontend Developers
1. **Must Read:** AGENTS.md (what to build)
2. **Must Read:** README.md (setup)
3. **Should Read:** PRODUCT.md (user journeys)
4. **Should Read:** TECH.md (Reflex architecture)
5. **Should Read:** UI_PHASE1_COMPLETE.md, UI_PHASE2_COMPLETE.md, UI_PHASE3_COMPLETE.md (UI features)
6. **Reference:** STRUCTURE.md (component organization)
7. **Reference:** REPLIT_TROUBLESHOOTING.md (deployment)

### Project Managers
1. **Must Read:** EXECUTIVE_SUMMARY_AND_PRD.md (timeline and phases)
2. **Should Read:** AGENTS.md (task breakdown)
3. **Should Read:** REQUIREMENTS.md (acceptance criteria)
4. **Reference:** PRESENTATION_PREP.md (demo timeline)

### QA/Testers
1. **Must Read:** REQUIREMENTS.md (acceptance criteria)
2. **Should Read:** AGENTS.md (testing checklist)
3. **Reference:** PRODUCT.md (user flows to test)

### DevOps/IT
1. **Must Read:** README.md (deployment options)
2. **Must Read:** REPLIT_TROUBLESHOOTING.md (Replit deployment)
3. **Should Read:** TECH.md (architecture)
4. **Reference:** REQUIREMENTS.md (NFR7 - Deployment & Operations)
5. **Reference:** SITEMAP_CONFIGURATION.md (SEO setup)

---

## â±ï¸ By Timeline

### Before Development (Day 0)
1. EXECUTIVE_SUMMARY_AND_PRD.md (understand the why)
2. AGENTS.md (understand the what)
3. STRUCTURE.md (understand the where)

### During Development (Days 1-6)
1. AGENTS.md (reference task priorities)
2. REQUIREMENTS.md (reference acceptance criteria)
3. TECH.md (reference architecture)

### Before Demo (Day 7)
1. PRESENTATION_PREP.md (master your pitch)
2. PRODUCT.md (review features)
3. REQUIREMENTS.md (verify targets)

### Post-Demo (Week 2+)
1. PRODUCT.md (roadmap for phases 2-3)
2. TECH.md (scaling strategies)

---

## ðŸŽ¯ By Question Type

### "What are we building?"
â†’ EXECUTIVE_SUMMARY_AND_PRD.md + PRODUCT.md

### "Why are we building it?"
â†’ EXECUTIVE_SUMMARY_AND_PRD.md (ROI section)

### "How do we build it?"
â†’ TECH.md + STRUCTURE.md + AGENTS.md

### "What do we build first?"
â†’ AGENTS.md (Phase 1 tasks)

### "How do we test it?"
â†’ REQUIREMENTS.md (acceptance criteria)

### "How do we deploy it?"
â†’ README.md + TECH.md

### "How do we demo it?"
â†’ PRESENTATION_PREP.md

### "How do we scale it?"
â†’ TECH.md (scaling section)

### "How do we secure it?"
â†’ PRESENTATION_PREP.md (security Q&A) + TECH.md (security architecture)

---

## ðŸ“Š Documentation Statistics

| Document | Pages | Purpose | Audience |
|----------|-------|---------|----------|
| EXECUTIVE_SUMMARY_AND_PRD.md | 4 | Business case | C-suite, PMs |
| README.md | 5 | Project setup | All developers |
| AGENTS.md | 7 | Coding instructions | AI agents, devs |
| STRUCTURE.md | 6 | File organization | All developers |
| TECH.md | 8 | Architecture | Technical staff |
| PRODUCT.md | 6 | Features & flows | Product, design |
| REQUIREMENTS.md | 8 | Requirements | QA, developers |
| PRESENTATION_PREP.md | 10 | Demo & pitch guide | Sales engineers |
| UI_PHASE1_COMPLETE.md | 3 | Phase 1 UI docs | Frontend devs |
| UI_PHASE2_COMPLETE.md | 4 | Phase 2 Analytics docs | Frontend devs |
| UI_PHASE3_COMPLETE.md | 5 | Phase 3 Enterprise docs | Frontend devs |
| REPLIT_TROUBLESHOOTING.md | 3 | Deployment guide | DevOps, developers |
| SITEMAP_CONFIGURATION.md | 2 | SEO setup | Frontend devs |
| **TOTAL** | **71** | **Complete guide** | **All roles** |

---

## ðŸ”— Cross-References

When you see these patterns, jump to:

- "How do I start coding?" â†' AGENTS.md
- "Where does this file go?" â†' STRUCTURE.md
- "Why did we choose Reflex?" â†' TECH.md
- "What's the user flow?" â†' PRODUCT.md
- "What's the acceptance criteria?" â†' REQUIREMENTS.md
- "What do I say in the demo?" â†' PRESENTATION_PREP.md
- "When is it due?" â†' EXECUTIVE_SUMMARY_AND_PRD.md
- "How do I run it?" â†' README.md
- "How do I work with Plotly charts?" â†' UI_PHASE2_COMPLETE.md
- "How do I implement filters?" â†' UI_PHASE3_COMPLETE.md
- "How do I set up dark mode?" â†' UI_PHASE3_COMPLETE.md
- "What's in the design system?" â†' UI_PHASE1_COMPLETE.md
- "Why won't it deploy on Replit?" â†' REPLIT_TROUBLESHOOTING.md
- "How do I add a sitemap?" â†' SITEMAP_CONFIGURATION.md

---

## ðŸ“ Document Status

| Document | Status | Last Updated | Reviewed |
|----------|--------|--------------|----------|
| EXECUTIVE_SUMMARY_AND_PRD.md | âœ… Final | 2025-11-03 | No |
| README.md | âœ… Final | 2025-11-03 | No |
| AGENTS.md | âœ… Final | 2025-11-03 | No |
| STRUCTURE.md | âœ… Final | 2025-11-03 | No |
| TECH.md | âœ… Final | 2025-11-03 | No |
| PRODUCT.md | âœ… Final | 2025-11-03 | No |
| REQUIREMENTS.md | âœ… Final | 2025-11-03 | No |
| PRESENTATION_PREP.md | âœ… Final | 2025-11-03 | No |
| UI_PHASE1_COMPLETE.md | âœ… Final | 2025-11-03 | No |
| UI_PHASE2_COMPLETE.md | âœ… Final | 2025-11-03 | No |
| UI_PHASE3_COMPLETE.md | âœ… Final | 2025-11-03 | No |
| REPLIT_TROUBLESHOOTING.md | âœ… Final | 2025-11-03 | No |
| SITEMAP_CONFIGURATION.md | âœ… Final | 2025-11-03 | No |

---

## ðŸš€ How to Use This Index

**You're reading this because:**

1. **You're starting the project** â†’ Go to AGENTS.md
2. **You're pitching to client** â†’ Go to PRESENTATION_PREP.md
3. **You're stuck on something** â†’ Use the cross-references above
4. **You're reviewing code** â†’ Go to TECH.md or STRUCTURE.md
5. **You're setting timelines** â†’ Go to EXECUTIVE_SUMMARY_AND_PRD.md

**Keep this document open while working** â€” it's your navigation hub.

---

## ðŸ“ž Getting Help

- **Technical questions?** â†’ Check TECH.md or README.md
- **Business questions?** â†’ Check EXECUTIVE_SUMMARY_AND_PRD.md
- **Demo/pitch questions?** â†’ Check PRESENTATION_PREP.md
- **Still stuck?** â†’ Ask james@sixfold.ai

---

**Version:** 1.0  
**Last Updated:** 2025-11-03  
**Audience:** Everyone working on ClaimsIQ