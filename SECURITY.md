# SECURITY

## Práticas de segurança
- senhas hash com bcrypt/argon2 (implementado em `auth/utils.py`)
- JWT com expiração (`ACCESS_TOKEN_EXPIRE_MINUTES` no settings)
- tokens de uso único para email/reset/invite
- status do usuário e `email_verified` checkados antes do login

## Validações aplicadas
- role check via `require_roles` dependency
- tenant check nas queries de recursos
- bloqueio de usuário via status `blocked`

## Melhorias recomendadas
- rate limit / brute-force protection (dependência futura)
- 2FA (opcional)
- helmet/CORS hardening no FastAPI
- CSP e input sanitization no frontend

## Requisitos implementados
- `is_verified` ou `email_verified` obrigatório
- tokens `expires_at` e `used_at`
- token JWT inclui `sub`, `role`, `tenant_id`
