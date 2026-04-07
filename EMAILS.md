# EMAILS

## Tipos de email
- Verificação de email
- Reset de senha
- Convite de usuário

## Conteúdo
### Verificação
- assunto: "Confirme seu email"
- CTA: /auth/verify-email?token=...
- expiração: 24h

### Reset de senha
- assunto: "Redefina sua senha"
- CTA: /auth/reset-password?token=...
- expiração: 1h

### Convite
- assunto: "Você foi convidado para InsightFlow"
- CTA: /auth/accept-invite?token=...
- expiração: 24h

## Provedor
- Atualmente placeholders (mock) no serviço de email (dependência de integração futura)
- Reenvio: endpoint de reenvio de token (POST /auth/resend-verification)

## Regras
- token único (used_at)
- expira corretamente
- inválido retorna 400
