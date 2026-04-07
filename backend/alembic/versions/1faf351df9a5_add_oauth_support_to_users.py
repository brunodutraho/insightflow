"""add oauth support to users

Revision ID: 1faf351df9a5
Revises: d2e527ba5892
Create Date: 2026-04-01 16:48:42.656763
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1faf351df9a5'
down_revision: Union[str, Sequence[str], None] = 'd2e527ba5892'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    # =========================
    # PERMISSIONS
    # =========================
    op.add_column('permissions', sa.Column('name', sa.String(), nullable=False))
    op.add_column('permissions', sa.Column('description', sa.String(), nullable=True))
    op.create_index(op.f('ix_permissions_name'), 'permissions', ['name'], unique=True)

    op.drop_constraint(op.f('permissions_user_id_fkey'), 'permissions', type_='foreignkey')
    op.drop_column('permissions', 'user_id')
    op.drop_column('permissions', 'permission')

    # =========================
    # PLANS
    # =========================
    op.add_column('plans', sa.Column('description', sa.String(), nullable=True))
    op.add_column('plans', sa.Column('currency', sa.String(), nullable=True))
    op.add_column('plans', sa.Column('tenant_id', sa.UUID(), nullable=True))  # 👈 SAFE FIRST

    op.alter_column('plans', 'price',
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        type_=sa.Numeric(precision=10, scale=2),
        existing_nullable=False
    )

    op.drop_constraint(op.f('plans_name_key'), 'plans', type_='unique')
    op.create_foreign_key(None, 'plans', 'tenants', ['tenant_id'], ['id'])

    # ⚠️ NÃO REMOVEMOS CAMPOS ANTIGOS PARA NÃO QUEBRAR NADA

    # =========================
    # USER PERMISSIONS
    # =========================
    op.drop_constraint(op.f('user_permissions_user_id_fkey'), 'user_permissions', type_='foreignkey')
    op.drop_constraint(op.f('user_permissions_permission_id_fkey'), 'user_permissions', type_='foreignkey')

    op.create_foreign_key(None, 'user_permissions', 'users', ['user_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'user_permissions', 'permissions', ['permission_id'], ['id'], ondelete='CASCADE')

    # =========================
    # USERS (🔥 PARTE CRÍTICA)
    # =========================

    # 1. Criar ENUM
    authprovider = sa.Enum('local', 'google', 'microsoft', 'apple', name='authprovider')
    authprovider.create(op.get_bind(), checkfirst=True)

    # 2. Criar coluna permitindo NULL
    op.add_column('users', sa.Column('provider', authprovider, nullable=True))

    # 3. Popular dados existentes
    op.execute("UPDATE users SET provider = 'local' WHERE provider IS NULL")

    # 4. Agora sim tornar NOT NULL
    op.alter_column('users', 'provider', nullable=False)

    # 5. provider_id
    op.add_column('users', sa.Column('provider_id', sa.String(), nullable=True))

    # 6. senha opcional
    op.alter_column('users', 'hashed_password',
        existing_type=sa.VARCHAR(),
        nullable=True
    )

    # 7. index
    op.create_index(op.f('ix_users_provider_id'), 'users', ['provider_id'], unique=False)

    # ⚠️ NÃO REMOVEMOS COLUNAS ANTIGAS (segurança total)


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_index(op.f('ix_users_provider_id'), table_name='users')

    op.alter_column('users', 'hashed_password',
        existing_type=sa.VARCHAR(),
        nullable=False
    )

    op.drop_column('users', 'provider_id')
    op.drop_column('users', 'provider')

    authprovider = sa.Enum('local', 'google', 'microsoft', 'apple', name='authprovider')
    authprovider.drop(op.get_bind(), checkfirst=True)

    op.drop_constraint(None, 'user_permissions', type_='foreignkey')
    op.drop_constraint(None, 'user_permissions', type_='foreignkey')

    op.create_foreign_key(op.f('user_permissions_permission_id_fkey'), 'user_permissions', 'permissions', ['permission_id'], ['id'])
    op.create_foreign_key(op.f('user_permissions_user_id_fkey'), 'user_permissions', 'users', ['user_id'], ['id'])

    op.drop_constraint(None, 'plans', type_='foreignkey')

    op.alter_column('plans', 'price',
        existing_type=sa.Numeric(precision=10, scale=2),
        type_=sa.DOUBLE_PRECISION(precision=53),
        existing_nullable=False
    )

    op.drop_column('plans', 'tenant_id')
    op.drop_column('plans', 'currency')
    op.drop_column('plans', 'description')

    op.add_column('permissions', sa.Column('permission', sa.VARCHAR(), nullable=False))
    op.add_column('permissions', sa.Column('user_id', sa.UUID(), nullable=False))

    op.create_foreign_key(op.f('permissions_user_id_fkey'), 'permissions', 'users', ['user_id'], ['id'])

    op.drop_index(op.f('ix_permissions_name'), table_name='permissions')

    op.drop_column('permissions', 'description')
    op.drop_column('permissions', 'name')