# 🏛️ ARQUITETURA DETALHADA - InsightFlow

---

## 1. FLUXO DE AUTENTICAÇÃO

```
┌─────────────────────────────────────────────────────────────────┐
│                      FRONTEND (Login Page)                      │
│                                                                 │
│  email: user@example.com                                        │
│  password: ••••••••                                             │
│  [Login Button]                                                 │
└──────────────────────────┬──────────────────────────────────────┘
                           │ POST /auth/login
                           ↓
┌─────────────────────────────────────────────────────────────────┐
│                   BACKEND (Auth Router)                         │
│                                                                 │
│  1. Recebe {email, password}                                   │
│  2. Busca user no BD: db.query(User).filter(email)             │
│  3. Valida: if not user → return 401 "Invalid credentials"     │
│  4. Verifica senha: verify_password(password, user.hashed) │
│  5. Se OK → cria JWT token com {user_id, email, role}         │
└──────────────────────────┬──────────────────────────────────────┘
                           │ Retorna token
                           ↓
┌─────────────────────────────────────────────────────────────────┐
│              FRONTEND (localStorage)                            │
│                                                                 │
│  localStorage.setItem("token", "eyJhbGc...")                   │
│  localStorage.setItem("role", "admin")                         │
│  Redireciona para /admin                                       │
└─────────────────────────────────────────────────────────────────┘
```

---

## 2. FLUXO DE REQUEST COM AUTENTICAÇÃO

```
┌─────────────────────────────────────────────────────────────────┐
│                  FRONTEND - Componente React                    │
│                                                                 │
│  const { data } = api.get('/admin/overview')                   │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ↓
┌─────────────────────────────────────────────────────────────────┐
│              FRONTEND - Axios Service                           │
│                                                                 │
│  axios.create({                                                │
│    headers: {                                                  │
│      Authorization: `Bearer ${localStorage.getItem('token')}`  │
│    }                                                           │
│  })                                                            │
└──────────────────────────┬──────────────────────────────────────┘
                           │
        GET /admin/overview HTTP/1.1
        Authorization: Bearer eyJhbGc...
                           │
                           ↓
┌─────────────────────────────────────────────────────────────────┐
│                  BACKEND - Middleware Chain                     │
│                                                                 │
│  1. CORSMiddleware                                             │
│     ✓ Verifica origem (localhost:3000)                        │
│     ✓ Permite request                                         │
│                                                               │
│  2. ErrorMiddleware                                            │
│     ✓ Pronto para capturar exceções                          │
│                                                               │
│  3. LoggingMiddleware                                          │
│     ✓ Registra: GET /admin/overview - IP: 127.0.0.1          │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ↓
┌─────────────────────────────────────────────────────────────────┐
│               BACKEND - Route Handler                           │
│                                                                 │
│  @router.get("/admin/overview")                               │
│  @require_roles(["admin"])  ← Verifica JWT payload            │
│  def get_admin_overview(db: Session = Depends(get_db)):       │
│      # FastAPI injeta a sessão do BD                          │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ↓
┌─────────────────────────────────────────────────────────────────┐
│                BACKEND - Service Layer                          │
│                                                                 │
│  metrics = metrics_service.get_mrr(db)                        │
│  users = metrics_service.get_total_users(db)                  │
│  health = metrics_service.calculate_health(...)               │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ↓
┌─────────────────────────────────────────────────────────────────┐
│               BACKEND - Database Queries                        │
│                                                                 │
│  SELECT SUM(plans.price) FROM subscriptions ...               │
│  SELECT COUNT(*) FROM users WHERE ...                         │
│  SELECT ... FROM clients WHERE last_activity ...             │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ↓
┌─────────────────────────────────────────────────────────────────┐
│               POSTGRESQL - Returns Results                      │
│                                                                 │
│  Rows aggregated and passed back up the chain                 │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ↓
┌─────────────────────────────────────────────────────────────────┐
│            BACKEND - JSON Response                              │
│                                                                 │
│  HTTP 200 OK                                                   │
│  {                                                              │
│    "users": { "total": 245, ... },                             │
│    "revenue": { "mrr": 12500, ... },                           │
│    "goal": { "target": 15000, ... }                            │
│  }                                                              │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ↓
┌─────────────────────────────────────────────────────────────────┐
│            FRONTEND - React State Update                        │
│                                                                 │
│  setData(response.data)                                        │
│  Component rerenders com novos valores                         │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ↓
┌─────────────────────────────────────────────────────────────────┐
│            FRONTEND - Browser Render                            │
│                                                                 │
│  <StatCard value={245} />                                      │
│  <MRRChart data={...} />                                       │
│  <HealthScoreCard score={87} />                                │
│  ... 9 outros componentes ...                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 3. ARQUITETURA DE CAMADAS (Layer Architecture)

```
┌───────────────────────────────────────────────────────────────┐
│                    PRESENTATION LAYER                         │
│                   (Frontend - React/Next)                     │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │ Admin Dashboard Components                              │ │
│  │ ┌──────┬──────┬──────────┬────────┬──────────┐          │ │
│  │ │Stats │Charts│HealthCard│MRRGoal │Alerts   │          │ │
│  │ │Cards │      │          │Tracker │+ Insights│          │ │
│  │ └──────┴──────┴──────────┴────────┴──────────┘          │ │
│  └────────────────────┬────────────────────────────────────┘ │
└────────────────────────┼──────────────────────────────────────┘
                         │ HTTP Request
                         │ (Axios with JWT)
