# Projects

---

## Project 1 — EV Charging Data Warehouse
**Link:** https://github.com/harshalsp0011/ev-charging-data-warehouse

**Core Scope:** End-to-end data warehouse for smart mobility sector — centralizing EV station, weather, and charging transaction data to enable demand forecasting and infrastructure optimization.

**Key Concepts:** ETL/ELT, star schema, dimensional modeling, data quality engine, source-to-target mapping, API integration, Snowflake, dbt, cloud warehousing, ML-ready design, Airflow orchestration, data documentation

**Stack:** Python (Pandas, SQLAlchemy), Snowflake, SQL, dbt, Streamlit, Docker, Apache Airflow, GitHub, NREL API, OpenWeather API

**Details:**
1. Architected star schema in Snowflake: central FACT_CHARGING table linked to DIM_STATIONS, DIM_WEATHER, DIM_TIME dimensions — optimized for high-performance analytics
2. Built modular ETL pipeline: raw CSV session data + real-time API feeds → Python cleaning/validation → transformation → structured Snowflake tables
3. Developed modular API connectors for NREL (EV station infrastructure) and OpenWeather (environmental conditions) — with rate-limiting, authentication handling, and complex JSON parsing
4. Used dbt for dimensional modeling and transformation layer managing source-to-target mappings
5. Implemented dedicated data_quality.py engine — automatically flags null values, type mismatches, schema deviations; generates automated health reports (data_quality_report.txt)
6. Built Python-based transformation scripts unifying 3 disparate data sources — unit normalization (energy consumption), temporal alignment of weather data with charging session timestamps
7. Designed warehouse as ML-ready for future demand forecasting models; established framework for Airflow DAG-based automated orchestration
8. Built automated reporting tools outputting numeric_summary.csv for immediate visibility into data distributions and station utilization metrics
9. Managed API keys and credentials via environment variables (.env); followed modular coding principles (Single Responsibility) for maintainability
10. Created detailed documentation artifacts: ER diagrams, Data Flow Mappings, Warehouse Table Dictionary — bridging technical and business stakeholder communication
11. Unified fragmented data into single source of truth, enabling weather-to-charging behavior correlation and reducing manual cross-platform analysis effort

---

## Project 2 — Real-Time User Interaction Analytics Pipeline
**Link:** https://github.com/harshalsp0011/realtime-user-analytics

**Core Scope:** End-to-end streaming analytics pipeline for e-commerce — monitoring live user behaviors, identifying funnel drop-off points, and predicting churn risk in real-time for proactive retention.

**Key Concepts:** Streaming/real-time processing, Kafka, Spark Structured Streaming, windowed aggregations, watermarking, ML integration in stream, real-time analytics schema design, containerization, FastAPI ingestion, Streamlit visualization

**Stack:** Python, Apache Kafka, Apache Spark/PySpark, PostgreSQL, Docker, Docker Compose, FastAPI, Streamlit, Random Forest (churn model)

**Details:**
1. Built end-to-end streaming pipeline: live events via FastAPI → Kafka topics → Spark Structured Streaming → ML scoring → PostgreSQL → Streamlit dashboard
2. Implemented sliding time windows and watermarking in PySpark to handle late-arriving events and calculate rolling metrics: conversion rates, session-based event counts
3. Integrated Random Forest churn prediction model directly into stream processing layer — assigns churn probability scores to users as interaction data flows through pipeline
4. Optimized PostgreSQL schema for real-time analytics: tables for event_counts, funnel_summary, churn_predictions supporting rapid dashboard refreshes
5. Built high-frequency Kafka producer simulating live traffic; Spark Streaming Aggregator for windowed KPIs
6. Exposed FastAPI as robust entry point for user events and processed analytics endpoints — enables easy integration with front-end e-commerce platforms
7. Containerized full multi-service environment with Docker: Kafka brokers, Zookeeper, Spark clusters, database — consistent deployment across environments
8. Built schema validation at ingestion layer ensuring high data quality and system reliability under varying load
9. Developed interactive Streamlit dashboard: live heatmaps of event trends, conversion funnel visualizations, user-level churn probability distributions for executive decision-making
10. Reduced latency between user interaction and churn risk identification to seconds — enabling shift from reactive daily reporting to proactive real-time intervention

---

## Project 3 — Utility Billing AI — The Agentic Auditor
**Link:** https://github.com/harshalsp0011/utility-billing-ai
**Associated with:** Troy & Banks Inc

