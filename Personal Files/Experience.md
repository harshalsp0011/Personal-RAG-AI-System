# Experience

---

## General Context (Applies to All Roles)
- Version control & CI/CD: GitHub, GitHub Actions (automated testing, builds, deployments)
- LLM APIs used across roles: OpenAI, Anthropic, Google Gemini, Hugging Face (NLP/classification)
- Local LLMs via Ollama for PII/sensitive data workloads
- AI tooling: GitHub Copilot, chatbot interfaces, conversational agents over data pipelines

---

## Experience 1 — Troy & Banks Inc | Data Engineer

**Core Scope:** Built end-to-end automation and AI platform — ETL pipelines, multi-agent LLM systems, cloud infrastructure — to reduce manual effort and enable data-driven billing audit and sales operations across two interconnected systems built within the same role.

**Key Concepts:** ETL/ELT, PDF parsing, SCD Type 2, data validation, observability, multi-agent LLM, LangGraph, LangChain, Airflow orchestration, IaC, Terraform, containerization, Docker, REST APIs, Streamlit, FastAPI, PostgreSQL, AWS, Prometheus, Grafana

**Overall Stack:** Python, Apache Airflow, n8n, PostgreSQL (AWS RDS via Heroku), Docker, Terraform, AWS (EC2, S3, IAM, networking), Nginx, Streamlit, React.js, FastAPI, Prometheus, Grafana, LangChain, LangGraph, Tavily, Hunter.io, SendGrid, Slack Webhooks, Camelot, pdfplumber, SQLAlchemy

---

### Sub-Project A: Utility Billing ETL & Audit Automation

**What it solved:** Manual utility bill auditing — parsed 600+ pages of tariff documents and 1,000+ bills/month into structured data, automated anomaly detection and audit reporting

**Details:**
1. Built end-to-end ETL platform ingesting tariff documents and bills using PDF parsing (Camelot, pdfplumber), pandas bulk processing, and SQLAlchemy ORM into PostgreSQL
2. Engineered tariff modeling layer: parsed PDFs → JSON → classified by rule type → normalized PostgreSQL tables covering 600+ pages of tariff documents
3. Implemented SCD Type 2 schema to track historical tariff rule versions, enabling time-accurate audits against correct rule set at bill issuance
4. Stored raw and processed documents in AWS S3 — separating input artifacts from curated relational data
5. Built custom calculation engine applying stored tariff rules to each bill, computing expected amount, and flagging discrepancies
6. Developed validation engine with extraction accuracy checks, mismatch flagging, and data quality alerts
7. Enforced PII protection via field encryption and secure storage patterns for sensitive bill data
8. Exposed Streamlit app for auditors: upload bills/tariffs, adjust variables, view real-time audit results, centralized logs, secure authentication
9. Orchestrated ETL and audit workflows via Airflow DAGs with monitoring, email notifications, retries, and scheduling
10. Migrated tightly coupled UI-backend to API-based architecture with retry/backoff and cached GET responses — ~50% latency improvement
11. Containerized all services with Docker; provisioned AWS infra (EC2, Elastic IPs, IAM, security groups, networking) with Terraform; configured Nginx reverse proxy with SSL termination
12. Achieved ~60% reduction in manual audit labor; scaled to processing 1,000+ bills/month; improved downstream analytics and BI dashboard data quality
13. Collaborated with business stakeholders through requirements gathering, solution demos, and change validation; used Jira with data engineering team for task tracking

---

### Sub-Project B: Lead Intelligence Multi-Agent Platform

**What it solved:** Manual sales prospecting — automated prospect discovery, fit scoring, personalized email drafting, outreach sequencing, and engagement tracking for the sales team

