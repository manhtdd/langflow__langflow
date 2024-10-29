"""event_error

Revision ID: 1eab2c3eb45e
Revises: eb5e72293a8e
Create Date: 2024-10-24 12:03:24.118937

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.engine.reflection import Inspector
from sqlalchemy.dialects import sqlite

# revision identifiers, used by Alembic.
revision: str = '1eab2c3eb45e'
down_revision: Union[str, None] = 'eb5e72293a8e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()
    inspector = Inspector.from_engine(conn)  # type: ignore
    table_names = inspector.get_table_names()  # noqa
    column_names = [column["name"] for column in inspector.get_columns("message")]
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('message', schema=None) as batch_op:
        if "meta_data" not in column_names:
            batch_op.add_column(sa.Column('meta_data', sa.JSON(), nullable=True))
        if "category" not in column_names:
            batch_op.add_column(sa.Column('category', sa.Text(), nullable=True))
        if "content_blocks" not in column_names:
            batch_op.add_column(sa.Column('content_blocks', sa.JSON(), nullable=True))

    # ### end Alembic commands ###


def downgrade() -> None:
    conn = op.get_bind()
    inspector = Inspector.from_engine(conn)  # type: ignore
    table_names = inspector.get_table_names()  # noqa
    column_names = [column["name"] for column in inspector.get_columns("message")]
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('message', schema=None) as batch_op:
        if "content_blocks" in column_names:
            batch_op.drop_column('content_blocks')
        if "category" in column_names:
            batch_op.drop_column('category')
        if "meta_data" in column_names:
            batch_op.drop_column('meta_data')

    # ### end Alembic commands ###