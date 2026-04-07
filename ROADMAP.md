# ROADMAP

## Próximas features
- impersonação segura (admin -> user)
- métricas avançadas em tempo real + comparativo histórico
- integração de canais adicionais (email marketing, Whatsapp Business API)
- webhooks para eventos de subscription/login
- API pública versionada (`/v1`/`/v2`)
- central de notificações (in-app, email, SMS)

## Curto prazo
- refatorar para repository layer
- consolidar AuthService / TokenService / EmailService
- criar PlanService e validação de limites
- primeiro MVP de permission middleware (`require_permission`)

## Médio prazo
- arquitetura event-driven (RabbitMQ/Celery/Kafka)
- audit pipeline e auditoria centralizada
- monitoramento e tracing (Prometheus, Grafana, OpenTelemetry)

## Longo prazo
- multi-tenant (schema ou DB por tenant) para enterprise
- colaboração entre múltiplos gestores por tenant
- integração com ERP/CRM
- enable SSO (OAuth2, SAML)
