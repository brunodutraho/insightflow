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
* Marketing data integration (APIs)
* Data processing pipelines (Python + Pandas)
* Analytical database modeling (PostgreSQL)
* Interactive dashboards

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

## 🚀 Getting Started

### Clone the repository

```bash
git clone https://github.com/brunodutraho/insightflow.git
cd insightflow
```

### Run with Docker (coming soon)

```bash
docker-compose up
```

---

## 📈 Roadmap

### MVP

* [ ] User authentication
* [ ] Client management
* [ ] Instagram API integration
* [ ] Basic analytics dashboard

### Next Steps

* [ ] Facebook Ads integration
* [ ] Advanced analytics
* [ ] Automation (email/WhatsApp)
* [ ] Machine learning insights

---

## 🎯 Project Goals

This project demonstrates:

* Data engineering concepts
* Backend development with FastAPI
* Data modeling (OLTP + Analytics)
* Business-oriented data analysis
* Dashboard development

---

## 📌 Status

🚧 MVP in development

---

## 👤 Author

**Bruno Dutra**

* LinkedIn: https://www.linkedin.com/in/brunodutraho
* Portfolio: https://bruno-dutra-portfolio.vercel.app

---

## ⭐ Final Note

Data well analyzed leads to better decisions.