**Core Scope:** Intelligent AI data platform that automatically extracts data from utility PDFs, interprets tariff rules via LLMs, recalculates charges, and detects overcharge discrepancies — transforming 2–4 hour manual audits into a minutes-long automated process.

**Key Concepts:** Agentic AI, LLM integration, PDF parsing, unstructured data extraction, ETL pipeline, data validation, audit automation, multi-layered agent architecture, Airflow orchestration, containerization

**Stack:** Python, Docker, Apache Airflow, AWS infrastructure, FastAPI, LLMs (OpenAI/Anthropic APIs), Camelot, pdfplumber

**Details:**
1. Built multi-layered agent architecture with distinct agents for parsing, calculation, and discrepancy reporting — high modularity and independent task handling
2. Automated pipeline: PDF ingestion → agentic text/table extraction → LLM rule extraction → validation/recalculation → audit report generation
3. Utilized LLMs to automate extraction and interpretation of Service Classification (SC) codes and seasonal surcharge rules from dense, non-transparent tariff documents
4. Implemented complex billing formulas and validation logic derived directly from official tariff documents using official recalculation algorithms
5. Built automated reporting generating detailed audit summaries — calculated vs. actual bill amounts for easy human auditor verification
6. Integrated backend APIs with user-friendly frontend UI — non-technical users can upload documents and view audit results instantly
7. Leveraged Docker Compose for consistent service orchestration; Apache Airflow for managing complex multi-step auditing workflows
8. Transformed 2–4 hour manual audit task into minutes; achieved ~60% reduction in labor costs through automated unstructured financial data pipeline
9. 200+ hours of research, development, testing, and deployment — moved from conceptual architecture to full-stack production-ready solution

---

## Project 4 — Job Market Analysis Using LinkedIn Data
**Link:** https://github.com/harshalsp0011/job-market-analysis-using-linkedIn-data

**Core Scope:** Scalable distributed data pipeline for analyzing large unstructured LinkedIn job posting data — converting raw files into skill-demand and hiring-trend insights using Hadoop/Spark ecosystem.

**Key Concepts:** Distributed computing, Hadoop/HDFS, Spark/PySpark, data ingestion, distributed transformations, cluster orchestration, EDA, containerization, YARN resource management

**Stack:** Python (PySpark, Jupyter), Java (Hadoop FileSystem API), Apache Hadoop (HDFS), Apache YARN, Apache Spark, Docker, Docker Compose, CSV, Git

**Details:**
1. Implemented Java-based HDFS ingestion utility (DataIngestion.java) and shell script (script.sh) for command-line ingestion and validation
2. Engineered distributed pipeline: CSV files → HDFS storage → Spark jobs on YARN → distributed transformations → analytical output in Jupyter notebooks
3. Used Spark transformation patterns (flatMap, map, reduceByKey) for scalable text analysis and word-count-style skill aggregation
4. Added ingestion validation via HDFS checks (hdfs dfs -test -e) confirming file upload success and pipeline operational integrity
5. Orchestrated full cluster with Docker Compose — single command startup, reproducible environment for demos and testing
6. Enabled cluster monitoring via HDFS and YARN web interfaces (port 9870, 8088, 8042) for storage and job execution visibility
7. Delivered end-to-end reproducible distributed workflow shifting processing from single-node to Hadoop/Spark-based distributed setup

---

## Project 5 — AI Job Market Insider and Career Advisor
**Link:** https://github.com/harshalsp0011/AI-job-Market-insider-and-Career-Advisor

**Core Scope:** Automated end-to-end multi-agent system that scours job markets, extracts and normalizes technical skills, and generates personalized career roadmaps — reducing hours of manual research to seconds.

**Key Concepts:** Multi-agent architecture, Agent2Agent (A2A), parallel agents, sequential agents, LLM synthesis, skill normalization, unstructured text processing, API tool integration, observability, retry logic

**Stack:** Python 3.10+, Google Gemini 2.5 Flash Lite (GenAI SDK), Google Agent Development Kit (ADK)

