# STQA-

# 📚 Digital Library Management System — STQA Capstone Project

## ✅ Build Complete & Verified

All code is **fully functional, tested, and ready to run**.

---

## Project Structure

```
STQA PROJECT/
├── app.py                 # Flask backend — 700 lines (REST API + SQLite)
├── requirements.txt       # Python dependencies
├── test_automation.py     # PyTest automation suite — 354 lines
├── HOW_TO_USE.md          # Complete usage documentation
├── library.db             # SQLite database (auto-created on first run)
└── templates/
    └── index.html         # Frontend SPA — 1,286 lines (Tailwind CSS)
```

**Total: 2,492 lines of production code across 5 files.**

---

## Quick Start

```bash
cd "STQA PROJECT"
pip install -r requirements.txt
python app.py
# Open http://localhost:5000
```

### Default Credentials

| Role | Username | Password |
|------|----------|----------|
| 🔑 Librarian/Admin | `admin` | `admin123` |
| 🎓 Student | `student1` | `student123` |
| 🎓 Student | `student2` | `student123` |

---

## Three Integrated Portals

### 1. Student Portal
- Book catalog with search (by title, author, ISBN, category)
- Reserve available books
- View borrowings and fines
- Pay outstanding fines

### 2. Librarian/Admin Portal
- Full book catalog management (CRUD)
- Issue reserved books to students (max 3 per student)
- Process returns with auto fine calculation ($2/day overdue)
- Member management with fine overview

### 3. STQA Quality Dashboard
- **QA Analytics** — Real-time KPIs with severity & test-type breakdowns
- **Test Cases** — 25 test cases with filter/search capabilities
- **Bug Tracker** — 5 pre-loaded defects + "Add New Defect" form
- **Automation Console** — Simulated Selenium WebDriver execution

---

## Verification Results

### API Smoke Tests — ✅ All Passed

| # | Test | Result |
|---|------|--------|
| 1 | Session check (unauthenticated) | ✅ `{logged_in: false}` |
| 2 | Admin login | ✅ `Login successful` |
| 3 | Book catalog | ✅ 12 books loaded |
| 4 | Test cases endpoint | ✅ 25 test cases |
| 5 | Defects endpoint | ✅ 5 defects loaded |
| 6 | Dashboard stats | ✅ Passed=22, Failed=3 |
| 7 | Automation runner | ✅ 4 test groups |
| 8 | CSV export | ✅ `text/csv` response |
| 9 | Logout | ✅ Session cleared |
| 10 | Student login | ✅ `Login successful` |
| 11 | Book reservation | ✅ `Book reserved` |

### Dashboard Statistics

```json
{
  "total_test_cases": 25,
  "passed": 22,
  "failed": 3,
  "total_defects": 5,
  "resolved_defects": 2,
  "open_defects": 3,
  "severity_breakdown": {
    "Critical": 1,
    "High": 2,
    "Medium": 2
  },
  "test_type_distribution": {
    "Boundary": 9,
    "Decision Table": 1,
    "Equivalence Partitioning": 2,
    "Functional": 7,
    "Security": 3,
    "State Transition": 3
  }
}
```

---

## STQA Techniques Coverage

| Technique | Test Cases | Examples |
|-----------|-----------|----------|
| **Equivalence Partitioning** | 2 | Valid/invalid ISBN, negative fine days |
| **Boundary Value Analysis** | 9 | Book limit (0,1,3,4), fine days (14,15,16) |
| **Decision Table** | 1 | Fine threshold + availability → issue decision |
| **State Transition** | 3 | Available→Reserved→Issued→Returned lifecycle |
| **Security Testing** | 3 | SQL injection, account lockout, auth bypass |
| **Functional Testing** | 7 | Login, registration, search, issue workflows |

## Pre-Loaded Defects

| Bug ID | Module | Severity | Priority | Status |
|--------|--------|----------|----------|--------|
| BUG01 | Fine Calculation | 🔴 Critical | P1 | Open |
| BUG02 | Security | 🟠 High | P1 | In Progress |
| BUG03 | Book Search | 🟡 Medium | P2 | Closed |
| BUG04 | Book Issue | 🟠 High | P2 | Open |
| BUG05 | Authentication | 🟡 Medium | P3 | Closed |

## Academic Report Alignment (10 Chapters)

| Chapter | Content | Location |
|---------|---------|----------|
| Ch 1 | Introduction & Scope | Dashboard overview |
| Ch 2 | Project Objectives | QA Dashboard KPIs |
| Ch 3 | System Modules | Sidebar navigation (6 modules) |
| Ch 4 | Testing Tools | Automation Console (Selenium, PyTest) |
| Ch 5 | Test Cases Table | Test Cases page (25 cases) |
| Ch 6 | Automation Scripts | [test_automation.py](file:///Users/gaurang/Documents/STQA%20PROJECT/test_automation.py) + Automation tab |
| Ch 7 | Defect Reports | Bug Tracker page (5+ defects) |
| Ch 8 | Results & Analysis | Dashboard analytics charts |
| Ch 9 | Deliverables Checksheet | Export CSV buttons |
| Ch 10 | Conclusion | Summary metrics |

---

## Running Automated Tests

```bash
# Terminal 1: Start the app
python app.py

# Terminal 2: Run PyTest suite
pytest test_automation.py -v
```

## Exporting Reports

Use the **QA Dashboard** export buttons in the UI, or direct API calls:
- `GET /api/export/test-cases` → `test_cases_report.csv`
- `GET /api/export/defects` → `defect_report.csv`
- `GET /api/export/summary` → `test_execution_summary.csv`
