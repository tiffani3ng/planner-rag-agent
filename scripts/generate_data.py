#!/usr/bin/env python3
"""
Generate synthetic data for the Planner RAG Agent.

Creates:
  data/syllabi/  - 4 PDF syllabi
  data/calendars/ - 2 ICS calendar files (class schedule + deadlines)

Run from the project root:
  python scripts/generate_data.py
"""

from pathlib import Path
from fpdf import FPDF

# ?? Output directories ?????????????????????????????????????????????????????????

ROOT = Path(__file__).parent.parent
SYLLABI_DIR = ROOT / "data" / "syllabi"
CAL_DIR = ROOT / "data" / "calendars"

SYLLABI_DIR.mkdir(parents=True, exist_ok=True)
CAL_DIR.mkdir(parents=True, exist_ok=True)


# ??????????????????????????????????????????????????????????????????????????????
#  PDF helpers
# ??????????????????????????????????????????????????????????????????????????????

class SyllabusPDF(FPDF):
    def __init__(self, course_title: str, course_code: str):
        super().__init__()
        self.course_title = course_title
        self.course_code = course_code
        self.set_auto_page_break(auto=True, margin=20)
        self.set_margins(20, 20, 20)

    def header(self):
        self.set_font("Helvetica", "B", 14)
        self.set_fill_color(30, 60, 120)
        self.set_text_color(255, 255, 255)
        self.cell(0, 12, f"{self.course_code}  -  {self.course_title}", fill=True, new_x="LMARGIN", new_y="NEXT", align="C")
        self.set_text_color(0, 0, 0)
        self.ln(4)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(120, 120, 120)
        self.cell(0, 10, f"Page {self.page_no()} | Fall 2026 Syllabus", align="C")
        self.set_text_color(0, 0, 0)

    def section(self, title: str):
        self.ln(4)
        self.set_font("Helvetica", "B", 12)
        self.set_fill_color(220, 230, 242)
        self.cell(0, 8, title, fill=True, new_x="LMARGIN", new_y="NEXT")
        self.ln(2)

    def body(self, text: str):
        self.set_font("Helvetica", "", 10)
        self.multi_cell(0, 6, text)
        self.ln(2)

    def assignment_row(self, label: str, due: str, weight: str, description: str):
        self.set_font("Helvetica", "B", 10)
        self.cell(0, 6, f"{label}  -  Due: {due}  ({weight})", new_x="LMARGIN", new_y="NEXT")
        self.set_font("Helvetica", "", 10)
        self.multi_cell(0, 6, description)
        self.ln(2)


def make_pdf(course_code, course_title, professor, office_hours, description,
             objectives, materials, assignments, schedule_notes, grading,
             filename):
    pdf = SyllabusPDF(course_title, course_code)
    pdf.add_page()

    # Course info block
    pdf.set_font("Helvetica", "", 10)
    info_lines = [
        f"Professor: {professor}",
        f"Office Hours: {office_hours}",
        "Term: Fall 2026  |  Credits: 3",
        "Location: See schedule below",
    ]
    for line in info_lines:
        pdf.cell(0, 6, line, new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)

    # Description
    pdf.section("Course Description")
    pdf.body(description)

    # Objectives
    pdf.section("Learning Objectives")
    pdf.body(objectives)

    # Materials
    pdf.section("Required Materials")
    pdf.body(materials)

    # Assignments
    pdf.section("Assignments & Due Dates")
    for a in assignments:
        pdf.assignment_row(a["label"], a["due"], a["weight"], a["desc"])

    # Schedule notes
    pdf.section("Course Schedule Notes")
    pdf.body(schedule_notes)

    # Grading
    pdf.section("Grading Policy")
    pdf.body(grading)

    out_path = SYLLABI_DIR / filename
    pdf.output(str(out_path))
    print(f"  Created: {out_path.relative_to(ROOT)}")


# ??????????????????????????????????????????????????????????????????????????????
#  Syllabus 1 - Applied Linear Algebra (MATH 301)
# ??????????????????????????????????????????????????????????????????????????????

