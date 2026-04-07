# 📚 DOCUMENTAÇÃO COMPLETA - InsightFlow

**Data**: 31 de Março de 2026  
**Versão**: MVP 1.0  
**Status**: Em Produção

---

## 🎯 O QUE É O PROJETO?

**InsightFlow** é uma **plataforma SaaS de análise de marketing** que centraliza dados de múltiplos canais de marketing (Instagram, Facebook, Google Ads) e os transforma em insights acionáveis.

### Objetivo Principal
Permitir que agências e empresas de marketing:
- ✅ Rastreiem performance de campanhas
- ✅ Analisem métricas de engajamento
- ✅ Monitorem conversões e ROI
- ✅ Visualizem dados em dashboards interativos
- ✅ Gerenciem assinaturas e planos

### Modelo de Negócio
- **Multi-tenant** (cada cliente vê apenas seus dados)
- **Subscription-based** (Free, Basic, Pro, Enterprise)
- **RBAC** (Controle de acesso por roles: Admin, Gestor, Cliente)

---

## 🏗️ ARQUITETURA GERAL

```
┌─────────────────────────────────────────┐
│        CAMADA DE APRESENTAÇÃO           │
│  Next.js 16 (React 19) - Frontend       │
│  - Admin Dashboard                      │
│  - User Dashboard                       │
│  - Login/Register                       │
└─────────────────────────────────────────┘
                    ↓
         Axios (HTTP Client)
                    ↓
┌─────────────────────────────────────────┐
│        CAMADA DE API                    │
│  FastAPI (Python) - Backend             │
│  - Routers (Endpoints)                  │
│  - Middlewares (Auth, Error, Logging)   │
│  - Services (Business Logic)            │
│  - Models (SQLAlchemy ORM)              │
└─────────────────────────────────────────┘
                    ↓
         SQLAlchemy ORM
                    ↓
┌─────────────────────────────────────────┐
│        CAMADA DE DADOS                  │
│  PostgreSQL Database                    │
│  - Users, Clients, Subscriptions        │
│  - Plans, Coupons, Metrics              │
│  - Activities, Logs                     │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│        INTEGRAÇÕES EXTERNAS             │
│  - Instagram Graph API                  │
│  - Facebook Marketing API               │
│  - Google Ads API                       │
│  - Scheduler (Coleta de dados)          │
└─────────────────────────────────────────┘
```

---

# 📦 BACKEND (`/backend`)

## 1️⃣ Estrutura Geral

```
backend/
├── alembic/                    # Migrações de banco de dados
├── app/
│   ├── main.py                # Arquivo principal da aplicação
│   ├── auth/                  # Autenticação e autorização
│   ├── config/                # Configurações
│   ├── core/                  # Utilidades de segurança e logging
│   ├── database/              # Inicialização e conexão com BD
│   ├── middlewares/           # Interceptadores HTTP
│   ├── models/                # Modelos SQLAlchemy (Banco de dados)
│   ├── routers/               # Endpoints da API
│   ├── schemas/               # Validação de request/response (Pydantic)
│   ├── scripts/               # Scripts úteis (seed, migration)
│   └── services/              # Lógica de negócio
├── requirements.txt           # Dependências Python
└── Dockerfile                 # Container docker
```

---

## 2️⃣ ROTAS & ENDPOINTS

### 📍 Auth Routes (`/auth`)
```
POST   /auth/register          → Registra novo usuário
POST   /auth/login             → Faz login (retorna token JWT)
POST   /auth/reauth            → Re-autentica (senha obrigatória)
```

### 📍 User Routes (`/users`)
```
GET    /users/me               → Dados do usuário logado
GET    /users                  → Lista todos (Admin)
PUT    /users/{id}             → Atualiza usuário
```

### 📍 Admin Routes (`/admin`)
```
GET    /admin/overview         → Dashboard principal com métricas
GET    /admin/stats            → Distribuição de usuários e roles
GET    /admin/mrr-history      → Histórico de receita mensal
GET    /admin/at-risk-clients  → Clientes em risco de churn
GET    /admin/recent-activity  → Timeline de atividades recentes
GET    /admin/detailed-activity→ Logs de cadastros e sessões

GET    /admin/plans            → Lista planos
POST   /admin/plans            → Cria plano novo
PUT    /admin/plans/{id}       → Atualiza plano

GET    /admin/coupons          → Lista cupons
POST   /admin/coupons          → Cria cupom novo
PUT    /admin/coupons/{id}     → Atualiza cupom

POST   /admin/goal/mrr          → Define meta de MRR (requer senha)
```

