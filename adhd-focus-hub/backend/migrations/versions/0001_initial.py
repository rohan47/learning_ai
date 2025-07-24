"""initial tables"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('username', sa.String(length=100), nullable=False, unique=True),
        sa.Column('hashed_password', sa.String(length=256), nullable=False),
        sa.Column('created_at', sa.DateTime, nullable=False),
    )
    op.create_table(
        'tasks',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('owner_id', sa.Integer, sa.ForeignKey('users.id')),
        sa.Column('title', sa.String(length=200)),
        sa.Column('description', sa.String(length=1000)),
        sa.Column('completed', sa.Boolean, default=False),
        sa.Column('created_at', sa.DateTime, nullable=False),
    )
    op.create_table(
        'mood_logs',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('owner_id', sa.Integer, sa.ForeignKey('users.id')),
        sa.Column('mood_score', sa.Integer),
        sa.Column('notes', sa.String(length=1000)),
        sa.Column('created_at', sa.DateTime, nullable=False),
    )


def downgrade() -> None:
    op.drop_table('mood_logs')
    op.drop_table('tasks')
    op.drop_table('users')
