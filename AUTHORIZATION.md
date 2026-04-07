# AUTHORIZATION

## Roles definidas
- admin_master
- admin_operacional
- gestor
- cliente

## Permissões
- users.create
- users.delete
- billing.manage
- campaign.send
- metrics.view_all
- metrics.view_own
- tenants.manage
- roles.assign

## Regra
- Role → várias Permissions
- Usuário ganha permissões via`Permission` model ou role presets

## Aplicação em FastAPI
- `require_roles(allowed_roles)` dependência em rotas (p.ex. admin only)
- `require_permission('users.create')` (se implementado) via middleware / dependency

## Exemplo
- `admin_master`: todas as permissões
- `admin_operacional`: users.create, users.delete, billing.manage, metrics.view_all
- `gestor`: campaign.send, metrics.view_own, users.create (subordinado)
- `cliente`: metrics.view_own

## Recomendação
- criar `PermissionService.has_permission(user, perm)` para validação central
- usar `@router.post(..., dependencies=[Depends(require_permission('...'))])`

## Todos os checks em runtime
1. Atualizar roles no JWT
2. Verificar role em `get_current_user`
3. if role != allowed: 403