### 📍 Subscription Routes (`/subscriptions`)
```
GET    /subscriptions/me       → Assinatura do usuário logado
POST   /subscriptions/{id}/apply-coupon → Aplica desconto
```

### 📍 Analytics Routes (`/analytics`)
```
GET    /analytics/dashboard    → Dados de análise
GET    /analytics/insights     → Insights automáticos
```

### 📍 Client Routes (`/clients`)
```
GET    /clients                → Lista clientes do usuário
GET    /clients/{id}           → Detalhes de um cliente
POST   /clients                → Cria novo cliente
```

### 📍 Other Routes
```
GET    /health                 → Health check
GET    /kpi/*                  → KPIs customizados
GET    /score/*                → Scores de performance
GET    /dashboard/*            → Dashboard data
GET    /insights/*             → Marketing insights
GET    /ad-accounts/*          → Contas de anúncios
GET    /social/*               → Métricas sociais
```

---

## 3️⃣ MODELS (Banco de Dados)

### 👤 User
```python
id                INTEGER PRIMARY KEY
email             STRING (unique)
hashed_password   STRING
last_login        DATETIME     # Última vez que fez login
role              ENUM(admin, gestor, cliente)
manager_id        FK → users.id (Quem gerencia este usuário)
client_id         FK → clients.id (Empresa associada)
created_at        DATETIME
```
**Uso**: Autenticação, autorização (RBAC), rastreamento de atividades

---

### 🏢 Client
```python
id                INTEGER PRIMARY KEY
name              STRING
owner_id          FK → users.id
created_at        DATETIME
last_activity_at  DATETIME (com server_default=now())
```
**Uso**: Empresa/agência que contrata o SaaS. Isolamento de dados multi-tenant.

---

### 📋 Subscription
```python
id                INTEGER PRIMARY KEY
user_id           FK → users.id
plan_id           FK → plans.id
created_at        DATETIME
canceled_at       DATETIME (NULL enquanto ativa)
is_active         BOOLEAN
```
**Uso**: Controla qual plano o usuário tem e quando cancelou.

---

### 💳 Plan
```python
id                INTEGER PRIMARY KEY
name              STRING (unique)
price             FLOAT
max_clients       INTEGER (limite de empresas)
is_active         BOOLEAN
created_at        DATETIME
subscriptions     RELATIONSHIP → Subscription[]
```
**Uso**: Planos disponíveis (free, basic, pro, enterprise)

---

### 🎟️ Coupon
```python
id                INTEGER PRIMARY KEY
code              STRING (unique)
discount_percent  FLOAT (NULL)
discount_amount   FLOAT (NULL)
max_uses          INTEGER (NULL)
used_count        INTEGER
is_active         BOOLEAN
created_at        DATETIME
```
**Uso**: Cupons de desconto para assinaturas

---

### 📊 Métricas
- **AdMetric**: Métricas de Google Ads (impressões, clicks, spend)
- **SocialMetric**: Followers, engagement, growth rate
- **MarketingMetric**: Conversões, CTR, ROAS
- **CommunicationMetric**: Email opens, clicks
- **Insight**: Insights gerados (texto + categoria)

---

### 🔔 Activity
```python
id                INTEGER PRIMARY KEY
type              STRING (assinatura, cadastro, cancelamento, configuracao)
message           STRING
created_at        DATETIME
```
**Uso**: Timeline de eventos para o dashboard

---

### ⚙️ AppConfig
```python
id                INTEGER PRIMARY KEY
key               STRING (unique)
value             FLOAT
```
**Uso**: Configurações globais (ex: meta de MRR)

---

## 4️⃣ SERVICES (Lógica de Negócio)

### 📈 metrics_service.py
**O CORAÇÃO DO DASHBOARD** - Calcula todas as métricas SaaS