**Details:**
1. Built ParallelAgent for concurrent market scouring and SequentialAgent for orchestrated skill normalization — specialized agent roles in pipeline
2. Implemented Agent2Agent (A2A) distributed architecture enabling local agents to communicate with remote trend_server.py microservice
3. Integrated APIs as tools grounding agent responses in real-world market data during execution
4. Built normalization logic cleaning and consolidating technical terms (e.g., "PyTorch" / "pytorch") ensuring integrity of trend analysis
5. Leveraged LLMs to interpret conflicting information and synthesize actionable insights from unstructured job description text
6. Integrated LoggingPlugin for real-time observability into complex agent interactions and system health
7. Implemented retry logic and robust error handling managing API dependencies and ensuring multi-agent pipeline stability
8. Progressed from research notebook (Multi_agent_system.ipynb) to standalone pipeline execution framework (main_pipeline.py)
9. Reduced job market research time from hours to seconds; delivers data-driven project-specific career advice
10. Designed with microservices patterns — expandable to online model retraining and session-based recommendation engines

---

## Project 6 — Meta-Agent Factory System
**Link:** https://github.com/harshalsp0011/the-meta-agent-system

**Core Scope:** End-to-end pipeline that converts plain-language requirements into working multi-agent systems — automating strategy design, blueprinting, code generation, and execution through a human-in-the-loop workflow.

**Key Concepts:** Multi-agent architecture, LangGraph stateful orchestration, LangChain, blueprint-driven generation, model routing with fallbacks, MCP tool validation, human-in-the-loop, approval gates, dynamic code execution, agentic AI

**Stack:** Python 3.10+, Google Gemini (google-genai), Google ADK, LangChain, LangGraph, Streamlit, Pydantic, MCP (mcp==1.23.3), asyncio, aiosqlite, SQLAlchemy, python-dotenv

**Details:**
1. Implemented 3-layer agent architecture: Consultant (strategy), Architect (blueprint), Builder (code generation) — with explicit human approval gates between layers
2. Used LangGraph for stateful orchestration with role-based specialization, iterative refinement loops, and fallback model routing for reliability and cost/latency optimization
3. Built 4-step Streamlit orchestration UI for human-in-the-loop workflow: requirement input → strategy selection → blueprint approval → agent execution
4. Implemented MCP-based tool validation in LangChain workflow — prevents agents from calling non-existent tools
5. Applied role-specific LLM prompting for strategy, architecture, and code synthesis with blueprint constraints and syntax checks
6. File-based artifact persistence (blueprint.json + agent.py) per agent; optional SQLAlchemy for DB-backed persistence
7. Built model routing with fallbacks (src/model_router.py) — handles model unavailability, optimizes cost and latency
8. Delivers repeatable agent-generation pipeline with approval-driven design; documented MCP-track metrics in docs/MCP_INTEGRATION.md
9. Includes .env-based secret handling, artifact traceability, no-restart dynamic execution via importlib

---

## Project 7 — E-Commerce Product Recommendation System
**Link:** https://github.com/harshalsp0011/E-Commerce-product-recommendation-system

**Core Scope:** End-to-end recommendation engine converting raw e-commerce interaction data (view, add-to-cart, transaction) into personalized product recommendations using collaborative filtering — served via production-style REST API.

**Key Concepts:** Collaborative filtering, ALS matrix factorization, implicit feedback, ML model serving, FastAPI, Streamlit, Docker, sparse matrix, recommendation scoring, MLOps-ready design

**Stack:** Python, Pandas, NumPy, SciPy sparse matrices, implicit ALS, Joblib, FastAPI, Pydantic, Uvicorn, Streamlit, Docker, Git/GitHub

**Details:**
1. Implemented implicit-feedback Collaborative Filtering using ALS latent-factor matrix factorization — infers user/item vectors, ranks unseen items by predicted affinity
2. Built interaction-weighting logic for implicit feedback: view=1, addtocart=3, transaction=5 → sparse user-item matrix → ALS training → artifact export (.joblib)
3. Exposed production-style REST endpoints via FastAPI (/recommendations, /users) with Pydantic typed response contracts, unknown-user rejection (404), exception-safe inference (500 fallback), and score normalization
4. Used sparse linear algebra and implicit library for efficient handling of large interaction volumes — low-latency top-N recommendations suitable for API serving
5. Integrated Streamlit as lightweight consumer app for manual QA, demos, and stakeholder-facing interaction testing
6. Containerized with Docker (python:3.10-slim) — installed system dependencies (gcc, libgomp1) for ML runtime; Uvicorn-hosted endpoints for local/cloud deployment
7. Followed modular project structure: separated model artifacts from serving code, strict API schema definitions, controlled dependency management via requirements.txt
8. Delivered complete recommender platform enabling improved user engagement experiments, easier A/B testing setup, and practical MLOps-ready recommendation serving