┌────────────────────────┼──────────────────────────────────────┐
│                        ↓                                        │
│                    API LAYER                                   │
│                 (Backend - FastAPI)                            │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │ Routers (13 files)                                      │ │
│  │ /auth /users /admin /subscriptions /plans /coupons... │ │
│  └──────────────────────────────┬──────────────────────────┘ │
│                                 │ Delegates to
│  ┌────────────────────────┬─────┴──────┬──────────────────────┐
│  │                        │            │                      │
│  ↓                        ↓            ↓                       │
│┌─────────────────┐ ┌──────────────┐ ┌──────────────┐         │
││ Middlewares     │ │ Services     │ │ Schemas      │         │
││ - CORS        │ │ - metrics    │ │ - Pydantic   │         │
││ - Error       │ │ - plan       │ │ - Validation │         │
││ - Logging     │ │ - coupon     │ │              │         │
│└─────────────────┘ └──────────────┘ └──────────────┘         │
│                                                               │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │ Core Utilities                                          │ │
│  │ - security (JWT, password hashing)                      │ │
│  │ - logging (structured logs)                             │ │
│  └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────┬───────────────────────────────────┘
                              │ SQLAlchemy ORM
                              │ (Query Builder)
┌─────────────────────────────┼───────────────────────────────────┐
│                             ↓                                     │
│                      DATABASE LAYER                              │
│                   (PostgreSQL + Alembic)                         │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ Models (15 tables)                                         │ │
│  │ Users | Clients | Subscriptions | Plans | Coupons |...   │ │
│  │                                                            │ │
│  │ Migrations (Alembic versions/)                            │ │
│  │ Schema versioning and rollback capability                │ │
│  └────────────────────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────────────┘
```

---

## 4. FLUXO DO ADMIN DASHBOARD

```
                   ┌─────────────────────────────────┐
                   │   Admin acessa /admin            │
                   │   Browser loads page.tsx         │
                   └────────────────┬──────────────────┘
                                    │
                                    ↓
                   ┌─────────────────────────────────┐
                   │   useEffect [] é disparado       │
                   │   fetchData() inicia             │
                   └────────────────┬──────────────────┘
                                    │
         ┌──────────────────────────┼──────────────────────────┐
         │                          │                          │
         ↓                          ↓                          ↓
    GET /admin/      GET /admin/mrr-    GET /admin/at-risk-
    overview         history            clients
         │                │                │
         └──────────────────┼──────────────┘
                           │
                    Promise.all([...])
                    Aguarda 5 requests
                           │
         ┌─────────────────┼─────────────────┐
         ↓                 ↓                 ↓
    [data]           [mrrHistory]      [atRisk]
    state updated    state updated     state updated
         │                │                │
         └────────────┬────┴────┬──────────┘
                      │         │
                      ↓         ↓
        Frontend Re-Render Triggered
                      │
         ┌────────────┼────────────┬────────────────┐
         │            │            │                │
         ↓            ↓            ↓                ↓
    HealthScore  MRRChart  MRRGoalCard  SmartAlert
    Calculation  render    render       render
         │            │            │                │
         └────────────┼────────────┴────────────────┘
                      │
                      ↓
         Dashboard Completo Renderizado
    ┌─────────────────────────────────────┐
    │  ┌──────────┐  ┌──────────┐        │
    │  │ Health   │  │MRR Goal  │....    │
    │  │Score: 87 │  │Target:   │...     │
    │  └──────────┘  │15000     │        │
    │                └──────────┘        │
    │  ┌──────────┐  ┌──────────┐        │
    │  │MRRChart  │  │AtRisk    │....    │
    │  │          │  │Clients: 3│...     │
    │  └──────────┘  └──────────┘        │
    │  ... +9 componentes restantes ...  │
    └─────────────────────────────────────┘
                      │
                60 segundos depois
                      │
                      ↓
           Re-fetch automático dispara
           (interval set em useEffect)