def gen_math301():
    make_pdf(
        course_code="MATH 301",
        course_title="Applied Linear Algebra",
        professor="Dr. Sarah Chen  |  schen@university.edu  |  Science Hall 412",
        office_hours="Mon & Wed 11:00 AM - 12:30 PM, or by appointment",
        description=(
            "This course provides a rigorous yet applied treatment of linear algebra, "
            "covering vector spaces, matrix theory, and linear transformations with an "
            "emphasis on computational applications. Students will implement algorithms in "
            "Python (NumPy/SciPy) and apply linear algebra to problems in data science, "
            "graphics, and optimization. Topics include Gaussian elimination, LU and QR "
            "factorization, eigenvalue decomposition, the Singular Value Decomposition (SVD), "
            "and Principal Component Analysis (PCA). The course meets Monday, Wednesday, and "
            "Friday from 10:00-10:50 AM in Science Hall 201."
        ),
        objectives=(
            "By the end of the course, students will be able to:\n"
            "1. Solve systems of linear equations using direct and iterative methods.\n"
            "2. Compute and interpret eigenvalues and eigenvectors.\n"
            "3. Apply the SVD to dimensionality reduction and least-squares problems.\n"
            "4. Implement matrix algorithms in Python with NumPy.\n"
            "5. Analyze the numerical stability of linear algebra computations."
        ),
        materials=(
            "Textbook: 'Introduction to Linear Algebra' by Gilbert Strang, 5th ed. (MIT Press).\n"
            "Software: Python 3.11+ with NumPy, SciPy, Matplotlib (Anaconda distribution recommended).\n"
            "A scientific calculator is required for exams."
        ),
        assignments=[
            {
                "label": "Homework 1 - Vectors, Matrices, and Linear Systems",
                "due": "September 18, 2026",
                "weight": "10%",
                "desc": (
                    "Problems 1-30 from Chapter 1 & 2. Topics: vector operations, "
                    "matrix multiplication, Gaussian elimination, and row echelon form. "
                    "Submit a PDF of hand-written or typed solutions on Gradescope by 11:59 PM."
                ),
            },
            {
                "label": "Homework 2 - Linear Independence, Bases, and Rank",
                "due": "October 2, 2026",
                "weight": "10%",
                "desc": (
                    "Problems from Chapters 3 & 4. Topics: null space, column space, "
                    "four fundamental subspaces, rank-nullity theorem. Submit on Gradescope."
                ),
            },
            {
                "label": "Midterm Exam",
                "due": "October 16, 2026",
                "weight": "20%",
                "desc": (
                    "In-class exam covering Chapters 1-4: linear systems, matrix factorizations, "
                    "subspaces, and orthogonality. Closed-book; one 3x5 index card of notes allowed. "
                    "Held during regular class time in Science Hall 201."
                ),
            },
            {
                "label": "Homework 3 - Eigenvalues and Eigenvectors",
                "due": "October 30, 2026",
                "weight": "10%",
                "desc": (
                    "Problems from Chapter 5. Topics: characteristic polynomial, diagonalization, "
                    "symmetric matrices, and the spectral theorem. Python portion: compute eigenvalues "
                    "of a 5x5 matrix using both NumPy and the power iteration method."
                ),
            },
            {
                "label": "Homework 4 - SVD and Least Squares",
                "due": "November 13, 2026",
                "weight": "10%",
                "desc": (
                    "Problems from Chapters 6 & 7. Topics: Singular Value Decomposition, "
                    "pseudoinverse, least-squares regression, and low-rank approximation. "
                    "Python coding problems included."
                ),
            },
            {
                "label": "Computational Project - PCA on Real Data",
                "due": "December 4, 2026",
                "weight": "20%",
                "desc": (
                    "Apply PCA to a dataset of your choosing (minimum 500 samples, 10+ features). "
                    "Submit a Jupyter notebook (.ipynb) and a 4-page report covering: data preprocessing, "
                    "explained variance analysis, 2D/3D visualisation, and interpretation. "
                    "Groups of 1-2 students. Submit via course portal by 11:59 PM."
                ),
            },
            {
                "label": "Homework 5 - Linear Transformations and Change of Basis",
                "due": "November 21, 2026",
                "weight": "10%",
                "desc": (
                    "Problems from Chapter 8. Topics: linear maps between vector spaces, "
                    "matrix representations, similar matrices, and Jordan normal form (intro)."
                ),
            },
            {
                "label": "Final Exam",
                "due": "December 15, 2026",
                "weight": "20%",
                "desc": (
                    "Comprehensive final covering all course material. 2-hour exam held "
                    "in the registrar-assigned room. One 8.5x11 sheet of notes (both sides) allowed. "
                    "Bring a scientific calculator."
                ),
            },
        ],
        schedule_notes=(
            "Week 1  (Sep 8-12):   Vectors, dot products, matrix basics\n"
            "Week 2  (Sep 15-19):  Gaussian elimination, LU decomposition\n"
            "Week 3  (Sep 22-26):  Four fundamental subspaces, rank\n"
            "Week 4  (Sep 29-Oct 3): Orthogonality, projections, Gram-Schmidt\n"
            "Week 5  (Oct 6-10):   QR factorization, least squares\n"
            "Week 6  (Oct 13-17):  Review + MIDTERM EXAM (Oct 16)\n"
            "Week 7  (Oct 20-24):  Determinants, eigenvalues intro\n"
            "Week 8  (Oct 27-31):  Diagonalization, spectral theorem\n"
            "Week 9  (Nov 3-7):    Singular Value Decomposition\n"
            "Week 10 (Nov 10-14):  SVD applications, pseudoinverse\n"
            "Week 11 (Nov 17-21):  PCA, dimensionality reduction\n"
            "Week 12 (Nov 24-28):  Linear transformations, change of basis  [Wed-Fri only]\n"
            "Week 13 (Dec 1-5):    Numerical methods, iterative solvers\n"
            "Week 14 (Dec 8-11):   Review and exam preparation\n"
            "FINAL EXAM:           December 15, 2026"
        ),
        grading=(
            "Homework (5 sets):  50%\n"
            "Midterm Exam:       20%\n"
            "Computational Project: 10%\n"
            "Final Exam:         20%\n\n"
            "Late policy: 10% penalty per day late. No submissions accepted after 3 days.\n"
            "Grade scale: A 93+, A- 90, B+ 87, B 83, B- 80, C+ 77, C 73, C- 70, D 60, F <60."
        ),
        filename="math301_applied_linear_algebra.pdf",
    )


# ??????????????????????????????????????????????????????????????????????????????
#  Syllabus 2 - Portfolio Allocation and Asset Pricing (FIN 405)
# ??????????????????????????????????????????????????????????????????????????????