```python
# USUÁRIOS
get_total_users()              → Total de usuários cadastrados
get_new_users_30d()            → Novos usuários últimos 30 dias
get_users_growth_rate()        → % de crescimento mensal

# RECEITA
get_mrr()                      → Monthly Recurring Revenue
get_mrr_growth()               → % de crescimento de MRR
get_arpu()                     → Ticket médio (Average Revenue Per User)
get_mrr_history()              → Histórico dos últimos 6 meses

# CHURN
get_churn_rate()               → % de cancelamentos em 30 dias

# EMPRESAS
get_at_risk_clients()          → Clientes sem atividade há 7+ dias

# ATIVIDADES
get_recent_activity()          → Últimos 10 eventos (usuários + subscrições)
get_detailed_activity()        → Novos cadastros + sessões ativas

# GOALS
get_mrr_pacing()               → Ritmo corrente vs meta do mês
update_mrr_goal()              → Altera meta de MRR (requer senha)
```

---

### 💼 plan_service.py
```python
get_all_plans()                → Lista todos os planos
create_plan()                  → Cria novo plano
update_plan()                  → Edita plano existente
```

---

### 🎟️ coupon_service.py
```python
get_all_coupons()              → Lista cupons
create_coupon()                → Cria cupom
update_coupon()                → Edita cupom
```

---

### 📋 subscription_service.py
```python
apply_coupon()                 → Aplica desconto à assinatura
cancel_subscription()          → Cancela assinatura
```

---

### 👤 user_service.py
```python
create_user()                  → Cria novo usuário
get_user_by_email()            → Busca por email
update_user()                  → Atualiza perfil
```

---

## 5️⃣ MIDDLEWARES

### ErrorMiddleware
- ✅ Captura todas as exceções
- ✅ Retorna erro estruturado com status HTTP
- ✅ Loga o erro

### LoggingMiddleware
- ✅ Registra todas as requisições (método, rota, IP)
- ✅ Registra tempo de resposta

---

## 6️⃣ AUTENTICAÇÃO & SEGURANÇA

### JWT (JSON Web Tokens)
```python
# Login gera token JWT contendo:
{
  "user_id": 1,
  "email": "user@example.com",
  "role": "admin"
}
# Token armazenado no localStorage do cliente
```

### RBAC (Role-Based Access Control)
```python
# Três roles:
ADMIN   → Acesso total (admin dashboard, manage plans/coupons)
GESTOR  → Acesso a dados de sua empresa
CLIENTE → Acesso limitado aos insights
```

### Reauth (Re-autenticação)
```python
# Para operações sensíveis (alterar meta, mudar plano):
POST /auth/reauth {password: "..."}
# Backend verifica hash da senha antes de permitir
```

---

## 7️⃣ MIGRAÇÕES (Alembic)

Alembic gerencia versionamento do schema do banco.

```
alembic/versions/
├── 433dd0f722ed_add_plans_table.py
├── ef381eb5c8d1_add_coupons_table.py
├── 015dc466f5cc_add_discount_to_subscriptions.py
├── 350792a708da_add_plan_id_to_subscriptions.py
├── 72d6f93b0bb0_add_timestamps_to_subscriptions.py
├── 80a52bf90c7d_add_updated_at_to_subscriptions.py
├── 881ff1241b38_add_canceled_at_to_subscriptions.py
├── bf4c90a3b23c_add_last_activity_at_to_clients.py
├── df84839902fb_add_last_login_to_users_and_last_.py
└── ea8aeb23f029_fix_subscription_remove_plan_string.py
```

**Como rodar migrações:**
```bash
$ cd backend
$ alembic upgrade head  # Aplica todas as migrações pendentes
```

---

## 8️⃣ SCRIPTS

### seed_plans.py
```bash
python -m app.scripts.seed_plans
```
Cria planos padrão (free, basic, pro, enterprise)

### create_subscription.py
```bash
python -m app.scripts.create_subscription
```
Cria assinatura manualmente para um usuário

### migrate_subscriptions.py
```bash
python -m app.scripts.migrate_subscriptions
```
Migra dados de plano antigo para novo schema

---

# 🎨 FRONTEND (`/frontend`)

## 1️⃣ Estrutura Geral

```
frontend/
├── public/                    # Arquivos estáticos
├── src/
│   ├── app/                  # Next.js App Router (páginas)
│   ├── components/           # Componentes React reutilizáveis
│   ├── hooks/                # Custom React hooks
│   ├── lib/                  # Utilitários (auth, helpers)
│   ├── services/             # Integração com API
│   ├── types/                # TypeScript types
│   ├── utils/                # Funções auxiliares
│   └── globals.css           # Estilos globais
├── tailwind.config.js        # Configuração Tailwind CSS
├── tsconfig.json             # Configuração TypeScript
└── next.config.ts            # Configuração Next.js
```