```

---

## 5. MODELO DE DADOS - Relacionamentos

```
┌──────────────────┐
│     USERS        │
├──────────────────┤
│ id (PK)          │
│ email (unique)   │
│ hashed_password  │
│ role             │◄──┐
│ last_login       │   │ Manager-to-user
│ manager_id (FK)  │───┴─ hierarchy (self-ref)
│ client_id (FK)   ├──────┐
│ created_at       │      │
└──────────────────┘      │ "Um user
                          │  pertence a"
                    ┌──────▼──────────┐
                    │    CLIENTS      │
                    ├─────────────────┤
                    │ id (PK)         │
                    │ name            │
                    │ owner_id (FK)   │
                    │ created_at      │
                    │ last_activity_at│
                    └────────┬────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
        ↓                    ↓                    ↓
┌──────────────────┐ ┌──────────────────┐ ┌──────────────┐
│ SUBSCRIPTIONS    │ │ AD_ACCOUNTS      │ │ AD_METRICS   │
├──────────────────┤ ├──────────────────┤ ├──────────────┤
│ id (PK)          │ │ id (PK)          │ │ id (PK)      │
│ user_id (FK)─────┼─┤ client_id (FK)──┼─│ client_id    │
│ plan_id (FK)     │ │ platform         │ │ (FK)         │
│ created_at       │ │ account_id       │ │ impressions  │
│ canceled_at      │ │ access_token     │ │ clicks       │
│ is_active        │ │                  │ │ spend        │
└────────┬─────────┘ └──────────────────┘ │ date         │
         │                                 └──────────────┘
         │
         ├──────────┐
         │          │
         ↓          ↓
    ┌────────────┐  ┌──────────────┐
    │    PLANS   │  │   COUPONS    │
    ├────────────┤  ├──────────────┤
    │ id (PK)    │  │ id (PK)      │
    │ name       │  │ code (unique)│
    │ price      │  │ discount_%   │
    │ max_clients│  │ discount_amt │
    │ is_active  │  │ max_uses     │
    │ created_at │  │ used_count   │
    └────────────┘  │ is_active    │
                    │ created_at   │
                    └──────────────┘

┌─────────────────────────────────────┐
│ Outras tabelas especializadas       │
├─────────────────────────────────────┤
│ - social_metrics (followers, etc)   │
│ - marketing_metrics (conversions)   │
│ - communication_metrics (email)     │
│ - insights (texto + categoria)      │
│ - activities (event log)            │
│ - app_config (MRR goals config)     │
│ - user_profiles (nome, empresa)     │
└─────────────────────────────────────┘
```

---

## 6. FLUXO DE CÁLCULO DO HEALTH SCORE

```
Input: OverviewData
  {
    revenue: { mrr_growth: 12, churn_rate: 3 },
    users: { growth_rate: 15 }
  }
           │
           ↓
┌──────────────────────────────────────────┐
│  calculateSaaSHealth(data)               │
├──────────────────────────────────────────┤
│                                          │
│  1. MRR Growth (Peso: 40%)              │
│     12% > 5% ?                          │
│     score += 30                         │
│                                          │
│  2. Churn Rate (Peso: 30%)              │
│     3% < 5% ?                           │
│     score += 20                         │
│                                          │
│  3. User Growth (Peso: 30%)             │
│     15% > 10% ?                         │
│     score += 30                         │
│                                          │
│  Total Score: 30 + 20 + 30 = 80         │
└──────────────────────────────────────────┘
           │
           ↓
