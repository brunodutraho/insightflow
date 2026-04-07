# DATABASE

## Tabelas principais

### users
Descrição: representa usuários da plataforma
Campos:
- id (UUID)
- email
- hashed_password
- full_name
- phone
- country
- state
- company_name
- team_size
- how_heard
- terms_accepted
- email_verified
- status (active, pending_invite, blocked, inactive)
- role (admin_master, admin_operacional, gestor, cliente)
- tenant_id (UUID)
- manager_id (UUID)
- created_at
- updated_at
- last_login
Relacionamentos:
- pertence a tenant
- pode ter manager / managed_users

### tenants
Descrição: loja/empresa da conta multi-tenant
Campos:
- id (UUID)
- name
- owner_id (UUID)
- created_at
- updated_at
- last_activity_at
Relacionamentos:
- tem usuários
- tem assinaturas
- tem métricas

### permissions
Descrição: permissões granulares de ações
Campos:
- id (UUID)
- user_id (UUID)
- permission (string)
- created_at
Relacionamentos:
- pertence a usuário

### plans
Descrição: planos de cobrança com limites
Campos:
- id (UUID)
- name
- price
- max_users
- max_clients
- max_campaigns
- emails_per_day
- whatsapp_enabled
- is_active
- created_at
- updated_at
Relacionamentos:
- tem subscriptions

### subscriptions
Descrição: vincula tenant ao plano ativo
Campos:
- id (UUID)
- created_at
- canceled_at
- user_id (UUID)
- tenant_id (UUID)
- plan_id (UUID)
Relacionamentos:
- pertence a user
- pertence a tenant
- pertence a plan

### audit_logs
Descrição: auditabilidade de ações críticas
Campos:
- id (UUID)
- user_id (UUID)
- action
- details
- ip_address
- user_agent
- created_at

### email_verification_tokens
Descrição: tokens para verificar email
Campos:
- id (UUID)
- user_id (UUID)
- token
- expires_at
- used_at
- created_at

### password_reset_tokens
Descrição: tokens para resetar senha
Campos:
- id (UUID)
- user_id (UUID)
- token
- expires_at
- used_at
- created_at

### invite_tokens
Descrição: tokens de convite de usuário
Campos:
- id (UUID)
- user_id (UUID)
- token
- expires_at
- used_at
- created_at

### Comentário
Todas as tabelas críticas incluem `tenant_id` medida que garante segregação de dados.  
Fora isto, existem modelos adicionais (ad_account, ad_metric, social_metric, marketing_metric, communication_metric, insight, user_profile, admin_log) que seguem mesmo padrão.