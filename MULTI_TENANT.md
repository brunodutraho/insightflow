# MULTI_TENANT

## Conceito
Cada Tenant representa uma empresa/organização. Todos os dados de negócio são isolados por `tenant_id`, garantindo compartilhamento seguro no mesmo banco.

## Regras
- User só acessa dados do seu tenant
- Admin_master pode acessar todos
- Gestor e cliente acessam apenas `tenant_id` do JWT

## Implementação atual
- `users.tenant_id` (FK)
- `tenants` tabela central
- `subscriptions.tenant_id` (FK)
- `insights.tenant_id`, `ad_metrics.tenant_id`, `social_metrics.tenant_id`, `communication_metrics.tenant_id`, `marketing_metrics.tenant_id` etc.

## Filtro automático recomendado
- `TenantContext` via middleware que extrai `tenant_id` do token
- Service layer sempre faz `where tenant_id == current_tenant`

## Estratégia aqui
- Shared DB + tenant_id (setup atual, ok para SaaS)
- Schema por tenant (futuro)
- DB por tenant (enterprise)

## Exemplo de controle
- `get_users` em admin: se `current_user.role == admin_master` retorno geral, senão filtro `User.tenant_id == current_user.tenant_id`