┌──────────────────────────────────────────┐
│  Classificação                           │
├──────────────────────────────────────────┤
│                                          │
│  Score 85+ → "Excelente"               │
│   colorClass: from-emerald-500 to-teal │
│                                          │
│  Score 65+ → "Boa"                      │
│   colorClass: from-blue-500 to-indigo   │
│                                          │
│  Score 45+ → "Atenção"                  │
│   colorClass: from-amber-400 to-orange  │
│                                          │
│  Score <45 → "Crítica"                  │
│   colorClass: from-red-500 to-rose      │
│                                          │
└──────────────────────────────────────────┘
           │
           ↓
Output: HealthResult
  {
    score: 80,
    label: "Boa",
    colorClass: "from-blue-500 to-indigo-600"
  }
           │
           ↓
Renderiza no HealthScoreCard
com gradient color grande 80/100
```

---

## 7. FLUXO DE APLICAR CUPOM

```
┌──────────────────────────────────┐
│ Frontend                         │
│ POST /subscriptions/{id}/apply-coupon
│ { code: "WELCOME50" }            │
└────────────────┬─────────────────┘
                 │
                 ↓
┌──────────────────────────────────────────┐
│ Backend - Subscription Route             │
├──────────────────────────────────────────┤
│                                          │
│ 1. Valida user (JWT)                    │
│ 2. Busca subscription                   │
│    subscription = db.query(Subscription)│
│    .filter(id=id, user_id=user.id)     │
│    .first()                             │
│                                          │
│ 3. Busca cupom                          │
│    coupon = db.query(Coupon)            │
│    .filter(code="WELCOME50")            │
│    .first()                             │
│                                          │
└────────────────┬───────────────────────┘
                 │
                 ↓
┌──────────────────────────────────────────┐
│ Validações                               │
├──────────────────────────────────────────┤
│                                          │
│ if not subscription:                    │
│    return 404 "Subscription not found"  │
│                                          │
│ if not coupon or not coupon.is_active:  │
│    return 400 "Invalid coupon"          │
│                                          │
│ if coupon.max_uses and coupon.used_count│
│    >= coupon.max_uses:                  │
│    return 400 "Coupon expired"          │
│                                          │
└────────────────┬───────────────────────┘
                 │
                 ↓
┌──────────────────────────────────────────┐
│ Apply Discount                           │
├──────────────────────────────────────────┤
│                                          │
│ subscription.discount_percent =         │
│    coupon.discount_percent              │
│                                          │
│ subscription.discount_amount =          │
│    coupon.discount_amount               │
│                                          │
│ coupon.used_count += 1                  │
│                                          │
│ db.commit()                             │
│ db.refresh(subscription)                │
│                                          │
└────────────────┬───────────────────────┘
                 │
                 ↓
┌──────────────────────────────────────────┐
│ Response 200 OK                          │
│ {                                        │
│   id: 1,                                │
│   user_id: 5,                            │
│   plan_id: 2,                            │
│   discount_percent: 50,                  │
│   discount_amount: null,                 │
│   is_active: true,                       │
│   created_at: "2024-03-31",             │
│   canceled_at: null                      │
│ }                                        │
└────────────────┬───────────────────────┘
                 │
                 ↓
        Frontend UI Atualizada
        Mostra "Cupom aplicado!"
        Calcula novo preço com desconto
