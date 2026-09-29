# 📚 Digital Library Management System - STQA Capstone Project
## How to Use Guide

### Quick Start

#### Prerequisites
- Python 3.9 or higher
- pip (Python package manager)
- Modern web browser (Chrome recommended)

#### Installation & Setup

1. **Navigate to the project directory:**
   ```bash
   cd "STQA PROJECT"
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   python app.py
   ```

4. **Open in browser:**
   Navigate to `http://localhost:5000`

### Default Login Credentials

| Role | Username | Password |
|------|----------|----------|
| Librarian/Admin | admin | admin123 |
| Student | student1 | student123 |
| Student | student2 | student123 |

### Application Portals

#### 1. Student Portal
- **Login** with student credentials
- **Browse** the book catalog with search and filters
- **Reserve** available books
- **View** your active borrowings and fines
- **Pay** outstanding fines

#### 2. Librarian/Admin Portal  
- **Login** with admin credentials
- **Manage** the book catalog (add/delete books)
- **Issue** reserved books to students
- **Return** books and auto-calculate fines
- **View** all members and their borrowing history
- **Manage** fines and payments

#### 3. STQA Quality Dashboard
Accessible to all logged-in users via the sidebar:

- **QA Dashboard**: View real-time KPIs, severity breakdown, and test type distribution charts
- **Test Cases**: Browse 25+ comprehensive test cases with filters by module, status, and test type
- **Bug Tracker**: View pre-loaded defects, add new bugs, and update defect status
- **Automation Console**: Run simulated Selenium/Cypress automation suite with visual terminal output

### ➕ Entering New Records (CRUD Support)

You can dynamically add new records across all system modules:

1. **Add New Books (Admin/Librarian)**:
   - Navigate to **Book Catalog** in the sidebar.
   - Click the blue **"+ Add Book"** button in the top toolbar (or click **"Add Book"** in the sidebar).
   - Fill in: Title, Author, 13-digit ISBN (e.g. `9780132350884`), Category, Total Copies, and Shelf Location.
   - Click **Save Book** — the book immediately appears in the catalog and becomes reservable.

2. **Add New Members / Students (Admin/Librarian)**:
   - Navigate to **Members** in the sidebar.
   - Click the green **"+ Add Member"** button in the top right.
   - Enter: Username, Full Name, Email, Password, and Role (`student` or `librarian`).
   - Click **Create Member** — the new member can immediately log in and borrow books.

3. **Add New Test Cases (QA Team / Admin / Student)**:
   - Navigate to **Test Cases** under the STQA Section in the sidebar.
   - Click the purple **"+ Add Test Case"** button.
   - Specify: Test ID (e.g. `TC-NEW-01`), Module, Test Type (EP, BVA, Security, Decision Table, State Transition), Preconditions, Execution Steps, Expected Result, and Status (`Passed`, `Failed`, `Pending`).
   - Click **Save Test Case** — saved to SQLite, immediately updates real-time KPI counts, Pass Rate, and CSV exports.

4. **Report / Add New Defects (QA Team / All Users)**:
   - Navigate to **Bug Tracker** in the sidebar.
   - Click the red **"+ Report Defect"** button.
   - Specify: Defect Title, Module, Severity (`Critical`, `Major`, `Minor`, `Low`), Priority (`High`, `Medium`, `Low`), Steps to Reproduce, Expected Behavior, Actual Behavior, and Assignee.
   - Click **Submit Defect** — logged with a unique Defect ID (`DEF-XXX`), dynamically updates Defect Density and KPI charts. Status can be updated inline anytime.


### Key Features Demonstrated

#### STQA Techniques Covered:
1. **Equivalence Partitioning** - Valid/invalid ISBN formats, login credentials
2. **Boundary Value Analysis** - Book limits (0,1,3,4), fine days (14,15,16)
3. **Decision Table Testing** - Issue approval based on fines and book count
4. **State Transition Testing** - Book lifecycle: Available→Reserved→Issued→Returned
5. **Security Testing** - SQL injection, unauthorized access, account lockout
6. **Automation Testing** - Simulated Selenium WebDriver test execution

#### Business Rules:
- Maximum 3 active books per student
- 14-day borrowing period
- $2/day overdue fine
- Account lockout after 5 failed login attempts (30-minute lockout)
- Students with unpaid fines > $100 cannot borrow

### Running Tests

1. **Start the application** (in one terminal):
   ```bash
   python app.py
   ```

2. **Run pytest** (in another terminal):
   ```bash
   pytest test_automation.py -v
   ```

3. **Run with HTML report** (optional):
   ```bash
   pip install pytest-html
   pytest test_automation.py -v --html=test_report.html
   ```

### Exporting Reports

From the QA Dashboard, click the export buttons:
- **Export Test Cases** → Downloads `test_cases_report.csv`
- **Export Defects** → Downloads `defect_report.csv`  
- **Export Summary** → Downloads `test_execution_summary.csv`

These CSV files can be opened in Excel for the STQA capstone report.

### Academic Report Alignment

This project covers all 10 chapters of the STQA capstone:

| Chapter | Content | Where to Find |
|---------|---------|---------------|
| Ch 1: Introduction | System overview | Dashboard page |
| Ch 2: Objectives | Testing goals | QA Dashboard KPIs |
| Ch 3: System Modules | Auth, Catalog, Issue/Return, Fines | Sidebar navigation |
| Ch 4: Testing Tools | Selenium, PyTest, Chrome | Automation Console |
| Ch 5: Test Cases | 25 test cases | Test Cases page |
| Ch 6: Automation Scripts | PyTest + Simulated Selenium | test_automation.py + Automation tab |
| Ch 7: Defect Reports | 5+ defects with full details | Bug Tracker page |
| Ch 8: Results & Analysis | Pass/Fail rates, defect density | QA Dashboard analytics |
| Ch 9: Deliverables | SRS, Test Plan, Reports | Export CSV buttons |
| Ch 10: Conclusion | Summary metrics | Dashboard summary |

### Troubleshooting

| Problem | Solution |
|---------|----------|
| Port 5000 in use | Change port in app.py: `app.run(port=5001)` |
| Database errors | Delete `library.db` file and restart app |
| Login not working | Check credentials table above |
| CSS not loading | Ensure internet connection (Tailwind CDN) |
| Tests failing | Ensure app is running on localhost:5000 first |

### Project Structure

```
STQA PROJECT/
├── app.py                 # Flask backend (REST API + SQLite)
├── requirements.txt       # Python dependencies
├── test_automation.py     # PyTest automation test suite
├── HOW_TO_USE.md          # This file
├── library.db             # SQLite database (auto-created)
└── templates/
    └── index.html         # Frontend SPA (Tailwind CSS)
```

### License
This project is created for academic purposes as part of the Software Testing & Quality Assurance capstone project.
