<div align="center">

## ☁️ CloudWarden

### AI-Powered Kubernetes Cost Governance Platform

Monitor. Forecast. Detect. Optimize — for your Kubernetes clusters.

![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Dashboard-Streamlit-FF4B4B?logo=streamlit&logoColor=white)
![FastAPI](https://img.shields.io/badge/API-FastAPI-009688?logo=fastapi&logoColor=white)
![Docker](https://img.shields.io/badge/Container-Docker-2496ED?logo=docker&logoColor=white)
![Kubernetes](https://img.shields.io/badge/Deploy-Kubernetes-326CE5?logo=kubernetes&logoColor=white)
![Groq](https://img.shields.io/badge/AI-Groq%20Llama%203.3%2070B-F55036)
![CI/CD](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-2088FF?logo=githubactions&logoColor=white)
![ArgoCD](https://img.shields.io/badge/GitOps-ArgoCD-EF7B4D?logo=argo&logoColor=white)
![Prometheus](https://img.shields.io/badge/Monitoring-Prometheus-E6522C?logo=prometheus&logoColor=white)
![Grafana](https://img.shields.io/badge/Dashboard-Grafana-F46800?logo=grafana&logoColor=white)
![OpenCost](https://img.shields.io/badge/FinOps-OpenCost-00C7B7)
![Slack](https://img.shields.io/badge/Alerts-Slack-4A154B?logo=slack)

</div>

---

## Overview

CloudWarden is a full-stack **FinOps platform** for Kubernetes. It pulls real-time namespace-level cost data from **OpenCost**, persists it for trend analysis, and layers on machine learning and an LLM copilot to help engineering teams understand *where* cluster spend is going, *why* it's changing, and *what* to do about it.

It ships as a Streamlit dashboard for humans, a FastAPI service for machines, a GitOps deployment pipeline via Argo CD, and a Prometheus/Grafana monitoring stack — all defined as code in this repo.

---

## ✨ Features

### Implemented

| Area | What it does |
|---|---|
| 💰 **Cost Collection** | Pulls live namespace allocation data from the OpenCost API and stores time-series history in SQLite |
| 🤖 **AI Analysis & Copilot** | Uses Groq's Llama 3.3 70B to generate structured cost reports (executive summary, CPU/memory/storage/network breakdown, savings recommendations) and answer free-form questions about the cluster |
| 📈 **Cost Forecasting** | Predicts next-period namespace cost using a scikit-learn Linear Regression model trained on historical data |
| 🚨 **Anomaly Detection** | Flags namespaces whose spend falls outside a 2-standard-deviation band, with a 3-tier (Healthy / Warning / Critical) cluster health status |
| 📊 **Streamlit Dashboard** | 6-page UI — Dashboard, AI Copilot, Anomaly Detection Center, Forecast, History, Settings — with Plotly charts and CSV export |
| 🔐 **Authentication** | bcrypt-hashed login/registration backed by SQLite |
| 📄 **PDF Reporting** | Exports AI-generated cost reports as PDF via ReportLab |
| 🌐 **REST API** | FastAPI service exposing `/costs`, `/forecast`, and a Prometheus-compatible `/metrics` endpoint (request counters + latency histograms) |
| 🐳 **Containerized** | Dockerfile + docker-compose (dashboard, API, Prometheus, Grafana) for local/single-node deployment |
| ☸️ **Kubernetes-Ready** | Deployment, Service, and Ingress manifests for both the dashboard and the API, with readiness/liveness probes and CPU/memory resource limits |
| ❤️ **Health Probes** | Kubernetes readiness and liveness probes on every deployed container |
| 🚀 **GitOps Deployment** | Argo CD `Application` manifest with automated sync, self-heal, and pruning against the `k8s/` manifests |
| 📊 **Monitoring** | Prometheus scrape config (+ optional Prometheus Operator `ServiceMonitor`) and a provisioned Grafana dashboard for request rate and p95 latency |
| ⚙️ **CI/CD + GitOps** | GitHub Actions pipeline — dependency install, pytest, flake8 lint, Bandit security scan, Docker image build & push to Docker Hub, Argo CD sync trigger, Slack notifications for both build and deployment stages |

### Roadmap

These are designed for but not yet implemented — listed here intentionally so the scope is clear:

- [ ] Policy engine for defining cost/risk rules
- [ ] Automated remediation with verification and rollback
- [ ] Slack-based *approval* workflow for remediation actions (Slack today only sends notifications, not approvals)
- [ ] Structured audit logging

> **Note on "production":** the Kubernetes, Argo CD, and Prometheus/Grafana configuration in this repo is written to production standards (probes, resource limits, GitOps sync, monitoring), but this is a portfolio project — it isn't currently serving live production traffic on a running cluster unless you deploy it yourself.

---

## 🏗️ Architecture

**Runtime data flow:**

```
                     ┌────────────────────┐
                     │   Kubernetes Cluster │
                     │   (workloads, pods)  │
                     └──────────┬──────────┘
                                │
                                ▼
                        ┌───────────────┐
                        │   OpenCost    │
                        │  Allocation   │
                        │      API      │
                        └───────┬───────┘
                                │
                                ▼
                     ┌─────────────────────┐
                     │   CostCollector     │──────► SQLite (cost history)
                     └──────────┬──────────┘
                                │
              ┌─────────────────┼─────────────────┐
              ▼                 ▼                 ▼
     ┌─────────────────┐ ┌─────────────┐ ┌──────────────────┐
     │  CostPredictor   │ │  Anomaly    │ │  AI Agent (Groq   │
     │ (Linear Reg.)    │ │  Detector   │ │  Llama 3.3 70B)   │
     └────────┬─────────┘ └──────┬──────┘ └─────────┬─────────┘
              │                  │                   │
              └──────────────────┼───────────────────┘
                                  ▼
                  ┌────────────────────────────────┐
                  │  Streamlit Dashboard  │  FastAPI │
                  │  (human interface)    │  (/costs,│
                  │                       │  /forecast│
                  │                       │  /metrics)│
                  └────────────────────────────────┘
```

**Build & deployment flow:**

```
Developer
   │
   ▼
Git Commit ──► GitHub Repository
                    │
                    ▼
              GitHub Actions
                    │
    ┌───────────────┼───────────────┐
    ▼                ▼               ▼
Unit Tests      Lint (flake8)   Security Scan (Bandit)
    │                │               │
    └────────────────┼───────────────┘
                      ▼
               Docker Build & Push
                      │
                      ▼
                  Docker Hub
                      │
                      ▼
              Argo CD (GitOps sync)
                      │
                      ▼
              Kubernetes Cluster
                      │
         ┌────────────┼────────────┐
         ▼            ▼            ▼
    CloudWarden   Prometheus    Grafana
    Dashboard/API  (scrapes    (visualizes
                   /metrics)    metrics)
                      │
                      ▼
              Slack Notification
              (build + deploy status)
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.12 |
| Cost data source | OpenCost |
| Dashboard | Streamlit, Plotly |
| API | FastAPI, Uvicorn |
| AI / LLM | Groq (Llama 3.3 70B) |
| ML | scikit-learn, pandas, NumPy |
| Database | SQLite |
| Auth | bcrypt |
| Reporting | ReportLab (PDF) |
| Monitoring | Prometheus, Grafana |
| GitOps | Argo CD |
| Notifications | Slack |
| Containers | Docker, docker-compose |
| Container Registry | Docker Hub |
| Orchestration | Kubernetes (Deployment, Service, Ingress) |
| CI/CD | GitHub Actions, flake8, Bandit |

---

## 📁 Project Structure

```
CloudWarden/
├── agent/
│   ├── app.py                 # CLI entry point — headless analysis run
│   ├── dashboard.py            # Streamlit multi-page dashboard
│   ├── api.py                  # FastAPI service (/costs, /forecast, /metrics)
│   ├── ai_agent.py              # Groq LLM client — analysis & chat
│   ├── analyzer.py             # Orchestrates collection + recommendations
│   ├── collector.py             # Pulls & persists OpenCost allocation data
│   ├── opencost_client.py        # OpenCost HTTP client
│   ├── predictor.py             # Linear Regression cost forecasting
│   ├── anomaly_detector.py       # Statistical (2σ) anomaly detection
│   ├── recommender.py           # Builds AI recommendation prompts
│   ├── incident_ai.py            # AI-based incident root-cause analysis
│   ├── database.py              # SQLite persistence layer
│   ├── auth.py / login.py / register.py   # bcrypt authentication
│   ├── pdf_report.py             # ReportLab PDF export
│   ├── config.py                # Environment-driven configuration
│   ├── Dockerfile / docker-compose.yml
│   └── requirements.txt
├── k8s/
│   ├── deployment.yaml          # Dashboard: probes + resource limits
│   ├── service.yaml
│   ├── ingress.yaml
│   ├── api-deployment.yaml       # FastAPI/metrics service: probes + resource limits
│   └── api-service.yaml
├── argocd/
│   └── application.yaml         # Argo CD Application — automated sync, self-heal, prune
├── monitoring/
│   ├── prometheus.yml            # Static scrape config (docker-compose)
│   ├── servicemonitor.yaml       # Prometheus Operator scrape config (in-cluster)
│   ├── grafana-dashboard.json     # Request rate + p95 latency dashboard
│   ├── grafana-datasource.yml     # Auto-provisions Prometheus as a data source
│   └── grafana-dashboard-provider.yml
├── .github/workflows/
│   └── cloudwarden.yml          # Test, lint, scan, build, push, Argo CD sync, Slack
└── requirements.txt
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.12+
- A running [OpenCost](https://www.opencost.io/) instance (or point `OPENCOST_URL` at one)
- A [Groq API key](https://console.groq.com/) for AI features
- (Optional) A Kubernetes cluster with [Argo CD](https://argo-cd.readthedocs.io/) installed, for GitOps deployment

### 1. Clone & install

```bash
git clone https://github.com/Aman-Ullah-Ansary/CloudWarden.git
cd CloudWarden/agent
pip install -r requirements.txt
```

### 2. Configure environment

Create a `.env` file inside `agent/`:

```env
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=llama-3.3-70b-versatile
OPENCOST_URL=http://localhost:9091
DATABASE_NAME=cloudwarden.db
COST_THRESHOLD=0.30
REFRESH_INTERVAL=60
```

### 3. Run the dashboard

```bash
streamlit run dashboard.py
```

### 4. Run the API (optional)

```bash
uvicorn api:app --reload --port 8000
```

### 5. Run a one-off CLI analysis

```bash
python app.py
```

### Run the full stack locally with Docker

Spins up the dashboard, the API, Prometheus, and Grafana together:

```bash
cd agent
docker build -t cloudwarden:latest .
docker compose up
```

- Dashboard → http://localhost:8503
- API → http://localhost:8000
- Prometheus → http://localhost:9090
- Grafana → http://localhost:3000 (login: `admin` / `admin`, dashboard auto-loads)

### Deploy to Kubernetes directly

```bash
kubectl apply -f k8s/
```

### Deploy via Argo CD (GitOps)

Requires Argo CD installed in the target cluster:

```bash
kubectl apply -f argocd/application.yaml
```

This creates an Argo CD `Application` that watches the `k8s/` folder in this repo and automatically syncs, self-heals, and prunes resources in the `cloudwarden` namespace.

### CI/CD secrets required

For the full GitHub Actions pipeline (build → push → deploy → notify) to run end to end, configure these repository secrets:

| Secret | Used for |
|---|---|
| `DOCKER_USERNAME`, `DOCKER_PASSWORD` | Docker Hub image push |
| `ARGOCD_SERVER`, `ARGOCD_USERNAME`, `ARGOCD_PASSWORD` | Triggering Argo CD sync from CI |
| `SLACK_WEBHOOK` | Build and deployment notifications |

---

## 🔄 CI/CD & GitOps Pipeline

- GitHub Actions automates dependency installation, testing, linting, security scanning, Docker image creation, and image publishing.
- Docker images are pushed to Docker Hub on every push to `main`.
- A dedicated `deploy` job logs into Argo CD and triggers `argocd app sync`, then waits for the sync to complete.
- Argo CD continuously watches the `k8s/` manifests in this repository and can also self-heal drift outside of CI.
- Kubernetes performs rolling updates using the configured readiness and liveness probes.
- Slack notifications fire separately for build status and deployment status.

---

## 📷 Screenshots

_Add screenshots here to make this section land — a README with real images converts far better than a bullet list:_

- Streamlit Dashboard
- AI Copilot
- Cost Forecast
- Anomaly Detection
- GitHub Actions run
- Argo CD sync view
- Grafana dashboard

---

## 🤝 Contributing

Contributions are welcome. Please open an issue to discuss significant changes before submitting a pull request.

## 📄 License

MIT L.

---

<div align="center">
<sub>Built by <a href="https://github.com/Aman-Ullah-Ansary">Aman Ullah Ansary</a></sub>
</div>
