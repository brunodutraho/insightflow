# 🚀 InsightFlow

**Turn marketing data into decisions.**

InsightFlow is a marketing analytics SaaS platform designed to centralize data from multiple marketing channels and transform it into actionable insights.

This project simulates a real-world data environment by combining data engineering, analytics, and modern web development practices.

---

## 📊 Overview

InsightFlow enables marketing professionals and businesses to:

* Track campaign performance
* Analyze engagement and growth metrics
* Monitor conversions and ROI
* Visualize data through interactive dashboards

---

## 🧠 Key Features (MVP)

* Multi-user system (Admin, Managers, Clients)
* Multi-tenant architecture (data isolation per client)
* Client management with subscription-based limits
* Marketing data modeling and analytics endpoints
* Data processing pipelines (Python + Pandas)
* Analytical database modeling (PostgreSQL)
* Secure API with JWT authentication and RBAC

---

## 🏗️ Architecture

```text
APIs (Instagram, Facebook, Ads)
        ↓
Data Collection (Python)
        ↓
Data Processing (Pandas)
        ↓
PostgreSQL (Database)
        ↓
FastAPI (Backend API)
        ↓
Next.js (Frontend)
```

---

## 🧰 Tech Stack

### Backend

* Python
* FastAPI
* PostgreSQL
* SQLAlchemy
* Pydantic Settings (env management)
* JWT Authentication (RBAC)

### Data

* Pandas
* ETL Pipelines

### Frontend

* Next.js
* React
* Tailwind CSS

### Infrastructure

* Docker
* Git & GitHub

---

## 📁 Project Structure

```text
insightflow/
│
├── backend/       # FastAPI application
├── frontend/      # Next.js application
├── docker/        # Docker and docker-compose configs
├── docs/          # Project documentation
└── README.md
```

---

## 🧱 Backend Highlights

The backend implements a multi-tenant SaaS architecture with:

### 👤 Role-Based Access Control (RBAC)
* Admin → full system access
* Manager (Gestor) → manages their own clients
* Client → access restricted to their own data

---

## 🏢 Multi-Tenant Data Model

````
User (role)
   ↓
Client (owned by manager)
   ↓
Insight (data records)

````
---

## 📊 Analytics Features
* Insights grouped by category
* Time-series aggregation
* Data filtering and pagination
* SQL-based aggregations (GROUP BY, COUNT)

---

## 💳 Subscription System (MVP)
* Plan-based client limits
* Free / Pro / Growth structure
* Backend-enforced limits (ready for billing integration)

---

## 🔐 Security
* JWT authentication
* Role-based authorization
* Data isolation using ownership validation

---

## 🚀 API Features
### 🔹 Clients

````
</> http
POST   /clients
GET    /clients
GET    /clients/{id}
PUT    /clients/{id}
DELETE /clients/{id}
````
---

### 🔹 Insights

````
</> http
POST   /insights
GET    /insights?client_id=1&limit=10&offset=0&category=finance
PUT    /insights/{id}
DELETE /insights/{id}
````

---

### 🔹 Insights

````
</> http
GET /analytics/insights-by-category
GET /analytics/insights-over-time
GET /analytics/insights-by-user
````
## 🚀 Getting Started

### Clone the repository

```bash
git clone https://github.com/brunodutraho/insightflow.git
cd insightflow
```
### Run backend locally

```bash
uvicorn app.main:app --reload
```

---
### Run with Docker (coming soon)

```bash
docker-compose up
```

---

## 📈 Roadmap

### MVP

* [ ] User authentication (JWT)
* [ ] Role-based access control (RBAC)
* [ ] Client management (multi-tenant)
* [ ] Insight tracking system
* [ ] Analytics endpoints (aggregations)

### Next Steps

* [ ] Meta Ads / Google Ads integration
* [ ] Automated data ingestion (ETL jobs)
* [ ] Interactive dashboard (React / BI tools)
* [ ] Real billing system (Stripe)
* [ ] Advanced analytics & forecasting

---

## 🎯 Project Goals

This project demonstrates:

* Data engineering concepts
* Backend development with FastAPI
* Multi-tenant SaaS architecture
* Data modeling (OLTP + Analytics)
* Business-oriented data analysis
* API design with scalability in mind

---

## 📌 Status

🚧 MVP Backend Complete — Frontend & integrations in progress

---

## 👤 Author

**Bruno Dutra**

* LinkedIn: https://www.linkedin.com/in/brunodutraho
* Portfolio: https://bruno-dutra-portfolio.vercel.app

---

## ⭐ Final Note

Data well analyzed leads to better decisions.