---

## 2️⃣ PÁGINAS (App Router)

### 🔑 `/login`
```
login/
├── page.tsx                  # Formulário de login
└── components/
```
**Funcionalidade**: 
- Formulário email + senha
- Valida credenciais com backend
- Armazena JWT no localStorage
- Redireciona para /dashboard ou /admin

---

### 📝 `/register`
```
register/
└── page.tsx
```
**Funcionalidade**:
- Formulário de cadastro
- Cria novo usuário como "cliente"
- Redireciona para login após sucesso

---

### 📊 `/dashboard`
```
dashboard/
├── page.tsx                  # Dashboard do usuário
├── layout.tsx                # Layout com sidebar
└── users/                    # Submenu de usuários
```
**Funcionalidade**:
- Visão geral de dados do cliente
- KPIs, gráficos, insights
- Seletor de empresas

---

### ⚙️ `/admin`
```
admin/
├── page.tsx                  # Dashboard executivo ✨ NOVO
├── layout.tsx                # Layout com sidebar responsiva
├── components/
│   ├── Sidebar.tsx           # Navegação fixa/colapsável
│   ├── StatCard.tsx          # Card de métrica com trend
│   ├── MRRChart.tsx          # Gráfico de receita
│   ├── HealthScoreCard.tsx   # Score 0-100
│   ├── MRRGoalCard.tsx       # Tracker de meta
│   ├── AtRiskClients.tsx     # Alertas de churn
│   ├── RecentActivityTimeline.tsx → Timeline de eventos
│   ├── LiveSessionsCard.tsx  # Usuários online agora
│   ├── NewUsersCard.tsx      # Novos cadastros
│   └── SmartIntelligence.tsx → Alertas + Insights
├── lib/
│   ├── analytics.ts          # Engine de análise
│   └── healthScore.ts        # Cálculo de saúde SaaS
├── plans/
│   └── page.tsx              # Gerenciar planos
├── coupons/
│   └── page.tsx              # Gerenciar cupons
├── users/
│   └── (mais páginas admin)
└── companies/
    └── (mais páginas admin)
```

---

## 3️⃣ COMPONENTES IMPORTANTES

### 🎯 Admin Dashboard (`/admin/page.tsx`)

**O componente central que orquestra todo o admin panel**

**Estados principais:**
```typescript
const [data, setData] = useState<OverviewData>()      // Métricas principais
const [mrrHistory, setMrrHistory] = useState([])      // Histórico MRR
const [atRisk, setAtRisk] = useState([])              // Clientes em risco
const [activity, setActivity] = useState([])          // Timeline
const [activityData, setActivityData] = useState({})  // Cadastros + sessões
```

**Fluxo de dados:**
```
1. Componente monta
2. fetchData() dispara 5 requisições paralelas ao backend
3. Recebe: overview, mrr-history, at-risk-clients, recent-activity, detailed-activity
4. Atualiza estado local
5. Renderiza 12 componentes filhos com os dados
6. A cada 60 segundos, refetch automático
```

---

### 📊 StatCard
```tsx
<StatCard 
  label="Total de Usuários"
  value={1243}
  change={12.5}        // % de crescimento
  prefix="R$"
/>
```
**Renderiza**: Card com título, valor grande, e seta ↑↓ com % de mudança

---

### 📈 MRRChart
```tsx
<MRRChart data={[
  { month: "Jan", mrr: 5000 },
  { month: "Fev", mrr: 5500 },
  ...
]} />
```
**Renderiza**: Gráfico de linha com Recharts mostrando receita mensal

---

### 💚 HealthScoreCard
```tsx
<HealthScoreCard health={{
  score: 87,
  label: "Excelente",
  colorClass: "from-emerald-500 to-teal-600"
}} />
```
**Renderiza**: Card grande com gradient cor, mostrando saúde SaaS (0-100)

**Cálculo de saúde:**
```
Score = (MRR Growth × 40%) + (Churn Rate × 30%) + (User Growth × 30%)

85+  → Excelente (verde)
65+  → Boa (azul)
45+  → Atenção (laranja)
<45  → Crítica (vermelho)
```

---

