"""add handled_by_user_id field to request model

Revision ID: eb5a578477a5
Revises: cc9719145cb8
Create Date: 2024-10-21 22:38:08.295980

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'eb5a578477a5'
down_revision: Union[str, None] = 'cc9719145cb8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('requests', sa.Column('handled_by_user_id', sa.Uuid(), nullable=True))
    op.alter_column('requests', 'status',
               existing_type=postgresql.ENUM('ACCEPTED', 'DECLINED', 'PENDING', name='requeststatus'),
               nullable=True)
    op.create_foreign_key(None, 'requests', 'users', ['handled_by_user_id'], ['id'])
    op.alter_column('users', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True,
               existing_server_default=sa.text('now()'))
    op.alter_column('users', 'edited_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True,
               existing_server_default=sa.text('now()'))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'edited_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False,
               existing_server_default=sa.text('now()'))
    op.alter_column('users', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False,
               existing_server_default=sa.text('now()'))
    op.drop_constraint(None, 'requests', type_='foreignkey')
    op.alter_column('requests', 'status',
               existing_type=postgresql.ENUM('ACCEPTED', 'DECLINED', 'PENDING', name='requeststatus'),
               nullable=False)
    op.drop_column('requests', 'handled_by_user_id')
    # ### end Alembic commands ###