def gen_fin405():
    make_pdf(
        course_code="FIN 405",
        course_title="Portfolio Allocation and Asset Pricing",
        professor="Prof. James Morrison  |  jmorrison@university.edu  |  Business School 215",
        office_hours="Tue & Thu 3:30-5:00 PM, or by appointment",
        description=(
            "This advanced finance course examines the theory and practice of portfolio "
            "construction and asset pricing. Students will study Modern Portfolio Theory (MPT), "
            "the Capital Asset Pricing Model (CAPM), multi-factor models (Fama-French), options "
            "pricing (Black-Scholes), and risk management frameworks. Emphasis is placed on "
            "empirical implementation: students will use Python (pandas, yfinance, statsmodels) "
            "to download real market data and test theoretical predictions. The course meets "
            "Tuesday and Thursday from 2:00-3:15 PM in Business School 305."
        ),
        objectives=(
            "Students completing this course will:\n"
            "1. Construct mean-variance efficient portfolios and the efficient frontier.\n"
            "2. Apply CAPM and Fama-French 3-factor model to equity returns.\n"
            "3. Price European options using Black-Scholes and binomial trees.\n"
            "4. Measure and manage portfolio risk (VaR, CVaR, beta hedging).\n"
            "5. Present original empirical findings in a professional research report."
        ),
        materials=(
            "Primary: 'Investments' by Bodie, Kane, and Marcus, 12th ed. (McGraw-Hill).\n"
            "Supplement: 'Options, Futures, and Other Derivatives' by Hull, 11th ed.\n"
            "Software: Python 3.11+, Jupyter, pandas, numpy, scipy, yfinance, statsmodels.\n"
            "Bloomberg terminal access available in the Finance Lab (Business School B102)."
        ),
        assignments=[
            {
                "label": "Case Study 1 - Modern Portfolio Theory",
                "due": "September 25, 2026",
                "weight": "10%",
                "desc": (
                    "Download 5 years of daily returns for 10 S&P 500 stocks using yfinance. "
                    "Compute the covariance matrix, construct the minimum-variance portfolio and "
                    "the tangency portfolio, and plot the efficient frontier. Submit a Jupyter "
                    "notebook and a 2-page write-up. Due by 11:59 PM on Gradescope."
                ),
            },
            {
                "label": "Problem Set 1 - CAPM and Beta Estimation",
                "due": "October 9, 2026",
                "weight": "8%",
                "desc": (
                    "Theoretical problems plus empirical exercise: estimate betas for 5 stocks "
                    "via OLS regression against the market index. Test the CAPM prediction using "
                    "the Fama-MacBeth cross-sectional regression. Submit PDF on Gradescope."
                ),
            },
            {
                "label": "Midterm Exam",
                "due": "October 27, 2026",
                "weight": "22%",
                "desc": (
                    "In-class exam on MPT, CAPM, and multi-factor models. Covers Chapters 1-10 "
                    "of Bodie et al. Closed-book; one formula sheet (one-sided, 8.5x11) allowed. "
                    "Financial calculator permitted. Held 2:00-3:15 PM in Business School 305."
                ),
            },
            {
                "label": "Portfolio Project - Proposal",
                "due": "November 6, 2026",
                "weight": "5%",
                "desc": (
                    "One-page proposal describing your portfolio strategy: asset universe (minimum "
                    "15 securities across 3 sectors), time period, pricing model, and risk targets. "
                    "Include a preliminary data source plan. Submit on course portal."
                ),
            },
            {
                "label": "Case Study 2 - Options Pricing and the Volatility Surface",
                "due": "November 20, 2026",
                "weight": "10%",
                "desc": (
                    "Price a set of European put and call options on SPY using Black-Scholes. "
                    "Compute implied volatilities, plot the volatility surface, and discuss "
                    "deviations from BSM assumptions. Submit Jupyter notebook + 3-page report."
                ),
            },
            {
                "label": "Portfolio Project - Final Report",
                "due": "December 7, 2026",
                "weight": "25%",
                "desc": (
                    "Full empirical portfolio analysis (8-10 pages + appendices). Must include: "
                    "factor model estimation, portfolio optimization, out-of-sample back-test "
                    "(rolling 6-month window), Sharpe ratio and drawdown analysis, and risk "
                    "decomposition. Jupyter notebook required. Groups of 1-3 students."
                ),
            },
            {
                "label": "Final Exam",
                "due": "December 16, 2026",
                "weight": "20%",
                "desc": (
                    "Comprehensive 2-hour final covering all material including options pricing "
                    "and risk management. Held in registrar-assigned room. Formula sheet allowed "
                    "(two-sided, 8.5x11). Financial calculator permitted."
                ),
            },
        ],
        schedule_notes=(
            "Week 1  (Sep 8-10):   Risk and return basics, portfolio math\n"
            "Week 2  (Sep 15-17):  Modern Portfolio Theory, efficient frontier\n"
            "Week 3  (Sep 22-24):  CAPM derivation and assumptions\n"
            "Week 4  (Sep 29-Oct 1): CAPM empirical tests, beta estimation\n"
            "Week 5  (Oct 6-8):    Fama-French 3 & 5 factor models\n"
            "Week 6  (Oct 13-15):  Momentum, liquidity, and anomalies\n"
            "Week 7  (Oct 20-22):  Review; MIDTERM EXAM Oct 27\n"
            "Week 8  (Oct 27-29):  Fixed income basics, duration and convexity\n"
            "Week 9  (Nov 3-5):    Options: payoffs, put-call parity\n"
            "Week 10 (Nov 10-12):  Black-Scholes model, Greeks\n"
            "Week 11 (Nov 17-19):  Volatility surface, exotic options intro\n"
            "Week 12 (Nov 24):     Value at Risk and CVaR  [Thursday only - no Tuesday class]\n"
            "Week 13 (Dec 1-3):    Portfolio risk management, tail risk\n"
            "Week 14 (Dec 8-10):   Student project presentations + review\n"
            "FINAL EXAM:           December 16, 2026"
        ),
        grading=(
            "Case Studies (2):    20%\n"
            "Problem Set 1:        8%\n"
            "Portfolio Project:   30%  (proposal 5% + final 25%)\n"
            "Midterm Exam:        22%\n"
            "Final Exam:          20%\n\n"
            "Late policy: Case studies and problem sets lose 15% per day. "
            "Project proposal late submissions not accepted. "
            "Grade scale: A 93+, A- 90, B+ 87, B 83, B- 80, C+ 77, C 73, D 60, F <60."
        ),
        filename="fin405_portfolio_allocation.pdf",
    )


# ??????????????????????????????????????????????????????????????????????????????
#  Syllabus 3 - Software Development (CS 350)
# ??????????????????????????????????????????????????????????????????????????????