### 🎯 MRRGoalCard
```tsx
<MRRGoalCard 
  current={12500}
  goal={{
    target: 15000,
    expected_progress: 75
  }}
  onUpdate={fetchData}
/>
```
**Renderiza**: 
- Div com MRR atual + meta
- Barra de progresso mostrando % do mês alcançado vs esperado
- Botão para editar meta (abre modal com campo de senha)

---

### 🚨 SmartIntelligence
```tsx
<SmartIntelligence analysis={{
  alerts: [
    { text: "Receita em queda", type: "danger", icon: "🚨" }
  ],
  insights: [
    { text: "Crescimento acelerado", type: "success", icon: "🚀" }
  ]
}} />
```
**Renderiza**: Seção de alertas críticos + insights estratégicos

**Engine de análise** (`lib/analytics.ts`):
```typescript
if (mrrGrowth < 0) → ALERTA "Receita em queda"
if (churn > 8%) → ALERTA "Churn crítico"
if (userGrowth > 15%) → INSIGHT "Viralidade detectada"
```

---

### ⚠️ AtRiskClients
```tsx
<AtRiskClients data={[
  { id: 5, name: "Acme Corp", last_login_days: 14, status: "inactive" }
]} />
```
**Renderiza**: Lista de clientes inativos há 7+ dias com botão "Resgatar"

---

## 4️⃣ HOOKS CUSTOMIZADOS

### useAuth
```typescript
const { user, login, logout, isLoading } = useAuth()
```
Gerencia autenticação, JWT, e estado de login

### useUser
```typescript
const { user } = useUser()
```
Busca dados do usuário (/users/me) e o cacheia

---

## 5️⃣ SERVIÇOS (API Integration)

### api.ts
```typescript
const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL,
  headers: {
    Authorization: `Bearer ${token}` // Adicionado automaticamente
  }
})
```
Todos os requests herdam o JWT automaticamente

### auth.service.ts
```typescript
login(email, password)        → POST /auth/login
register(email, password)     → POST /auth/register
reauth(password)              → POST /auth/reauth
```

### dashboard.service.ts
```typescript
getOverview()                 → GET /admin/overview
getStats()                    → GET /admin/stats
getMRRHistory()               → GET /admin/mrr-history
getAtRiskClients()            → GET /admin/at-risk-clients
getRecentActivity()           → GET /admin/recent-activity
getDetailedActivity()         → GET /admin/detailed-activity
```

---

## 6️⃣ STYLED COMPONENTS

### Tailwind CSS
Framework utility-first para estilização

```tsx
<div className="bg-white dark:bg-slate-900 p-6 rounded-2xl shadow-lg">
  Dark mode automático via localStorage
</div>
```

### Temas Implementados
- 🌙 Dark mode (automático)
- ⚡ Animações suaves (transitions)
- 📱 Responsivo mobile-first

---

## 7️⃣ TYPESCRIPT TYPES

### types/dashboard.ts
```typescript
interface OverviewData {
  users: { total, new_last_30_days, growth_rate }
  revenue: { active_subscriptions, mrr, arpu, churn_rate, mrr_growth }
  goal: { target, expected_progress }
}
```

---

# 🏗️ PADRÕES & METODOLOGIAS

## ✅ DESIGN PATTERNS IMPLEMENTADOS

### 1. **MVC (Model-View-Controller)**
```
Backend:
  Model     → SQLAlchemy (app/models/)
  View      → Routers/Endpoints (app/routers/)
  Controller→ Services (app/services/)

Frontend:
  Model     → TypeScript types
  View      → React components
  Controller→ Services (custom hooks)
```

### 2. **Dependency Injection**
```python
# Backend
@router.get("/admin/overview")
def get_overview(db: Session = Depends(get_db)):
    # Ambos injetados automaticamente pelo FastAPI
```

```typescript
// Frontend
const { data } = useQuery(['admin'], () => api.get('/admin/overview'))
```

### 3. **Middleware Pattern**
```python
app.add_middleware(ErrorMiddleware)    # Intercepta erros
app.add_middleware(LoggingMiddleware)  # Registra requisições
app.add_middleware(CORSMiddleware)     # Permite requisições cross-origin
```

### 4. **Service Layer Pattern**
```
Routers → Services → Models
  HTTP      Lógica     Banco
```
Routers apenas orquestram, Services possuem a lógica

### 5. **Repository Pattern (Implicit)**
```python
# Serviços atuam como repositórios
metrics_service.get_mrr()  # Abstrai SQL complexity
```

