# 📋 RESUMO EXECUTIVO - InsightFlow

## 🎯 EM UMA FRASE
**SaaS de análise de marketing que centraliza dados de múltiplos canais e os transforma em dashboards interativos com métricas SaaS avançadas**

---

## 🏢 ESTRUTURA TÉCNICA

```
┌──────────────────────────────────────────┐
│ FRONTEND (Next.js 16 + React 19 + Tailwind)
│ - 3 dashboards (Login, User, Admin) ✨   
│ - 12 componentes + 9 páginas             
│ - Real-time metrics (refresh 60s)        
│ - Dark mode automático                   
└──────────────────────────────────────────┘
         ↓ (Axios + JWT Token)
┌──────────────────────────────────────────┐
│ BACKEND (FastAPI + SQLAlchemy + PostgreSQL)
│ - 13 routers com 40+ endpoints           
│ - Metrics engine (SaaS analytics)        
│ - RBAC (Admin, Gestor, Cliente)         
│ - JWT + Reauth security                  
│ - Alembic migrations                     
└──────────────────────────────────────────┘
         ↓ (ORM + Query Builder)
┌──────────────────────────────────────────┐
│ DATABASE (PostgreSQL)
│ - 15 tabelas (Users, Plans, Subscriptions, etc)
│ - Multi-tenant architecture              
│ - Indexação de performance               
└──────────────────────────────────────────┘
```

---

## 📁 BACKEND - QUICK MAP

