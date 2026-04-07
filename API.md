# API

## Auth
- POST /auth/login
  - input: { email, password }
  - output: { access_token, token_type }
  - erros: 401 invalid credentials, 403 user blocked/pending

- POST /auth/register
  - input: { full_name, email, password, company_name, ... }
  - output: user data + token flows

- POST /auth/verify-email
  - input: { token }
  - output: success message

- POST /auth/request-password-reset
  - input: { email }

- POST /auth/reset-password
  - input: { token, new_password }

- POST /auth/invite-user
  - input: { email, role, tenant_id }

- POST /auth/accept-invite
  - input: { token, password }

## Admin
- GET /admin/users
- POST /admin/users/{id}/block
- POST /admin/users/{id}/reset-password
- GET /admin/clients
- etc.

## Metrics
- GET /kpi?client_id=...
- GET /score?client_id=...
- GET /social/metrics?client_id=...

## Campaign/Insight
- GET/POST /insights
- GET /ad-accounts

## Regras de contrato
- JWT no header `Authorization: Bearer ...`
- Erros comuns: 401 Unauthorized, 403 Forbidden, 404 Not Found

## Notas
Documentar cada rota com input/output/erros requer leitura de `routers/*.py`. O direcionamento acima garante base mínima do contrato.
