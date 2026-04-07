# AUDIT

## O que logar
- login
- logout (quando implementado)
- reset senha
- criação de usuário
- atualização de role/status
- bloqueio de usuário
- criação/alteração de tenant
- planos e cobrança
- impersonação

## Estrutura de audit log
Tabela: `audit_logs`
Campos:
- id (UUID)
- user_id (UUID)
- action (string)
- details (texto)
- ip_address (string)
- user_agent (string)
- created_at (timestamp)

## Arquitetura
### AuditService
- `log_action(user, action, entity, metadata)`
- chamado por: AuthService, UserService, BillingService

## Regra de uso
- Toda ação crítica passa por AuditService
- Middleware de segurança adiciona contexto (IP / user-agent)

## Status atual
- model existente
- logs de login e registro feitos no `auth/service.py`
- falta centralizar em AuditService: implementação próxima
