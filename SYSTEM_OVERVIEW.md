# SYSTEM OVERVIEW

## O que é o sistema?
InsightFlow é uma plataforma SaaS de gestão de marketing e performance para agências e clientes finais. Combina coleta, lacunas de métricas, insights e administração de contas com assinatura e controle de acesso multi-tenant.

## Quem são os usuários?
- admin_master: super administrador com visão global de todos os tenants
- admin_operacional: operador interno com ações administrativas
- gestor: cliente pagante que gerencia a agência/empresa
- cliente: usuário final vinculado a um tenant

## Quais problemas resolve?
- organização de dados de múltiplos clientes em única plataforma
- controle de acesso e permissões por função
- coleta e análise de métricas de campanhas (Meta/Google/TikTok/LinkedIn)
- gerenciamento de planos/assinaturas e limites de uso
- auditoria de ações críticas

## Módulos principais
- Auth & Identity
- Multi-Tenant
- Campaign Engine
- Metrics & Analytics
- Billing & Plans
- Admin Panel

## Seções de alto nível
- 
### Auth & Identity
Login/JWT, registro, reset de senha, email verification, invite flow.

### Multi-Tenant
Modelo de tenant, isolamento por tenant_id, regras RBAC.

### Campaign Engine
Coleta de dados via integrações (GAds, Meta, TikTok, LinkedIn), métricas e insights.

### Metrics & Analytics
EndPoints de KPI, score, ad/social/communication metrics.

### Billing & Plans
Planos (+limites), subscriptions, roles de consumo.

### Admin Panel
Dashboard, gerenciamento de usuários/tenants/plans/coupons, ações de bloqueio e reset.