def gen_cs350():
    make_pdf(
        course_code="CS 350",
        course_title="Software Development",
        professor="Prof. Alex Rivera  |  arivera@university.edu  |  Engineering 312",
        office_hours="Mon 5:00-6:30 PM, Wed 1:00-2:30 PM, or by appointment",
        description=(
            "A project-oriented course on professional software engineering practices. Students "
            "work in teams of 3-4 using Agile/Scrum methodology to build a full-stack web "
            "application over three sprints. Topics include: version control with Git/GitHub, "
            "test-driven development (TDD), CI/CD pipelines (GitHub Actions), containerization "
            "(Docker), REST API design, design patterns, and code review best practices. "
            "Lecture: Mon/Wed 3:30-4:45 PM in Engineering 102. "
            "Lab: Friday 2:00-3:50 PM in Engineering Computer Lab 110."
        ),
        objectives=(
            "Students will:\n"
            "1. Apply Agile/Scrum practices including sprint planning, standups, and retrospectives.\n"
            "2. Use Git branching strategies and code review workflows professionally.\n"
            "3. Write unit, integration, and end-to-end tests using pytest and Playwright.\n"
            "4. Build and deploy a containerized web application with Docker and GitHub Actions.\n"
            "5. Design and implement a clean REST API following OpenAPI specification.\n"
            "6. Conduct and receive structured code reviews using industry-standard rubrics."
        ),
        materials=(
            "No required textbook. Weekly readings posted on course portal (free/open access).\n"
            "Software: Git, Python 3.11+, Node.js 20+, Docker Desktop, VS Code (recommended).\n"
            "Required accounts: GitHub (student pro account - free), GitHub Actions minutes provided.\n"
            "Recommended: 'Clean Code' by Robert C. Martin (optional but highly useful)."
        ),
        assignments=[
            {
                "label": "Lab 1 - Git Workflow and Code Review",
                "due": "September 14, 2026",
                "weight": "5%",
                "desc": (
                    "Fork the starter repository, implement a small feature using a feature branch, "
                    "open a pull request with a detailed description, and review a classmate's PR "
                    "using the provided rubric. Submit GitHub PR link on course portal by 11:59 PM."
                ),
            },
            {
                "label": "Lab 2 - Test-Driven Development",
                "due": "September 28, 2026",
                "weight": "5%",
                "desc": (
                    "Implement 3 small functions using the red-green-refactor TDD cycle with pytest. "
                    "Achieve 90%+ code coverage. Submit pytest report and code on GitHub by 11:59 PM."
                ),
            },
            {
                "label": "Sprint 1 Demo - MVP Feature Set",
                "due": "October 5, 2026",
                "weight": "10%",
                "desc": (
                    "Live 10-minute demo of your team's Sprint 1 deliverable in lab. Must include: "
                    "at least 3 working user stories, a passing CI pipeline, and a deployed demo "
                    "environment. Submit Sprint 1 retrospective document on course portal same day."
                ),
            },
            {
                "label": "Lab 3 - Docker and CI/CD",
                "due": "October 12, 2026",
                "weight": "5%",
                "desc": (
                    "Containerize a provided Flask application using Docker. Write a GitHub Actions "
                    "workflow that builds the image, runs tests, and publishes to GitHub Container "
                    "Registry. Submit docker-compose.yml, Dockerfile, and workflow YAML on GitHub."
                ),
            },
            {
                "label": "Midterm Exam",
                "due": "October 19, 2026",
                "weight": "15%",
                "desc": (
                    "Written exam on software engineering concepts: Git internals, testing theory, "
                    "design patterns (SOLID principles, Factory, Observer, Strategy), REST API design, "
                    "and Agile principles. Open-notes (personal notes only, not slides). 75 minutes."
                ),
            },
            {
                "label": "Sprint 2 Demo - Core Feature Complete",
                "due": "November 2, 2026",
                "weight": "15%",
                "desc": (
                    "15-minute live demo. Sprint 2 must add: database persistence, user authentication, "
                    "REST API endpoints, and full test coverage (>80%). Code review from another team "
                    "due at same time. Submit Sprint 2 retrospective and updated backlog."
                ),
            },
            {
                "label": "Lab 4 - REST API Design",
                "due": "November 9, 2026",
                "weight": "5%",
                "desc": (
                    "Design and implement a REST API for a given domain model. Write an OpenAPI 3.0 "
                    "specification, implement endpoints in FastAPI, and write integration tests. "
                    "Submit on GitHub by 11:59 PM."
                ),
            },
            {
                "label": "Code Review Assignment",
                "due": "November 16, 2026",
                "weight": "5%",
                "desc": (
                    "Conduct a structured code review of a provided codebase (400-line Python module). "
                    "Identify: bugs, security issues, performance bottlenecks, style violations, "
                    "and test gaps. Submit written review (minimum 600 words) on course portal."
                ),
            },
            {
                "label": "Sprint 3 Demo - Final Polish",
                "due": "November 30, 2026",
                "weight": "15%",
                "desc": (
                    "20-minute final sprint demo. Must include: complete feature set, end-to-end "
                    "tests with Playwright, full CI/CD pipeline, Docker Compose for local dev, "
                    "and production deployment (Render or Railway free tier). All team members "
                    "must present. Submit Sprint 3 retrospective."
                ),
            },
            {
                "label": "Final Project Submission",
                "due": "December 7, 2026",
                "weight": "10%",
                "desc": (
                    "Final code submission including: clean README, architecture diagram, API docs, "
                    "test results, and individual contribution summary. Tag release v1.0.0 on GitHub "
                    "and submit the tag link on the course portal by 11:59 PM."
                ),
            },
            {
                "label": "Final Exam",
                "due": "December 17, 2026",
                "weight": "10%",
                "desc": (
                    "Comprehensive written final covering all course topics. 90 minutes. "
                    "Emphasis on design patterns, system design, and trade-off analysis. "
                    "Open-notes (one 8.5x11 sheet, both sides)."
                ),
            },
        ],
        schedule_notes=(
            "Week 1  (Sep 8-12):   Course intro, Git review, team formation\n"
            "Week 2  (Sep 15-19):  Agile/Scrum, user stories, backlog grooming\n"
            "Week 3  (Sep 22-26):  TDD, pytest, mocking  [Sprint 1 begins]\n"
            "Week 4  (Sep 29-Oct 3): CI/CD, GitHub Actions basics\n"
            "Week 5  (Oct 6-10):   Docker, containers, docker-compose\n"
            "Week 6  (Oct 13-17):  Design patterns I + MIDTERM EXAM (Oct 19)\n"
            "Week 7  (Oct 20-24):  REST API design, OpenAPI; SPRINT 1 DEMO (Oct 5)\n"
            "Week 8  (Oct 27-31):  Databases, ORMs, migrations  [Sprint 2 begins]\n"
            "Week 9  (Nov 3-7):    Authentication, security basics\n"
            "Week 10 (Nov 10-14):  Design patterns II, code review techniques\n"
            "Week 11 (Nov 17-21):  End-to-end testing, Playwright  [Sprint 3 begins]\n"
            "Week 12 (Nov 24):     Deployment, monitoring  [Monday only]\n"
            "Week 13 (Dec 1-5):    Performance, refactoring, tech debt\n"
            "Week 14 (Dec 7-10):   Presentations and project demos\n"
            "FINAL EXAM:           December 17, 2026"
        ),
        grading=(
            "Labs (4):             20%\n"
            "Sprint Demos (3):     40%\n"
            "Code Review:           5%\n"
            "Final Project:        10%\n"
            "Midterm Exam:         15%\n"
            "Final Exam:           10%\n\n"
            "Team grades are adjusted by peer evaluation scores (+/-10%). "
            "Late labs lose 20% per day. Sprint demos cannot be submitted late. "
            "Grade scale: A 93+, A- 90, B+ 87, B 83, B- 80, C+ 77, C 73, D 60, F <60."
        ),
        filename="cs350_software_development.pdf",
    )


