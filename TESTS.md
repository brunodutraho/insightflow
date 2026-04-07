# TESTS

## O que testar
- Login válido/inválido
- Registro novo
- Verificação de email (token válido/expirado/usado)
- Reset de senha (fluxo completo)
- Convite (criação/aceite)
- Permissões (você deve negar e permitir com roles)
- Multi-tenant (acesso cross-tenant proibido)

## Estrutura sugerida
- `backend/tests/test_auth.py`
- `backend/tests/test_users.py`
- `backend/tests/test_tenant.py`
- `backend/tests/test_billing.py`
- `backend/tests/test_audit.py`

## Ferramentas
- pytest
- SQLAlchemy SQLite in-memory para speed
- TestClient (FastAPI)

## Exemplos
- assert response.status_code == 200
- assert auth service retorna token
- assert usuário with wrong tenant recebe 403
- assert plan limit bloqueia criação de user
