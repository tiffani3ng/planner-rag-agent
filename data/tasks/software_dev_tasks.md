# CS 350 — Software Development: Personal Task List

## Lab 1 — Git Workflow and Code Review (Due September 14, 2026)

- Fork the cs350-lab1 starter repo on GitHub — due September 10, 2026
- Create feature branch: git checkout -b feature/add-calculator
- Implement the calculator feature following the spec in README
- Write at least 3 unit tests for the new feature (pytest)
- Open pull request with: description, screenshots, testing notes
- Review a classmate's PR: use the provided code review rubric checklist
- Submit GitHub PR link on course portal by 11:59 PM September 14, 2026

## Lab 2 — Test-Driven Development (Due September 28, 2026)

- Read the TDD chapter from course readings before starting
- Set up pytest and pytest-cov in your virtual environment
- Function 1 (red-green-refactor): binary search with edge cases
- Function 2 (red-green-refactor): Roman numeral converter
- Function 3 (red-green-refactor): CSV parser with malformed row handling
- Verify 90%+ code coverage: run pytest --cov and screenshot the report
- Submit code + coverage report on GitHub by 11:59 PM September 28, 2026

## Sprint 1 Preparation (Demo: October 5, 2026)

- Sprint planning meeting with team — schedule for September 15, 2026
- Write and estimate user stories in GitHub Issues (use story points)
- Set up team repository, branch protection rules, and PR template — due September 16, 2026
- Assign Sprint 1 issues to team members; update project board
- Set up GitHub Actions CI: run pytest on every PR — due September 19, 2026
- Implement at least 3 user stories with tests — working software only
- Deploy demo environment (Render free tier or GitHub Pages) — due October 3, 2026
- Write Sprint 1 retrospective document (what went well, what to improve) — due October 5, 2026
- 10-minute demo rehearsal with team the day before: October 4, 2026

## Lab 3 — Docker and CI/CD (Due October 12, 2026)

- Pull the provided Flask app repository from course portal
- Write Dockerfile: use python:3.11-slim base, install deps, expose port 5000
- Write docker-compose.yml: app + postgres database service with volumes
- Write GitHub Actions workflow: build image → run tests → push to GHCR
- Verify workflow passes end-to-end in GitHub Actions
- Submit docker-compose.yml, Dockerfile, and .github/workflows/ci.yml on GitHub — due October 12, 2026

## Midterm Exam Prep (Exam: October 19, 2026)

- Review lecture slides on SOLID principles — due October 14, 2026
- Flashcards for design patterns: Factory, Observer, Strategy, Decorator, Singleton
- Know the difference: unit test vs integration test vs end-to-end test
- Practice: draw class diagrams for Factory and Observer patterns from memory
- Review REST API design principles: idempotency, resource naming, HTTP status codes
- Review Agile concepts: velocity, burndown chart, definition of done
- Open-notes policy: organize personal notes into one coherent reference sheet

## Sprint 2 Preparation (Demo: November 2, 2026)

- Sprint 2 planning meeting — schedule for October 7, 2026
- Add database models with SQLAlchemy: User, Session (or project-specific models)
- Implement user authentication: JWT tokens or session-based (Flask-Login)
- Design REST API endpoints following OpenAPI spec — at least 5 CRUD endpoints
- Write integration tests hitting the actual database (use test database)
- Achieve >80% test coverage overall (check with pytest-cov)
- Set up database migrations with Alembic
- Peer code review exchange with assigned team — due October 29, 2026
- Sprint 2 retrospective document — due November 2, 2026
- 15-minute demo rehearsal with team: October 31, 2026

## Lab 4 — REST API Design (Due November 9, 2026)

- Read the OpenAPI 3.0 specification tutorial on course portal
- Design API for the provided domain model (Library Management System)
- Write complete openapi.yaml: all endpoints, request/response schemas, error codes
- Implement all endpoints in FastAPI (use provided skeleton)
- Write integration tests with httpx.AsyncClient for every endpoint
- Ensure proper HTTP status codes: 200, 201, 204, 400, 404, 422, 500
- Submit on GitHub by 11:59 PM November 9, 2026

## Code Review Assignment (Due November 16, 2026)

- Download the provided codebase from course portal (400-line Python module)
- Read all code carefully — first pass for understanding, second pass for issues
- Identify and document: at least 2 bugs, 1 security issue, 2 performance issues, style violations
- Check test coverage: what scenarios are not tested?
- Write structured review (minimum 600 words): intro, findings, recommendations, conclusion
- Use inline code references (function names, line numbers) to support each finding
- Submit written review as PDF on course portal by 11:59 PM November 16, 2026

## Sprint 3 Preparation (Demo: November 30, 2026)

- Sprint 3 planning — schedule for November 5, 2026
- Set up Playwright for end-to-end tests: install, configure browser, write 5+ E2E tests
- Polish all existing features: fix bugs from Sprint 2 feedback
- Add production deployment: configure Render.com or Railway.app
- Update docker-compose.yml for full local dev setup (app + db + redis if needed)
- Write complete README: setup, architecture diagram (draw.io or Mermaid), API docs
- Sprint 3 retrospective — due November 30, 2026
- Full team rehearsal (20 minutes): November 28, 2026

## Final Project Submission (Due December 7, 2026)

- Finalize all code — feature freeze December 5, 2026
- Tag release v1.0.0 on GitHub: git tag -a v1.0.0 -m "Production release"
- Verify all GitHub Actions workflows pass on the tagged commit
- Write individual contribution summary (1 page per person)
- Final README review: setup instructions, architecture, API docs, test instructions
- Submit GitHub release tag link on course portal by 11:59 PM December 7, 2026

## Final Exam Prep (Exam: December 17, 2026)

- Review all design patterns covered in lecture (Factory, Observer, Strategy, Command, Adapter)
- Practice system design questions: design a URL shortener, design a task queue
- Review trade-off analysis: when to use SQL vs NoSQL, monolith vs microservices
- Prepare one 8.5x11 reference sheet (both sides allowed)
- Work through 2 past finals from course portal under timed conditions (90 min each)
