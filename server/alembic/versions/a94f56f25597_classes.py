"""classes

Revision ID: a94f56f25597
Revises: 0fafd71644fc
Create Date: 2018-04-02 12:12:24.249422

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a94f56f25597'
down_revision = '0fafd71644fc'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'subject',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String),
        sa.Column('department_id', sa.Integer, sa.ForeignKey(
            'department.id', ondelete="CASCADE")),

    )
    op.create_table(
        'session',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String),
        sa.Column('room', sa.Integer),
        sa.Column('department_id', sa.Integer, sa.ForeignKey(
            'department.id', ondelete="CASCADE")),
        sa.Column('subject_id', sa.Integer, sa.ForeignKey(
            'subject.id', ondelete="CASCADE")),
        sa.Column('teacher_id', sa.Integer, sa.ForeignKey(
            'teacher.id', ondelete="CASCADE"
        )),
        sa.Column('total_students', sa.Integer)
    )


def downgrade():
    op.drop_table('session')
    op.drop_table('subject')
