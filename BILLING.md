# BILLING

## Modelos
### Plan
Define limites e recursos garantidos:
- max_users
- max_clients
- max_campaigns
- emails_per_day
- whatsapp_enabled

### Subscription
Vincula Tenant a Plan específico
Campos chave:
- tenant_id
- plan_id
- user_id (criador)
- created_at
- canceled_at

## Regras de negócio
- Antes de criar recurso, validar limite do plano:
  - se total_users >= plan.max_users -> bloqueio
  - se total_campaigns >= plan.max_campaigns -> bloqueio
  - se email_send_today >= plan.emails_per_day -> bloqueio

## Serviços sugeridos
- `PlanService.can_create_user(tenant)`
- `PlanService.can_send_email(tenant)`
- `PlanService.can_create_campaign(tenant)`

## Fluxo
1. Tenant cria/atualiza assinatura (subscription)
2. Sistema aplica limite via `PlanService`
3. Em violações, retorna erro 403 e notifica admin

## Observações
- ainda existe modelo, mas falta engine (como requisitado). Próximo passo: implementar validação em service layer e uso de banco momentâneo de consumo (usage table).