# ??????????????????????????????????????????????????????????????????????????????
#  Syllabus 4 - History and Philosophy of Science (HPS 220)
# ??????????????????????????????????????????????????????????????????????????????

def gen_hps220():
    make_pdf(
        course_code="HPS 220",
        course_title="History and Philosophy of Science",
        professor="Dr. Maya Patel  |  mpatel@university.edu  |  Humanities 318",
        office_hours="Tue 12:00-1:30 PM, Thu 11:30 AM-1:00 PM, or by appointment",
        description=(
            "How does science work? What makes a theory scientific? How do scientific revolutions "
            "happen, and who gets to participate in them? This course surveys major themes in the "
            "history and philosophy of science from the Scientific Revolution to the present. We "
            "examine foundational texts by Kuhn, Popper, Lakatos, Feyerabend, and Longino, and "
            "apply their frameworks to case studies in physics, biology, and medicine. Discussion-"
            "heavy format: students are expected to come to every class having done the readings. "
            "The course meets Tuesday and Thursday from 10:00-11:15 AM in Humanities 115."
        ),
        objectives=(
            "Students will be able to:\n"
            "1. Explain and critically evaluate major philosophical accounts of scientific method.\n"
            "2. Analyze historical episodes of scientific change using Kuhn's and Lakatos's frameworks.\n"
            "3. Situate science within its social, political, and cultural context.\n"
            "4. Write clear, well-argued philosophical essays using textual evidence.\n"
            "5. Engage charitably with opposing viewpoints in seminar discussion."
        ),
        materials=(
            "All readings provided as PDFs on the course portal (no textbook purchase required).\n"
            "Key texts: Kuhn 'The Structure of Scientific Revolutions'; Popper 'Conjectures and "
            "Refutations' (selected chapters); Lakatos 'The Methodology of Scientific Research "
            "Programmes'; Longino 'Science as Social Knowledge' (selected chapters).\n"
            "Recommended: Chalmers 'What Is This Thing Called Science?' (optional overview text)."
        ),
        assignments=[
            {
                "label": "Reading Response 1 - Scientific Revolutions",
                "due": "September 22, 2026",
                "weight": "5%",
                "desc": (
                    "One-page (400-500 word) response to Kuhn Chapters 1-5. Address: What is a "
                    "paradigm, and why does Kuhn think normal science is conservative? Where do you "
                    "agree or disagree with his account? Submit PDF on course portal by 11:59 PM."
                ),
            },
            {
                "label": "Reading Response 2 - Falsificationism and Its Critics",
                "due": "October 6, 2026",
                "weight": "5%",
                "desc": (
                    "One-page response to Popper's 'Science: Conjectures and Refutations' and Kuhn's "
                    "reply. Address: What is Popper's demarcation criterion, and how does Kuhn's "
                    "account challenge it? Which view do you find more persuasive, and why?"
                ),
            },
            {
                "label": "Essay 1 - Kuhn vs. Popper on Scientific Progress",
                "due": "October 20, 2026",
                "weight": "15%",
                "desc": (
                    "3-page argumentative essay (900-1000 words, double-spaced, 12pt Times New Roman, "
                    "1-inch margins). Thesis-driven: defend a clear position on whether Kuhn's or "
                    "Popper's account better explains a specific episode of scientific change. "
                    "Use at least 3 primary sources and 1 secondary source. "
                    "Submit PDF on course portal by 11:59 PM."
                ),
            },
            {
                "label": "Reading Response 3 - Lakatos and Research Programmes",
                "due": "November 3, 2026",
                "weight": "5%",
                "desc": (
                    "One-page response to Lakatos 'Falsification and the Methodology of Scientific "
                    "Research Programmes.' Address: How does Lakatos try to reconcile Popper and Kuhn? "
                    "What is the difference between a progressive and a degenerating research programme?"
                ),
            },
            {
                "label": "Essay 2 - Social Epistemology and Scientific Objectivity",
                "due": "November 17, 2026",
                "weight": "20%",
                "desc": (
                    "5-page argumentative essay (1400-1600 words). Choose ONE of the following prompts:\n"
                    "(A) Is Longino right that objectivity requires social diversity in science?\n"
                    "(B) Does the underdetermination of theory by evidence threaten scientific realism?\n"
                    "(C) Can feminist philosophy of science improve the epistemic credentials of science?\n"
                    "Engage with at least 4 primary sources and 2 peer-reviewed secondary sources. "
                    "Submit PDF on course portal."
                ),
            },
            {
                "label": "Reading Response 4 - Science and Society",
                "due": "December 1, 2026",
                "weight": "5%",
                "desc": (
                    "One-page response to Oreskes & Conway 'Merchants of Doubt' (excerpt). Address: "
                    "What does this case study reveal about the relationship between industry, politics, "
                    "and the production of scientific uncertainty? What are the implications for how we "
                    "evaluate expert consensus?"
                ),
            },
            {
                "label": "Final Paper - Draft",
                "due": "December 4, 2026",
                "weight": "5%",
                "desc": (
                    "Submit a complete draft of your final paper (see below) for peer workshop. "
                    "Bring 2 printed copies to Thursday's class. Draft does not need to be polished "
                    "but must have a clear thesis, argument structure, and bibliography. "
                    "Also submit PDF on course portal by 11:59 PM."
                ),
            },
            {
                "label": "Final Paper - A Philosophical Analysis of a Scientific Controversy",
                "due": "December 14, 2026",
                "weight": "30%",
                "desc": (
                    "10-page research paper (2800-3200 words). Choose a real scientific controversy "
                    "(historical or contemporary) and analyze it through the lens of at least TWO "
                    "philosophical frameworks studied in the course. Your paper must: (1) accurately "
                    "describe the scientific controversy, (2) apply philosophical frameworks rigorously, "
                    "(3) defend an original thesis about what the controversy reveals about how science "
                    "works or should work, and (4) engage with at least 6 academic sources. "
                    "Submit PDF on course portal by 11:59 PM."
                ),
            },
            {
                "label": "Class Participation",
                "due": "Throughout semester",
                "weight": "10%",
                "desc": (
                    "Active, prepared, and respectful participation in seminar discussions, "
                    "assessed holistically at the end of the semester. Quality over quantity. "
                    "Missing more than 3 classes without excuse results in automatic grade reduction."
                ),
            },
        ],
        schedule_notes=(
            "Week 1  (Sep 8-10):   What is philosophy of science? Course overview\n"
            "Week 2  (Sep 15-17):  The Scientific Revolution - Galileo, Newton, methodology\n"
            "Week 3  (Sep 22-24):  Kuhn - Structure of Scientific Revolutions I\n"
            "Week 4  (Sep 29-Oct 1): Kuhn - Revolutions II + Popper on falsification\n"
            "Week 5  (Oct 6-8):    Popper vs. Kuhn; Feyerabend 'Against Method'\n"
            "Week 6  (Oct 13-15):  Lakatos and research programmes\n"
            "Week 7  (Oct 20-22):  Essay 1 due Oct 20; Bayesianism and confirmation theory\n"
            "Week 8  (Oct 27-29):  Scientific realism vs. anti-realism\n"
            "Week 9  (Nov 3-5):    Social epistemology; Longino on objectivity\n"
            "Week 10 (Nov 10-12):  Feminist philosophy of science\n"
            "Week 11 (Nov 17-19):  Philosophy of biology: evolution and function\n"
            "Week 12 (Nov 24):     Science and policy; climate change case study  [Tue only]\n"
            "Week 13 (Dec 1-3):    Science denial, expertise, and public trust\n"
            "Week 14 (Dec 8-10):   Final paper workshops; course synthesis\n"
            "FINAL PAPER DUE:      December 14, 2026  (no final exam)"
        ),
        grading=(
            "Reading Responses (4): 20%\n"
            "Essay 1 (3 pages):     15%\n"
            "Essay 2 (5 pages):     20%\n"
            "Final Paper Draft:      5%\n"
            "Final Paper (10 pages): 30%\n"
            "Participation:         10%\n\n"
            "Late policy: Essays lose 1/3 grade per day late (A -> A- -> B+ ...). "
            "Reading responses not accepted late. Extensions granted only for documented emergencies "
            "requested at least 48 hours before the deadline. "
            "Grade scale: A 93+, A- 90, B+ 87, B 83, B- 80, C+ 77, C 73, D 60, F <60."
        ),
        filename="hps220_history_philosophy_science.pdf",
    )