**Details:**
1. Architected stateful multi-agent workflow using LangChain + LangGraph — nodes as specialized agents, transitions implementing branching, retries, and quality gates
2. Defined 5 specialized agents: Scout (prospect discovery), Analyst (fit scoring and savings evaluation), Writer (personalized email drafting), Outreach (sending and follow-up sequencing), Tracker (reply and engagement monitoring)
3. Implemented agent memory: short-term LangGraph state + long-term PostgreSQL-backed storage tracking prompt version win rates, industry/location performance, and prior run outcomes so subsequent runs adapt strategy
4. Integrated external APIs: Tavily (web research and discovery), Hunter.io (email/contact enrichment), SendGrid (email delivery and sequencing), Slack Incoming Webhooks (real-time sales team alerts)
5. Added policy-based approval gates — no outreach sent without confidence-scored, validated drafts ensuring quality and compliance
6. Implemented observability: Prometheus metrics (latency, enrichment success rate, draft approval rate, token/API cost per run, lead yield by source) + Grafana dashboards with quality heatmaps, cost-per-qualified-lead tracking, and alerts for quality drops and cost spikes
7. Exposed React.js dashboard for sales team: inspect pipelines, approve/reject drafts, review engagement metrics
8. Used FastAPI as control-plane API for triggering runs, tracking state, and exposing multi-agent execution summaries to internal tools
9. Scheduled recurring lead-generation and outreach runs via Airflow DAGs orchestrating multi-agent flows through FastAPI endpoints, summarizing outcomes into reports
10. Containerized platform with Docker; provisioned AWS infrastructure with Terraform — repeatable, version-controlled deployments across environments
11. Replaced manual research and outreach with AI-driven system identifying energy overpayment candidates, scoring them, and delivering targeted data-backed outreach at scale

---

## Experience 2 — Reliance Jio Platforms Ltd | Software Development Engineer | Assistant Manager

**Core Scope:** Led data platform development for FTTX fiber network deployment lifecycle — ETL pipelines, GIS data processing, REST APIs, workflow orchestration, billing, and user management across cross-functional teams.

**Key Concepts:** ETL, MySQL, REST APIs, Camunda workflow orchestration, GIS data processing, query optimization, database schema design, SAP integration, role-based access control, unit testing, logging, monitoring, Azure DevOps, CI/CD

**Stack:** .NET (C#), Python, MySQL, Camunda, Entity Framework, REST APIs, Mudblazor, Azure DevOps, SAP APIs

**Details:**
1. Led end-to-end data platform development using .NET, Python, MySQL, and Camunda — automated FTTX deployment lifecycle, eliminated spreadsheet-based workflows
2. Designed and operated ETL jobs ingesting and cleaning 100K+ daily GIS and log records into centralized MySQL data store for reporting and downstream systems
3. Optimized database schemas and analytical queries — 20% query performance improvement; exposed structured deployment and financial data via RESTful APIs
4. Collaborated with planning, finance, and field teams to define critical fields, validations, and reports removing deployment and cost bottlenecks
5. Implemented Camunda workflows to orchestrate pipeline execution; built REST APIs connecting database with Mudblazor web platform
6. Developed Material Management flow including BOQ/SOQ processing
7. Built User Management system integrated with SAP APIs — authentication, validation, role-based workflow pipeline for user tasks and permissions
8. Created User Billing module for accurate bill calculation and validation with high precision
9. Collaborated with GIS team to optimize location-based database; implemented logging and monitoring for reliability and traceability
10. Conducted unit testing across full product lifecycle — web UI functionality, validation checks, data consistency, and retrieval accuracy
11. Used Azure DevOps for documentation, unit testing, and issue resolution; deployed across dev/test/pre-prod/prod environments using CI/CD pipelines
12. Collaborated with multiple cross-functional teams, gathering requirements from stakeholders and delivering end-to-end solutions with sustained support

---

## Experience 3 — Incerro.ai (CodeBin) | Frontend/Integration Engineer

**Core Scope:** Built and integrated frontend data-facing features for an AI-powered e-commerce and SaaS web platform — connecting UI to backend AI services and data pipelines via REST APIs.

**Key Concepts:** REST API integration, data validation, error handling, frontend-backend data flow, reusable UI components, end-to-end testing, SaaS product development, AI model output integration

**Stack:** REST APIs, frontend frameworks, backend AI services integration

**Details:**
1. Connected frontend to backend AI and data services via REST APIs on an AI-powered platform for e-commerce and SaaS clients
2. Integrated live data feeds and AI model outputs into UI; designed request/response models for API interactions
3. Implemented data validation and error handling to prevent broken or bad data from reaching UI or crashing the frontend
4. Collaborated with backend engineers to make API integrations production-ready
5. Refactored UI components for reusability and maintainability
6. Tested features end-to-end ensuring full API-to-UI flow worked correctly
7. Ensured reliable data flows from backend services into the user-facing product