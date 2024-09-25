"""empty message

Revision ID: 6c795f7d95b1
Revises: 1fcdfcaed563
Create Date: 2024-09-15 11:53:48.550251

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6c795f7d95b1'
down_revision = '1fcdfcaed563'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Post',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=40), nullable=False),
    sa.Column('date_posted', sa.DateTime(), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('file', sa.Text(length=100), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['User.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('post')
    with op.batch_alter_table('User', schema=None) as batch_op:
        batch_op.create_unique_constraint(None, ['username'])
        batch_op.create_unique_constraint(None, ['email'])

    with op.batch_alter_table('comment', schema=None) as batch_op:
        batch_op.add_column(sa.Column('date_posted', sa.DateTime(), nullable=False))
        batch_op.add_column(sa.Column('user_id', sa.Integer(), nullable=False))
        batch_op.alter_column('content',
               existing_type=sa.TEXT(),
               nullable=False)
        batch_op.alter_column('post_id',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key(None, 'Post', ['post_id'], ['id'])
        batch_op.create_foreign_key(None, 'User', ['user_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('comment', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key(None, 'post', ['post_id'], ['id'])
        batch_op.alter_column('post_id',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.alter_column('content',
               existing_type=sa.TEXT(),
               nullable=True)
        batch_op.drop_column('user_id')
        batch_op.drop_column('date_posted')

    with op.batch_alter_table('User', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')
        batch_op.drop_constraint(None, type_='unique')

    op.create_table('post',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('title', sa.VARCHAR(length=40), nullable=False),
    sa.Column('date_posted', sa.DATETIME(), nullable=False),
    sa.Column('content', sa.TEXT(), nullable=False),
    sa.Column('user_id', sa.INTEGER(), nullable=False),
    sa.Column('file', sa.TEXT(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['User.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('Post')
    # ### end Alembic commands ###
