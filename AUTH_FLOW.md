# AUTH_FLOW

## 1. Login
1. POST /auth/login (email + password)
2. Service valida dados
3. Verifica status diferente de blocked/inactive
4. Verifica `email_verified == true`
5. Gera JWT com payload: `sub`, `role`, `tenant_id`
6. Registra audit log `user_login`

## 2. Registro
1. POST /auth/register
2. Verifica se email existe
3. Cria `Tenant` (empresa)
4. Cria `User` com status `pending_invite` e role `gestor`
5. Associa `tenant_id` ao usuário
6. Cria token de verificação em `email_verification_tokens`
7. Envia email de verificação (placeholder no serviço de email)
8. Registra audit log `user_registered`

## 3. Verificação de email
1. POST /auth/verify-email token
2. Busca token em `email_verification_tokens`
3. Verifica expiração e se `used_at` é nulo
4. Marca `used_at`, define `email_verified=true`, status `active`
5. Responde com sucesso e atualiza audit log

## 4. Reset de senha
1. POST /auth/request-password-reset (email)
2. Cria token em `password_reset_tokens` com expiração 1h
3. Envia email com link
4. POST /auth/reset-password (token, nova senha)
5. Valida token (não usado e não expirado)
6. Atualiza `User.hashed_password`, marca `used_at`
7. Audit log `password_reset`

## 5. Convite
1. POST /auth/invite-user (gestor/admin)
2. Cria usuário com `status=pending_invite`, sem senha ou hashed password default com token
3. Cria `invite_tokens` com expiração 24h
4. Envia email com link de ativação
5. Quando usuário aceita:
   - POST /auth/accept-invite (token, senha)
   - Valida expiração/uso do token
   - Define senha, `email_verified=true`, status `active`
   - Audit log `invite_accepted`

## Notas gerais
- Tokens possuem expiração explícita e uso único
- Regras de autenticação estão centralizadas em `app/auth/service.py` e `app/auth/dependencies.py`