```

---

## 8. ESTRUTURA DO DIRETÓRIO - Completa

```
insightflow/
│
├── backend/
│   ├── alembic/                       # Database migrations
│   │   ├── versions/
│   │   │   ├── 433dd0f722ed_add_plans_table.py
│   │   │   ├── ef381eb5c8d1_add_coupons_table.py
│   │   │   ├── 015dc466f5cc_add_discount_to_subscriptions.py
│   │   │   └── ... 7 mais
│   │   ├── alembic.ini
│   │   ├── env.py                    # Migration config
│   │   └── script.py.mako
│   │
│   ├── app/
│   │   ├── main.py                   # FastAPI app entry
│   │   │
│   │   ├── auth/                     # Authentication
│   │   │   ├── __init__.py
│   │   │   ├── routes.py             # POST /auth/login, register
│   │   │   ├── service.py            # login_user, create_user logic
│   │   │   ├── reauth.py             # POST /auth/reauth for sensitive ops
│   │   │   ├── dependencies.py       # get_current_user, require_roles
│   │   │   ├── utils.py              # hash_password, verify_password, create_access_token
│   │   │   └── schemas.py            # Pydantic models
│   │   │
│   │   ├── models/                   # SQLAlchemy ORM Models
│   │   │   ├── __init__.py           # Exports all models
│   │   │   ├── user.py               # User, UserRole enum
│   │   │   ├── client.py             # Client (company)
│   │   │   ├── subscription.py       # Subscription (with plan_id)
│   │   │   ├── plan.py               # Plan (free, basic, pro, enterprise)
│   │   │   ├── coupon.py             # Coupon (discounts)
│   │   │   ├── activity.py           # ActivityItem (event log)
│   │   │   ├── app_config.py         # AppConfig (global settings like MRR goal)
│   │   │   ├── ad_metric.py          # AdMetric
│   │   │   ├── social_metric.py      # SocialMetric
│   │   │   ├── marketing_metric.py   # MarketingMetric
│   │   │   ├── communication_metric.py
│   │   │   ├── insight.py            # Insight
│   │   │   ├── user_profile.py       # UserProfile
│   │   │   └── ... más
│   │   │
│   │   ├── routers/                  # API Routes (Endpoints)
│   │   │   ├── __init__.py
│   │   │   ├── auth_routes.py        # /auth/...
│   │   │   ├── user_routes.py        # /users/... GET /users/me
│   │   │   ├── admin_routes.py       # /admin/... (14 endpoints!)
│   │   │   ├── subscription_routes.py # /subscriptions/...
│   │   │   ├── client_routes.py      # /clients/...
│   │   │   ├── analytics_routes.py   # /analytics/...
│   │   │   ├── health.py             # GET /health
│   │   │   └── ... outros
│   │   │
│   │   ├── services/                 # Business Logic
│   │   │   ├── __init__.py
│   │   │   ├── metrics_service.py    # ⭐ MRR, churn, health, growth
│   │   │   ├── plan_service.py       # Plan CRUD
│   │   │   ├── coupon_service.py     # Coupon CRUD
│   │   │   ├── subscription_service.py # apply_coupon, cancel_subscription
│   │   │   ├── user_service.py       # User operations
│   │   │   ├── admin_service.py      # Admin utilities
│   │   │   └── ... mais
│   │   │
│   │   ├── schemas/                  # Pydantic Validation
│   │   │   ├── __init__.py
│   │   │   ├── user_schema.py
│   │   │   ├── user_admin.py
│   │   │   ├── client.py
│   │   │   ├── analytics_schema.py
│   │   │   └── ... mas
│   │   │
│   │   ├── middlewares/              # HTTP Interceptors
│   │   │   ├── __init__.py
│   │   │   ├── error_middleware.py   # Error handling
│   │   │   └── logging_middleware.py # Request logging
│   │   │
│   │   ├── database/                 # Database Setup
│   │   │   ├── __init__.py
│   │   │   ├── database.py           # SessionLocal, get_db
│   │   │   ├── base.py               # Base class for models
│   │   │   └── init_db.py            # DB initialization
│   │   │
│   │   ├── core/                     # Core Utilities
│   │   │   ├── __init__.py
│   │   │   ├── security.py           # Password hashing functions
│   │   │   └── logging_config.py     # Structured logging
│   │   │
│   │   ├── config/                   # Configuration
│   │   │   ├── __init__.py
│   │   │   └── settings.py           # Settings from .env
│   │   │
│   │   └── scripts/                  # Utility Scripts
│   │       ├── __init__.py
│   │       ├── seed_plans.py         # Create default plans
│   │       ├── create_subscription.py
│   │       └── migrate_subscriptions.py
│   │
│   ├── requirements.txt              # Python dependencies
│   ├── alembic.ini                   # Alembic config
│   ├── Dockerfile                    # Docker container
│   └── .env                          # Environment variables
│
├── frontend/
│   ├── src/
│   │   ├── app/                      # Next.js App Router
│   │   │   ├── globals.css           # Global styles
│   │   │   ├── layout.tsx            # Root layout
│   │   │   ├── page.tsx              # Home page
│   │   │   ├── providers.tsx         # React providers
│   │   │   │
│   │   │   ├── (dashboard)/          # User dashboard
│   │   │   │   ├── layout.tsx
│   │   │   │   ├── page.tsx
│   │   │   │   └── users/
│   │   │   │
│   │   │   ├── (admin)/              # ⭐ NEW Admin dashboard
│   │   │   │   ├── layout.tsx        # Layout with collapsible sidebar
│   │   │   │   ├── page.tsx          # Main dashboard page
│   │   │   │   ├── components/       # 12 custom components
│   │   │   │   │   ├── Sidebar.tsx       # Responsive navigation
│   │   │   │   │   ├── StatCard.tsx      # Metric card with trend
│   │   │   │   │   ├── MRRChart.tsx      # Line chart (recharts)
│   │   │   │   │   ├── HealthScoreCard.tsx # 0-100 health score
│   │   │   │   │   ├── MRRGoalCard.tsx   # MRR target tracker
│   │   │   │   │   ├── AtRiskClients.tsx # Churn warnings
│   │   │   │   │   ├── RecentActivityTimeline.tsx # Event stream
│   │   │   │   │   ├── LiveSessionsCard.tsx # Active users now
│   │   │   │   │   ├── NewUsersCard.tsx # New registrations
│   │   │   │   │   └── SmartIntelligence.tsx # AI alerts + insights
│   │   │   │   ├── lib/              # Utility functions
│   │   │   │   │   ├── analytics.ts  # Insight engine
│   │   │   │   │   └── healthScore.ts # Health calculation
│   │   │   │   ├── plans/            # Plan management
│   │   │   │   │   └── page.tsx
│   │   │   │   ├── coupons/          # Coupon management
│   │   │   │   │   └── page.tsx
│   │   │   │   └── users/            # More admin pages
│   │   │   │
│   │   │   ├── (login)/              # Login page
│   │   │   │   └── page.tsx
│   │   │   │
│   │   │   └── (register)/           # Register page
│   │   │       └── page.tsx
│   │   │
│   │   ├── components/               # Shared React components
│   │   │   ├── dashboard/
│   │   │   │   ├── ReauthModal.tsx   # Password confirmation modal
│   │   │   │   ├── Navbar.tsx
│   │   │   │   ├── Sidebar.tsx
│   │   │   │   └── ... mais
│   │   │   └── Landing/
│   │   │
│   │   ├── hooks/                    # Custom React hooks
│   │   │   ├── useAuth.ts            # Auth context hook
│   │   │   ├── useUser.ts            # User data hook
│   │   │   └── useAdminUsers.ts
│   │   │
│   │   ├── services/                 # API integration
│   │   │   ├── api.ts                # Axios instance with JWT
│   │   │   ├── auth.service.ts       # login, register, reauth
│   │   │   └── dashboard.service.ts  # Admin API calls
│   │   │
│   │   ├── lib/                      # Utilities
│   │   │   └── auth.ts               # Auth helpers
│   │   │
│   │   ├── types/                    # TypeScript types
│   │   │   └── dashboard.ts
│   │   │
│   │   └── utils/                    # Helper functions
│   │       └── auth.ts
│   │
│   ├── public/                       # Static assets
│   │
│   ├── .env.local                    # Environment variables
│   ├── .gitignore
│   ├── package.json                  # Dependencies
│   ├── tsconfig.json                 # TypeScript config
│   ├── tailwind.config.js            # Tailwind CSS config
│   ├── next.config.ts                # Next.js config
│   ├── middleware.ts                 # Next.js middleware
│   └── eslint.config.mjs             # ESLint config
│
├── DOCUMENTACAO.md                   # 📚 Full documentation (this file)
├── RESUMO_EXECUTIVO.md              # 📋 Executive summary
├── docker-compose.yml                # Docker orchestration
├── README.md                         # Project readme
└── .env                              # Root env file
```

---

## 9. CI/CD PIPELINE (Para o futuro)

```
┌──────────────────────────────────────────────────────────┐
│                 Developer pushes code                    │
│                 git push origin main                     │
└────────────────────────┬─────────────────────────────────┘
                         │
                         ↓