# ??????????????????????????????????????????????????????????????????????????????
#  ICS Calendar - Class Schedule (recurring class meetings)
# ??????????????????????????????????????????????????????????????????????????????

def gen_class_schedule_ics():
    """Weekly recurring class meetings for all four courses."""

    def vevent(uid, summary, dtstart, dtend, location, rrule, description=""):
        return (
            "BEGIN:VEVENT\n"
            f"UID:{uid}\n"
            f"SUMMARY:{summary}\n"
            f"DTSTART;TZID=America/New_York:{dtstart}\n"
            f"DTEND;TZID=America/New_York:{dtend}\n"
            f"LOCATION:{location}\n"
            f"RRULE:{rrule}\n"
            + (f"DESCRIPTION:{description}\n" if description else "")
            + "END:VEVENT\n"
        )

    events = []

    # MATH 301 - Mon/Wed/Fri 10:00-10:50 AM
    events.append(vevent(
        uid="math301-mwf@university.edu",
        summary="MATH 301 - Applied Linear Algebra",
        dtstart="20260909T100000",
        dtend="20260909T105000",
        location="Science Hall 201",
        rrule="FREQ=WEEKLY;BYDAY=MO,WE,FR;UNTIL=20261211T235959Z",
        description="Dr. Sarah Chen. Bring textbook and scientific calculator.",
    ))

    # FIN 405 - Tue/Thu 2:00-3:15 PM
    events.append(vevent(
        uid="fin405-tth@university.edu",
        summary="FIN 405 - Portfolio Allocation and Asset Pricing",
        dtstart="20260908T140000",
        dtend="20260908T151500",
        location="Business School 305",
        rrule="FREQ=WEEKLY;BYDAY=TU,TH;UNTIL=20261210T235959Z",
        description="Prof. James Morrison. Bring laptop with Python environment.",
    ))

    # CS 350 - Mon/Wed 3:30-4:45 PM
    events.append(vevent(
        uid="cs350-mw@university.edu",
        summary="CS 350 - Software Development (Lecture)",
        dtstart="20260909T153000",
        dtend="20260909T164500",
        location="Engineering 102",
        rrule="FREQ=WEEKLY;BYDAY=MO,WE;UNTIL=20261209T235959Z",
        description="Prof. Alex Rivera. Bring laptop.",
    ))

    # CS 350 - Friday Lab 2:00-3:50 PM
    events.append(vevent(
        uid="cs350-lab-fri@university.edu",
        summary="CS 350 - Software Development Lab",
        dtstart="20260911T140000",
        dtend="20260911T155000",
        location="Engineering Computer Lab 110",
        rrule="FREQ=WEEKLY;BYDAY=FR;UNTIL=20261211T235959Z",
        description="CS 350 Friday lab section. Bring laptop. Labs due at 11:59 PM same day.",
    ))

    # HPS 220 - Tue/Thu 10:00-11:15 AM
    events.append(vevent(
        uid="hps220-tth@university.edu",
        summary="HPS 220 - History and Philosophy of Science",
        dtstart="20260908T100000",
        dtend="20260908T111500",
        location="Humanities 115",
        rrule="FREQ=WEEKLY;BYDAY=TU,TH;UNTIL=20261210T235959Z",
        description="Dr. Maya Patel. Complete all readings before class. Discussion-heavy.",
    ))

    # Gym - Mon/Wed/Fri 7:00-8:00 AM
    events.append(vevent(
        uid="gym-mwf@personal",
        summary="Gym / Workout",
        dtstart="20260909T070000",
        dtend="20260909T080000",
        location="Campus Recreation Center",
        rrule="FREQ=WEEKLY;BYDAY=MO,WE,FR;UNTIL=20261212T235959Z",
        description="Morning workout routine. Cardio Mon/Fri, strength Wed.",
    ))

    # Weekly study block - Sunday evenings
    events.append(vevent(
        uid="study-sun@personal",
        summary="Weekly Planning and Study Block",
        dtstart="20260913T190000",
        dtend="20260913T210000",
        location="Library Study Room",
        rrule="FREQ=WEEKLY;BYDAY=SU;UNTIL=20261213T235959Z",
        description="Weekly review: check upcoming deadlines, plan the week, catch up on readings.",
    ))

    # Thanksgiving break - no classes Nov 25-28
    events.append(
        "BEGIN:VEVENT\n"
        "UID:thanksgiving-break@university.edu\n"
        "SUMMARY:Thanksgiving Break - No Classes\n"
        "DTSTART;VALUE=DATE:20261125\n"
        "DTEND;VALUE=DATE:20261129\n"
        "DESCRIPTION:University closed Nov 25-28. Enjoy the break!\n"
        "END:VEVENT\n"
    )

    # Fall break - no classes Oct 19-23
    events.append(
        "BEGIN:VEVENT\n"
        "UID:fall-break@university.edu\n"
        "SUMMARY:Fall Break - No Classes\n"
        "DTSTART;VALUE=DATE:20261019\n"
        "DTEND;VALUE=DATE:20261024\n"
        "DESCRIPTION:Fall recess. No classes Mon-Fri. A good time to catch up on projects.\n"
        "END:VEVENT\n"
    )

    ics_content = (
        "BEGIN:VCALENDAR\n"
        "VERSION:2.0\n"
        "PRODID:-//Planner RAG Agent//Class Schedule Fall 2026//EN\n"
        "CALSCALE:GREGORIAN\n"
        "X-WR-CALNAME:Fall 2026 Class Schedule\n"
        "X-WR-TIMEZONE:America/New_York\n"
        + "".join(events)
        + "END:VCALENDAR\n"
    )

    out = CAL_DIR / "class_schedule.ics"
    out.write_text(ics_content)
    print(f"  Created: {out.relative_to(ROOT)}")