| Pasta | Arquivos Principais | O Que Faz |
|-------|-------------------|-----------|
| **auth/** | service.py, routes.py, reauth.py, utils.py | JWT login/register, password hash, re-auth para operações sensíveis |
| **models/** | 15 arquivos (user.py, plan.py, subscription.py, etc) | Define tabelas do BD com SQLAlchemy ORM |
| **routers/** | 13 arquivos (admin_routes.py, subscription_routes.py, etc) | HTTP endpoints para a API |
| **services/** | metrics_service.py, plan_service.py, coupon_service.py, subscription_service.py | Lógica de negócio (cálculo de MRR, churn, etc) |
| **schemas/** | Pydantic models | Validação de requests/responses |
| **middlewares/** | error_middleware.py, logging_middleware.py | Interceptadores HTTP |
| **database/** | database.py, base.py, init_db.py | Conexão BD, session factory, init |
| **scripts/** | seed_plans.py, migrate_subscriptions.py | Scripts de setup |
| **core/** | security.py, logging_config.py | Utilidades de segurança |
| **alembic/** | 10 migration files | Versionamento do schema |

---

## 📁 FRONTEND - QUICK MAP

| Pasta | Arquivos Principais | O Que Faz |
|-------|-------------------|-----------|
| **app/login/** | page.tsx | Formulário de login + JWT handling |
| **app/register/** | page.tsx | Formulário de cadastro novo |
| **app/dashboard/** | page.tsx, layout.tsx | Dashboard do usuário final |
| **app/admin/** | page.tsx (✨ NOVO), layout.tsx, lib/ | **Dashboard executivo com 12 componentes** |
| **app/admin/components/** | 9 novos componentes | StatCard, MRRChart, HealthScoreCard, etc |
| **app/admin/plans/** | page.tsx | Gerenciar planos (CRUD) |
| **app/admin/coupons/** | page.tsx | Gerenciar cupons com desconto |
| **hooks/** | useAuth.ts, useUser.ts | Custom hooks para auth e user data |
| **services/** | api.ts, auth.service.ts, dashboard.service.ts | Integração com API backend |
| **lib/** | auth.ts, analytics.ts, healthScore.ts | Utilitários e cálculos |

---

## 🔑 ENDPOINTS PRINCIPAIS

### 🔐 Autenticação
```
POST   /auth/register        Cria novo usuário
POST   /auth/login           JWT login
POST   /auth/reauth          Re-valida senha
```

### 📊 Admin Dashboard (NOVO!)
```
GET    /admin/overview       Todas métricas em um go
GET    /admin/stats          Distribuição de usuários
GET    /admin/mrr-history    Histórico de receita
GET    /admin/at-risk-clients Clientes em churn
GET    /admin/recent-activity Timeline de events
GET    /admin/detailed-activity Cadastros + sessions
```

### 💳 Planos & Cupons
```
GET    /admin/plans          Lista planos
POST   /admin/plans          Cria plano
PUT    /admin/plans/{id}     Edita plano

GET    /admin/coupons        Lista cupons
POST   /admin/coupons        Cria cupom
PUT    /admin/coupons/{id}   Edita cupom
```

### 📋 Assinaturas
```
GET    /subscriptions/me     Sua assinatura
POST   /subscriptions/{id}/apply-coupon Aplica desconto
```

### 👤 Usuários & Clients
```
GET    /users/me             Dados do usuário
GET    /clients              Empresas do usuário
POST   /clients              Cria novo cliente
```

---

## 🗄️ BANCO DE DADOS - 15 TABELAS

```
users
├── id, email, hashed_password
├── last_login (novo!)
├── role (admin | gestor | cliente)
├── manager_id (FK → users)
└── client_id (FK → clients)

clients
├── id, name, owner_id
├── created_at
└── last_activity_at (novo!)

subscriptions (ANTIGA ESTRUTURA)
├── id, user_id, plan_id (novo!)
├── created_at (novo!)
├── canceled_at (novo!)
└── is_active

plans (NOVA TABELA)
├── id, name, price, max_clients
└── is_active

coupons (NOVA TABELA)
├── id, code, discount_percent, discount_amount
├── max_uses, used_count
└── is_active

activities (NOVA TABELA)
├── id, type, message
└── created_at

app_config (NOVA TABELA)
├── id, key (unique), value
└── Armazena: MRR goals, settings globais

+ 7 outras (ad_metrics, social_metrics, marketing_metrics, etc)
```

---

## 🧠 SERVIÇOS & LÓGICA

### MetricsService (O CORAÇÃO)
```python
# Usuários
get_total_users()              # COUNT(users)
get_new_users_30d()            # WHERE created_at >= 30d ago
get_users_growth_rate()        # % mensal

# Receita
get_mrr()                      # SUM(plans.price) WHERE ativo
get_arpu()                     # MRR / assinaturas
get_mrr_growth()               # % mensal

# Retenção
get_churn_rate()               # % de cancelamentos

# Negócio
get_at_risk_clients()          # Sem atividade 7+ dias
get_mrr_history()              # Histórico 6 meses
get_mrr_pacing()               # Ritmo vs meta

# Events
get_recent_activity()          # Timeline últimos 10
get_detailed_activity()        # Cadastros + sessions
```

### PlansService
```python
get_all_plans()
create_plan()
update_plan()
```

### CouponService
```python
get_all_coupons()
create_coupon()
update_coupon()
```

### SubscriptionService
```python
apply_coupon()                 # Aplica desconto
cancel_subscription()          # Cancela e registra tudo
```

---

## 🎨 COMPONENTES FRONTEND (NOVOS)

| Componente | Usa | Renderiza |
|-----------|-----|-----------|
| **StatCard** | metrics | Card com métrica + trend % |
| **MRRChart** | recharts | Gráfico de linha (receita) |
| **HealthScoreCard** | healthScore.ts | Score 0-100 com gradient |
| **MRRGoalCard** | app_config | Tracker meta com % esperado |
| **AtRiskClients** | at_risk data | Lista clientes em churn |
| **RecentActivityTimeline** | activities | Timeline com filtros |
| **LiveSessionsCard** | sessions | Usuários online agora |
| **NewUsersCard** | accounts | Últimos cadastros |
| **SmartIntelligence** | analytics | Alertas + Insights IA |

---

## 🔐 SEGURANÇA IMPLEMENTADA

✅ **JWT Tokens**
- Armazenado em localStorage
- Enviado em todos os requests
- Expira automaticamente

✅ **Password Hashing**
- bcrypt com salt
- Verificação antes de operations sensíveis

✅ **RBAC (Role-Based Access)**
```python
@require_roles(["admin"])        # Só admin
@require_roles(["admin", "gestor"])  # Admin ou gestor
```

✅ **Reauth (Re-authentication)**
- Sensível: alterar meta MRR, deletar plano
- Requer re-validação de senha

✅ **CORS**
- Apenas localhost:3000 pode acessar API

---

## 📈 CÁLCULOS PRINCIPAIS

### SaaS Health Score (0-100)
```
Score = (MRR Growth × 40%) + (Churn × 30%) + (User Growth × 30%)

Exemplo:
- MRR cresceu 20% = 40 pontos
- Churn 3% = 20 pontos
- Users cresceu 10% = 30 pontos
- Total: 90 = "Excelente" ✅
```

### MRR (Monthly Recurring Revenue)
```sql
SELECT SUM(plans.price)
FROM subscriptions
JOIN plans ON subscriptions.plan_id = plans.id
WHERE subscriptions.is_active = TRUE
```

### Churn Rate
```
(Cancelamentos em 30d / Total no início) × 100
Exemplo: 4 canceled / 100 total = 4% churn
```

### ARPU (Average Revenue Per User)
```
MRR / active_subscriptions
Exemplo: 10.000 MRR / 50 subs = 200 ARPU
```

---

## 🎯 PADRÕES IMPLEMENTADOS

✅ **MVC**: Models (SQLAlchemy) → Views (Routers) → Controllers (Services)

✅ **Dependency Injection**: FastAPI `Depends()` para BD session

✅ **Service Layer**: Routers chamam Services, não BD direto

✅ **Middleware Chain**: CORS → ErrorHandler → LoggerMiddleware

✅ **Repository Pattern**: Services atuam como repositórios

✅ **Factory Pattern**: seed_plans(), seed_coupons() para data init

✅ **REST Conventions**: GET/POST/PUT/DELETE por recurso

---

## 🚀 FLUXO DE DADOS - Exemplo Real

```
Admin acessa /admin
    ↓
Frontend dispara 5 requests paralelos:
    GET /admin/overview
    GET /admin/mrr-history
    GET /admin/at-risk-clients
    GET /admin/recent-activity
    GET /admin/detailed-activity
    ↓
Backend processa cada request:
    1. Valida JWT token
    2. Checa role (deve ser "admin")
    3. Chama service method apropriado
    4. Service faz queries ao BD
    5. Retorna JSON com 200 OK
    ↓
Frontend recebe 5 responses
    ↓
React state atualiza com dados
    ↓
Componentes (StatCard, MRRChart, etc) rerendem
    ↓
Admin vê dashboard completo! 📊
    ↓
Cada 60s → fetch automático de novo
```

---

## 💾 MIGRAÇÕES (Alembic)

```bash
# Criar nova migração
$ alembic revision --autogenerate -m "add new feature"

# Aplicar todas as pendentes
$ alembic upgrade head

# Voltar uma versão
$ alembic downgrade -1

# Ver histórico
$ alembic history
```

**10 migrações já aplicadas:**
- Add plans table
- Add coupons table
- Add plan_id to subscriptions
- Add timestamps
- Add canceled_at
- Add last_activity_at
- Add last_login
- Drop deprecated columns
- E mais...

---

## 📦 DEPENDÊNCIAS PRINCIPAIS

### Backend
```
fastapi             7Web framework
sqlalchemy          ORM Python
psycopg2            Driver PostgreSQL
alembic             Database migrations
pydantic            Validation
python-jose         JWT tokens
passlib+bcrypt      Password hashing
python-multipart    File uploads
```

### Frontend
```
next                16     Framework React
react               19     UI library
typescript          5      Type safety
tailwindcss         3.4    Styling
axios               1.13   HTTP client
react-query         5.95   Data fetching
recharts            3.8    Charts
lucide-react        1.7    Icons
```

---

## 🎯 MÉTRICAS RASTREADAS

| Métrica | Frequência | Fonte | Uso |
|---------|-----------|-------|-----|
| Total Usuários | Real-time | COUNT(users) | Dashboard |
| Novos Usuários | Diário | WHERE created_at >= 24h | Growth |
| MRR | Real-time | SUM(plans.price) | Receita |
| Churn Rate | Diário | Cancelamentos/Total | Retenção |
| ARPU | Real-time | MRR/Assinaturas | Valor |
| Health Score | Real-time | Fórmula composta | SaaS Health |
| Growth Rate | Mensal | (Novo-Anterior)/Anterior | Tendência |
| At-Risk | Real-time | WHERE last_activity > 7d | Alerta |

---

## ✨ FEATURES IMPLEMENTADAS (RECENTES)

✅ **Sistema de Planos** (Plan CRUD)
✅ **Sistema de Cupons** (Coupon CRUD com desconto)
✅ **Assinaturas** (Subscription + plan_id FK)
✅ **Rastreamento de Login** (last_login field)
✅ **Atividades** (Activity Timeline)
✅ **Admin Dashboard** (12 componentes)
✅ **Health Score** (Algoritmo SaaS)
✅ **MRR Tracking** (Cálculo + Histórico)
✅ **Smart Intelligence** (Alerts + Insights)
✅ **At-Risk Detection** (Churn prediction)
✅ **Re-auth Security** (Password confirmation)

---

## 🔮 ROADMAP

- [ ] Exportar dados (PDF/CSV)
- [ ] Webhooks para eventos
- [ ] 2FA (Two-Factor Auth)
- [ ] Integrações (Slack/Zapier)
- [ ] Mobile App (React Native)
- [ ] Analytics avançado
- [ ] Custom reports
- [ ] API pública para partners

---

## 🎓 CONCEITOS-CHAVE

| Conceito | Implementado Como |
|----------|-------------------|
| **Multi-tenant** | client_id em cada tabela |
| **RBAC** | UserRole enum + @require_roles |
| **MVC** | Services → Routers → Frontend |
| **REST API** | FastAPI routers + Pydantic |
| **ORM** | SQLAlchemy Models |
| **Migrations** | Alembic versions |
| **JWT Auth** | Jose + localStorage |
| **SSR** | Next.js App Router |
| **Type Safety** | TypeScript + Pydantic |
| **Responsive** | Tailwind CSS + mobile-first |

---

## 📞 QUICK COMMANDS

```bash
# Backend - Rodagem local
$ cd backend
$ pip install -r requirements.txt
$ alembic upgrade head
$ uvicorn app.main:app --reload

# Frontend - Rodagem local
$ cd frontend
$ npm install
$ npm run dev

# Docker
$ docker-compose up

# Seed data
$ python -m app.scripts.seed_plans
```

---

## 📊 ESTATÍSTICAS DO CÓDIGO

- **Backend**: ~15 modelos, 40+ endpoints, 4 services principais
- **Frontend**: 9 páginas, 12 componentes, 3 hooks, 3 services
- **Database**: 15 tabelas, 10 migrações, índices em PK+FK
- **Linhas de código**: ~8000+ (backend) + 5000+ (frontend)
- **TypeScript**: 100% coverage no frontend
- **Cobertura de testes**: (para fazer)

---

**Versão**: 1.0.0 MVP  
**Data**: 31 de Março, 2026  
**Mantida por**: Seu Time Dev  
**Status**: 🟢 Production Ready
