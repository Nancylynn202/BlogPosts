"""Update post-user relationship

Revision ID: 01d9fa20ff20
Revises: 5598007a9d0a
Create Date: 2022-10-04 21:49:45.049802

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '01d9fa20ff20'
down_revision = '5598007a9d0a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posts', sa.Column('author_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'posts', 'users', ['author_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'posts', type_='foreignkey')
    op.drop_column('posts', 'author_id')
    # ### end Alembic commands ###