# ??????????????????????????????????????????????????????????????????????????????
#  ICS Calendar - All Deadlines (assignments, exams, project milestones)
# ??????????????????????????????????????????????????????????????????????????????

def gen_deadlines_ics():
    """All-day deadline events for every assignment and exam."""

    def deadline(uid, summary, date_str, description="", priority=""):
        alarm = (
            "BEGIN:VALARM\n"
            "TRIGGER:-P1D\n"
            "ACTION:DISPLAY\n"
            f"DESCRIPTION:Reminder: {summary} due tomorrow!\n"
            "END:VALARM\n"
        ) if priority == "high" else ""
        return (
            "BEGIN:VEVENT\n"
            f"UID:{uid}\n"
            f"SUMMARY:{summary}\n"
            f"DTSTART;VALUE=DATE:{date_str}\n"
            f"DTEND;VALUE=DATE:{date_str}\n"
            + (f"DESCRIPTION:{description}\n" if description else "")
            + (f"PRIORITY:{'1' if priority == 'high' else '5'}\n")
            + alarm
            + "END:VEVENT\n"
        )

    deadlines = [
        # ?? MATH 301 ??????????????????????????????????????????????????????
        deadline("math301-hw1", "MATH 301 HW1 Due - Vectors & Matrix Operations",
                 "20260918", "Submit on Gradescope by 11:59 PM.", "low"),
        deadline("math301-hw2", "MATH 301 HW2 Due - Linear Independence & Rank",
                 "20261002", "Submit on Gradescope by 11:59 PM.", "low"),
        deadline("math301-midterm", "MATH 301 MIDTERM EXAM - In Class",
                 "20261016", "Science Hall 201, 10:00-10:50 AM. 1 index card allowed.", "high"),
        deadline("math301-hw3", "MATH 301 HW3 Due - Eigenvalues & Eigenvectors",
                 "20261030", "Submit on Gradescope by 11:59 PM.", "low"),
        deadline("math301-hw4", "MATH 301 HW4 Due - SVD & Least Squares",
                 "20261113", "Submit on Gradescope by 11:59 PM.", "low"),
        deadline("math301-hw5", "MATH 301 HW5 Due - Linear Transformations",
                 "20261121", "Submit on Gradescope by 11:59 PM.", "low"),
        deadline("math301-project", "MATH 301 Computational Project Due - PCA Analysis",
                 "20261204", "Jupyter notebook + 4-page report. Submit on course portal.", "medium"),
        deadline("math301-final", "MATH 301 FINAL EXAM",
                 "20261215", "Comprehensive. 1 sheet of notes (both sides). Scientific calculator.", "high"),

        # ?? FIN 405 ???????????????????????????????????????????????????????
        deadline("fin405-case1", "FIN 405 Case Study 1 Due - Modern Portfolio Theory",
                 "20260925", "Jupyter notebook + 2-page write-up on Gradescope.", "medium"),
        deadline("fin405-pset1", "FIN 405 Problem Set 1 Due - CAPM & Beta Estimation",
                 "20261009", "Submit PDF on Gradescope by 11:59 PM.", "low"),
        deadline("fin405-midterm", "FIN 405 MIDTERM EXAM - In Class",
                 "20261027", "Business School 305, 2:00-3:15 PM. Formula sheet allowed.", "high"),
        deadline("fin405-proposal", "FIN 405 Portfolio Project Proposal Due",
                 "20261106", "1-page proposal on course portal. Not accepted late.", "medium"),
        deadline("fin405-case2", "FIN 405 Case Study 2 Due - Options & Volatility Surface",
                 "20261120", "Jupyter notebook + 3-page report on Gradescope.", "medium"),
        deadline("fin405-project", "FIN 405 Portfolio Project Final Report Due",
                 "20261207", "8-10 pages + appendices + Jupyter notebook. Course portal.", "medium"),
        deadline("fin405-final", "FIN 405 FINAL EXAM",
                 "20261216", "2-hour comprehensive exam. Formula sheet (two-sided) allowed.", "high"),

        # ?? CS 350 ????????????????????????????????????????????????????????
        deadline("cs350-lab1", "CS 350 Lab 1 Due - Git Workflow & Code Review",
                 "20260914", "Submit GitHub PR link on course portal.", "low"),
        deadline("cs350-lab2", "CS 350 Lab 2 Due - Test-Driven Development",
                 "20260928", "Submit pytest report and code on GitHub.", "low"),
        deadline("cs350-sprint1", "CS 350 SPRINT 1 DEMO - MVP Feature Set",
                 "20261005", "10-min live demo in lab. Sprint 1 retrospective due same day.", "medium"),
        deadline("cs350-lab3", "CS 350 Lab 3 Due - Docker & CI/CD",
                 "20261012", "Submit docker-compose.yml, Dockerfile, workflow YAML.", "low"),
        deadline("cs350-midterm", "CS 350 MIDTERM EXAM - In Class",
                 "20261019", "Engineering 102, 3:30 PM. Open notes (personal notes only).", "high"),
        deadline("cs350-sprint2", "CS 350 SPRINT 2 DEMO - Core Feature Complete",
                 "20261102", "15-min demo. Auth, DB, REST API, 80%+ test coverage.", "medium"),
        deadline("cs350-lab4", "CS 350 Lab 4 Due - REST API Design",
                 "20261109", "OpenAPI spec + FastAPI endpoints + integration tests.", "low"),
        deadline("cs350-codereview", "CS 350 Code Review Assignment Due",
                 "20261116", "Written review (min 600 words) on course portal.", "low"),
        deadline("cs350-sprint3", "CS 350 SPRINT 3 DEMO - Final Polish",
                 "20261130", "20-min demo. E2E tests, CI/CD, Docker Compose, deployed app.", "medium"),
        deadline("cs350-final-submission", "CS 350 Final Project Submission Due",
                 "20261207", "Tag v1.0.0 on GitHub. README, architecture docs, test results.", "medium"),
        deadline("cs350-final-exam", "CS 350 FINAL EXAM",
                 "20261217", "90-min exam. Open notes (one 8.5x11 sheet, both sides).", "high"),

        # ?? HPS 220 ???????????????????????????????????????????????????????
        deadline("hps220-resp1", "HPS 220 Reading Response 1 Due - Scientific Revolutions",
                 "20260922", "400-500 words on Kuhn Chapters 1-5. Submit PDF on portal.", "low"),
        deadline("hps220-resp2", "HPS 220 Reading Response 2 Due - Falsificationism",
                 "20261006", "1-page response: Popper vs Kuhn. Submit PDF on portal.", "low"),
        deadline("hps220-essay1", "HPS 220 Essay 1 Due - Kuhn vs. Popper",
                 "20261020", "3 pages (900-1000 words). Argumentative, thesis-driven. PDF on portal.", "medium"),
        deadline("hps220-resp3", "HPS 220 Reading Response 3 Due - Lakatos",
                 "20261103", "1-page response on Lakatos's methodology. Submit PDF on portal.", "low"),
        deadline("hps220-essay2", "HPS 220 Essay 2 Due - Social Epistemology",
                 "20261117", "5 pages (1400-1600 words). Choose one of three prompts. PDF on portal.", "medium"),
        deadline("hps220-resp4", "HPS 220 Reading Response 4 Due - Science & Society",
                 "20261201", "1-page response on Oreskes & Conway excerpt. PDF on portal.", "low"),
        deadline("hps220-draft", "HPS 220 Final Paper DRAFT Due",
                 "20261204", "Bring 2 printed copies to class AND submit PDF on portal.", "medium"),
        deadline("hps220-finalpaper", "HPS 220 FINAL PAPER Due - Scientific Controversy Analysis",
                 "20261214", "10 pages (2800-3200 words). 6+ academic sources. Submit PDF on portal.", "high"),
    ]

    ics_content = (
        "BEGIN:VCALENDAR\n"
        "VERSION:2.0\n"
        "PRODID:-//Planner RAG Agent//Deadlines Fall 2026//EN\n"
        "CALSCALE:GREGORIAN\n"
        "X-WR-CALNAME:Fall 2026 Deadlines\n"
        + "".join(deadlines)
        + "END:VCALENDAR\n"
    )

    out = CAL_DIR / "deadlines.ics"
    out.write_text(ics_content)
    print(f"  Created: {out.relative_to(ROOT)}")


# ??????????????????????????????????????????????????????????????????????????????
#  Main
# ??????????????????????????????????????????????????????????????????????????????

if __name__ == "__main__":
    print("Generating synthetic data for Planner RAG Agent...\n")

    print("PDFs:")
    gen_math301()
    gen_fin405()
    gen_cs350()
    gen_hps220()

    print("\nCalendars:")
    gen_class_schedule_ics()
    gen_deadlines_ics()

    print("\nAll data generated successfully.")
    print("Next step: run  python -m src.cli ingest")