┌──────────────────────────────────────────────────────────┐
│           GitHub Actions Triggered                       │
│                                                          │
│  1. Lint (ESLint + Prettier)                            │
│  2. Type Check (TypeScript compiler)                    │
│  3. Test Backend (pytest)                              │
│  4. Test Frontend (Jest)                               │
└────────────────────────────┬─────────────────────────────┘
                             │
                    ┌────────┴────────┐
                    │                 │
                Passed?             Failed?
                    │                 │
                    ↓                 ↓
            ┌─────────────┐    Notificar Dev
            │  Build      │    Bloqueia merge
            │  Docker     │
            │  Images     │
            └──────┬──────┘
                   │
                   ↓
        ┌───────────────────────┐
        │ Push to Registry      │
        │ (Docker Hub/ECR)      │
        └───────────┬───────────┘
                    │
                    ↓
        ┌───────────────────────┐
        │ Deploy to Production  │
        │ (EC2/Heroku/Railway)  │
        │                       │
        │ Backend:  uvicorn     │
        │ Frontend: next start  │
        │ Database: alembic run │
        └───────────────────────┘
                    │
                    ↓
        Health Check + Monitoring
```

---

## 10. SEGURANÇA - Implementação

```
┌─────────────────────────────────────────┐
│         Camada de Entrada                │
├─────────────────────────────────────────┤
│                                         │
│  1. CORS Check                          │
│     Origin == localhost:3000 ✓          │
│     Origin == malicious.com ❌          │
│                                         │
└─────────────────────────────────────────┘
           │ Request passado
           ↓
