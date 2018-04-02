"""baseline

Revision ID: 0fafd71644fc
Revises: 
Create Date: 2018-04-01 13:43:32.634826

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0fafd71644fc'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    department_type_table = op.create_table(
        'department',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String)
    )

    teacher_type_table = op.create_table(
        'teacher',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String),
        sa.Column('hired_on', sa.DateTime, default=sa.func.now()),
        sa.Column('department_id', sa.Integer, sa.ForeignKey(
            'department.id', ondelete="CASCADE"))
    )

    op.bulk_insert(
        department_type_table,
        [
            {'name': 'Dat Boi'},
            {'name': 'Computer Science'},
            {'name': 'Engineering'}
        ]
    )

    op.bulk_insert(
        teacher_type_table,
        [
            {'name': 'poot', 'department_id': 1},
            {'name': 'david', 'department_id': 2},
            {'name': 'justin', 'department_id': 3}
        ]
    )


def downgrade():
    op.drop_table('department')
    op.drop_table('teacher')
