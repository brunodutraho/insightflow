from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = 'd2e527ba5892'
down_revision: Union[str, Sequence[str], None] = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    # 🔹 EXTENSION UUID
    op.execute('CREATE EXTENSION IF NOT EXISTS "pgcrypto";')

    # 🔹 ENUMS (ATUALIZADOS PARA BATER COM O SEU MODELO ATUAL)
    user_status = sa.Enum('active', 'pending_invite', 'blocked', 'inactive', name='userstatus')
    # Use exatamente os nomes que estão no seu arquivo app/models/user.py
    user_role = sa.Enum(
        'admin_master', 'gerente', 'administrativo', 
        'suporte', 'marketing', 'gestor_interno', 
        'gestor_assinante', 'cliente_final', 
        name='userrole'
    )

    user_status.create(op.get_bind(), checkfirst=True)
    user_role.create(op.get_bind(), checkfirst=True)

    # 🔹 TENANTS
    op.create_table(
        'tenants',
        sa.Column('id', sa.UUID(), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('owner_id', sa.UUID(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
    )

    # 🔹 USERS
    op.create_table(
        'users',
        sa.Column('id', sa.UUID(), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('email', sa.String(), nullable=False, unique=True),
        sa.Column('hashed_password', sa.String(), nullable=False),
        sa.Column('full_name', sa.String()),
        sa.Column('phone', sa.String()),
        sa.Column('email_verified', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('status', user_status, nullable=False),
        sa.Column('role', user_role, nullable=False),
        sa.Column('tenant_id', sa.UUID(), nullable=False),
        sa.Column('manager_id', sa.UUID()),
        sa.Column('last_login', sa.DateTime(timezone=True)),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.ForeignKeyConstraint(['tenant_id'], ['tenants.id']),
        sa.ForeignKeyConstraint(['manager_id'], ['users.id']),
    )

    # 🔹 LINK OWNER → USERS
    op.create_foreign_key('fk_tenant_owner', 'tenants', 'users', ['owner_id'], ['id'])

    # 🔹 TOKENS
    for table in ['email_verification_tokens', 'password_reset_tokens', 'invite_tokens']:
        op.create_table(
            table,
            sa.Column('id', sa.UUID(), primary_key=True, server_default=sa.text('gen_random_uuid()')),
            sa.Column('user_id', sa.UUID(), nullable=False),
            sa.Column('token', sa.String(), nullable=False, unique=True),
            sa.Column('expires_at', sa.DateTime(timezone=True), nullable=False),
            sa.Column('used_at', sa.DateTime(timezone=True)),
            sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
            sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        )

    # 🔹 PLANS
    op.create_table(
        'plans',
        sa.Column('id', sa.UUID(), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('price', sa.Numeric(10, 2), nullable=False),
        sa.Column('tenant_id', sa.UUID(), nullable=False),
        sa.ForeignKeyConstraint(['tenant_id'], ['tenants.id']),
    )

    # 🔹 SUBSCRIPTIONS
    op.create_table(
        'subscriptions',
        sa.Column('id', sa.UUID(), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('tenant_id', sa.UUID(), nullable=False),
        sa.Column('user_id', sa.UUID(), nullable=False),
        sa.Column('plan_id', sa.UUID()),
        sa.Column('is_active', sa.Boolean(), server_default='true'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.ForeignKeyConstraint(['tenant_id'], ['tenants.id']),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.ForeignKeyConstraint(['plan_id'], ['plans.id']),
    )

    # 🔹 MARKETING METRICS (ADICIONADA PARA RESOLVER O ERRO DE COLETA)
    op.create_table(
        'marketing_metrics',
        sa.Column('id', sa.UUID(), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('tenant_id', sa.UUID(), nullable=False),
        sa.Column('platform', sa.String(), nullable=False),
        sa.Column('impressions', sa.Integer(), server_default='0'),
        sa.Column('clicks', sa.Integer(), server_default='0'),
        sa.Column('spend', sa.Float(), server_default='0'),
        sa.Column('conversions', sa.Integer(), server_default='0'),
        sa.Column('date', sa.Date(), nullable=False),
        sa.ForeignKeyConstraint(['tenant_id'], ['tenants.id']),
    )

def downgrade() -> None:
    op.drop_table('marketing_metrics')
    op.drop_table('subscriptions')
    op.drop_table('plans')
    op.drop_table('users')
    op.drop_table('tenants')
    # ... remover enums se necessário