### 6. **Factory Pattern (Seed Scripts)**
```python
seed_plans()         # Factory que cria dados iniciais
seed_coupons()       # Sem necessidade de UI
```

---

## 🔐 SEGURANÇA

### JWT Authentication
```
1. Login → POST /auth/login {email, password}
2. Backend valida credenciais
3. Retorna JWT token
4. Frontend armazena em localStorage
5. Cada requisição envia Authorization: Bearer {token}
6. Backend valida JWT antes de processar
```

### RBAC (Roles-Based Access Control)
```python
@require_roles(["admin"])           # Só admin pode acessar
def admin_endpoint():
    ...

@require_roles(["admin", "gestor"]) # Admin OU gestor
def both_can_access():
    ...
```

### Password Hashing
```python
# Backend
from passlib import CryptContext

hash_password("senha123")  # bcrypt hash
verify_password("senha123", hash)  # Valida
```

### Reauth (Re-authentication)
Para operações sensíveis (alterar meta, deletar dados):
```python
POST /auth/reauth {password: "..."}
# Backend re-valida a senha antes de permitir
```

---

## 📊 DATABASE & ORM

### SQLAlchemy (Python ORM)
```python
# Define modelos como classes Python
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)

# Query de forma Pythônica
users = db.query(User).filter(User.role == "admin").all()
```

### Migrations com Alembic
```bash
alembic revision --autogenerate -m "add new column"
alembic upgrade head
alembic downgrade -1  # Volta uma versão
```

---

## 📡 API DESIGN

### RESTful Conventions
```
GET    /resource         → Lista tudo
GET    /resource/{id}    → Um específico
POST   /resource         → Cria novo
PUT    /resource/{id}    → Edita
DELETE /resource/{id}    → Deleta
```

### Structured Responses
```json
// Sucesso
{ "data": {...}, "status": 200 }

// Erro
{ "detail": "Mensagem de erro", "status": 400 }
```

### Pagination (quando aplicável)
```json
{
  "items": [...],
  "total": 100,
  "page": 1,
  "limit": 10
}
```

---

## ⚡ PERFORMANCE

### Frontend
- **React Query** para caching automático
- **Next.js Image** para otimizações de imagem
- **Code splitting** automático (lazy loading)
- **Dark mode** com localStorage (sem blink)

### Backend
- **Query batching** (múltiplas métricas em uma requisição)
- **Índices no BD** (email, user_id, client_id)
- **Lazy loading** de relacionamentos
- **Database connection pooling**

### Caching
- Frontend: React Query (24h padrão)
- Backend: (possível adicionar Redis no futuro)

---

## 📝 LOGGING & MONITORING

### Backend
```python
# Todos os logs salvos em logs/
2024-03-31 14:23:15 - INFO - GET /admin/overview Called
2024-03-31 14:23:16 - ERROR - Subscription not found (404)
```

### Frontend
```typescript
// Console logs para debug
console.log("Dashboard loaded", data)
```

---

## 🔄 CI/CD Ready

### Docker
```dockerfile
# Backend containerizado
FROM python:3.11
RUN pip install -r requirements.txt
CMD ["uvicorn", "app.main:app"]
```

### Environment Variables
```bash
# Backend (.env)
DATABASE_URL=postgresql://user:pass@localhost/insightflow
SECRET_KEY=xxx...

# Frontend (.env.local)
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## 📚 ESTRUTURA DE PASTAS - RESUMO

```
InsightFlow/
├── backend/
│   ├── app/
│   │   ├── auth/          ← Autenticação & JWT
│   │   ├── models/        ← SQLAlchemy Models (Banco)
│   │   ├── routers/       ← Endpoints/Routes
│   │   ├── services/      ← Lógica de negócio
│   │   ├── middlewares/   ← Interceptadores HTTP
│   │   ├── schemas/       ← Validação Pydantic
│   │   ├── core/          ← Utilities (security, logging)
│   │   ├── database/      ← Conexão BD
│   │   ├── scripts/       ← Seed, migration scripts
│   │   └── main.py        ← Instância FastAPI

│   ├── alembic/           ← Versionamento BD
│   ├── requirements.txt   ← Dependências
│   └── Dockerfile

