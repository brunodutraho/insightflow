# ARCHITECTURE

## Modelo mental
- User → Tenant → Plan → Subscription
- Cada Tenant é uma empresa/organização multi-tenant
- Cada User pertence a um Tenant
- Tenant é associado a um Plan e Subscription atual

## Camadas
1. API (FastAPI)
   - Rotas definidas em `backend/app/routers`
2. Controllers / Routes
   - Recebem request, validam e chamam services
3. Services (regras de negócio)
   - `backend/app/services` + `backend/app/auth/service.py`
4. Models (SQLAlchemy)
   - `backend/app/models`
5. Database (PostgreSQL)
   - configurado em `backend/app/database`

## Padrões usados
- UUID-first (todas as entidades críticas usam UUID PK)
- Multi-tenant isolado por `tenant_id`
- Role + Permission (RBAC)
- Token Services separados (email, reset, invite, JWT)
- Audit logs para ações críticas

## Fluxo essencial
1. request → rota
2. middleware/auth → verifica JWT e tenant
3. rota -> service
4. service -> repository/model
5. DB

## Futuro (repo quecite)
- Repository Layer (UserRepository, TenantRepository)
- Event-driven (Pub/Sub) para notificações e auditoria
- Gateways de cache e filas