┌─────────────────────────────────────────┐
│      Camada de Autenticação             │
├─────────────────────────────────────────┤
│                                         │
│  2. JWT Validation                      │
│     Authorization: Bearer {token}       │
│     Decode JWT → {user_id, role}        │
│     if exp < now → 401 Unauthorized     │
│                                         │
└─────────────────────────────────────────┘
           │ Usuário autenticado
           ↓
┌─────────────────────────────────────────┐
│    Camada de Autorização (RBAC)         │
├─────────────────────────────────────────┤
│                                         │
│  3. Role Check                          │
│     @require_roles(["admin"])           │
│     if user.role == "admin" ✓           │
│     else → 403 Forbidden                │
│                                         │
└─────────────────────────────────────────┘
           │ Usuário autorizado
           ↓
┌─────────────────────────────────────────┐
│  Camada de Validação (Sensibilidade)    │
├─────────────────────────────────────────┤
│                                         │
│  4. Reauth (se operação sensível)       │
│     POST /auth/reauth {password}        │
│     Hash(password) == User.hashed ✓     │
│     else → 401 Unauthorized             │
│                                         │
└─────────────────────────────────────────┘
           │ Tudo validado
           ↓
┌─────────────────────────────────────────┐
│    Exceção Controlada (try/except)      │
├─────────────────────────────────────────┤
│                                         │
│  5. Error Middleware                    │
│     try:                                │
│       ... do operation ...              │
│     except Exception as e:              │
│       return 500 {detail: str(e)}       │
│       log error to file                 │
│                                         │
└─────────────────────────────────────────┘
```

---

## 11. PADRÕES DE DESIGN

```
┌──────────────────────────────────────────┐
│         Design Patterns Usados           │
├──────────────────────────────────────────┤
│                                          │
│ 1. Singleton (Database Session)          │
│    SessionLocal = Session factory        │
│    One instance per request              │
│                                          │
│ 2. Repository (Service Layer)            │
│    metrics_service.get_mrr()             │
│    Abstrai SQL complexity                │
│                                          │
│ 3. Factory (Seed Scripts)                │
│    seed_plans() → cria dados iniciais   │
│                                          │
│ 4. Dependency Injection                  │
│    @router.get()                         │
│    def handler(db = Depends(get_db))     │
│                                          │
│ 5. Middleware (Chain of Responsibility)  │
│    Chained middlewares process request   │
│                                          │
│ 6. Observer (React useEffect)            │
│    Observa dependency array []           │
│    Executa quando dependência muda       │
│                                          │
│ 7. Strategy (Multiple auth methods)      │
│    JWT vs OAuth vs 2FA (future)         │
│                                          │
└──────────────────────────────────────────┘
```

---

**Diagrama finalizado! Agora você tem um entendimento completo da arquitetura do InsightFlow.**