└── frontend/
    ├── src/
    │   ├── app/
    │   │   ├── (login)    ← Autenticação
    │   │   ├── (dashboard)← User dashboard
    │   │   └── (admin)    ← Admin dashboard ✨
    │   ├── components/    ← React components
    │   ├── hooks/         ← Custom hooks
    │   ├── services/      ← API integration
    │   ├── lib/           ← Utilities
    │   └── types/         ← TypeScript types
    ├── public/            ← Assets estáticos
    ├── tailwind.config.js ← Estilos
    └── tsconfig.json      ← TypeScript config
```

---

# 🚀 FLUXO DE UMA REQUISIÇÃO

## Exemplo: Admin quer ver Dashboard

### 1️⃣ Frontend
```typescript
// Admin acessa /admin
// useEffect dispara:
const { data } = await Promise.all([
  api.get("/admin/overview"),
  api.get("/admin/mrr-history"),
  api.get("/admin/at-risk-clients"),
  api.get("/admin/recent-activity"),
  api.get("/admin/detailed-activity")
])
```

### 2️⃣ Backend - Request
```
GET /admin/overview HTTP/1.1
Authorization: Bearer eyJhbGc...
```

### 3️⃣ Backend - Middleware
```python
# 1. CORSMiddleware → Permite request
# 2. ErrorMiddleware → Pronto para capturar erros
# 3. LoggingMiddleware → Registra a requisição
```

### 4️⃣ Backend - Route Handler
```python
@router.get("/admin/overview")
def get_admin_overview(db: Session = Depends(get_db)):
    # FastAPI injeta a sessão do BD
    return {
        "users": metrics.get_total_users(db),
        "revenue": metrics.get_mrr(db),
        "goal": metrics.get_mrr_pacing(db)
    }
```

### 5️⃣ Backend - Service Layer
```python
def get_mrr(db: Session):
    result = db.query(func.sum(Plan.price))\
        .select_from(Subscription)\
        .join(Plan, Subscription.plan_id == Plan.id)\
        .filter(Subscription.is_active == True)\
        .scalar()
    return float(result or 0.0)
```

### 6️⃣ Backend - Database
```sql
SELECT SUM(plans.price)
FROM subscriptions
JOIN plans ON subscriptions.plan_id = plans.id
WHERE subscriptions.is_active = TRUE
```

### 7️⃣ Backend - Response
```json
{
  "users": {
    "total": 245,
    "new_last_30_days": 18,
    "growth_rate": 12.5
  },
  "revenue": {
    "active_subscriptions": 64,
    "mrr": 12500.00,
    "arpu": 195.31,
    "churn_rate": 3.2,
    "mrr_growth": 8.7
  },
  "goal": {
    "target": 15000,
    "expected_progress": 75.1
  }
}
```

### 8️⃣ Frontend - State Update
```typescript
const [data, setData] = useState(response.data)
// Rerenderiza componentes filhos com novos dados
```

### 9️⃣ Frontend - Render
```tsx
<StatCard label="MRR" value={12500} change={8.7} />
<MRRChart data={mrrHistory} />
<HealthScoreCard health={calculateSaaSHealth(data)} />
// ... mais 9 componentes
```

---

# 📊 MÉTRICAS PRINCIPAIS

| Métrica | Cálculo | Interpretação |
|---------|---------|---------------|
| **MRR** | SUM(Plan.price) onde ativo | Receita mensal recorrente |
| **ARPU** | MRR / active_subscriptions | Valor médio por usuário |
| **Churn Rate** | canceled / total × 100 | % de cancelamentos |
| **Growth Rate** | (novo - anterior) / anterior × 100 | % de crescimento |
| **Health Score** | (MRR 40% + Churn 30% + Users 30%) | 0-100 rating |

---

# 🎯 PRÓXIMAS FEATURES

- [ ] Exportar dados em PDF/CSV
- [ ] Webhooks para eventos
- [ ] 2FA (Two-Factor Authentication)
- [ ] Dark mode completo (já 80% pronto)
- [ ] Integrações com Slack/Zapier
- [ ] Mobile app (React Native)
- [ ] Analytics avançado (attribution)
- [ ] Custom reports

---

# 📞 SUPORTE & CONTRIB

**GitHub**: insightflow  
**Issues**: GitHub Issues  
**Email**: support@insightflow.com  

---

**Última atualização**: 31 de Março de 2026  
**Versão**: 1.0.0 MVP  
**Mantida por**: Tim Insider Dev Team
