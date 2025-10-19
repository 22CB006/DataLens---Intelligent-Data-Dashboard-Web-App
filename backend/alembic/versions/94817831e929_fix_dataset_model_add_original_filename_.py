"""fix dataset model - add original_filename and file_type

Revision ID: 94817831e929
Revises: da1e6f31fb79
Create Date: 2025-10-19 21:26:09.546174

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '94817831e929'
down_revision = 'da1e6f31fb79'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add original_filename column if it doesn't exist
    op.add_column('datasets', sa.Column('original_filename', sa.String(length=255), nullable=True))
    
    # Add file_type column if it doesn't exist
    op.add_column('datasets', sa.Column('file_type', sa.String(length=50), nullable=True))
    
    # Update existing records with placeholder values
    op.execute("UPDATE datasets SET original_filename = filename WHERE original_filename IS NULL")
    op.execute("UPDATE datasets SET file_type = 'csv' WHERE file_type IS NULL")
    
    # Make columns non-nullable after populating
    op.alter_column('datasets', 'original_filename', nullable=False)
    op.alter_column('datasets', 'file_type', nullable=False)
    
    # Add index on filename for faster lookups
    op.create_index('ix_datasets_filename', 'datasets', ['filename'], unique=False)


def downgrade() -> None:
    # Remove index
    op.drop_index('ix_datasets_filename', table_name='datasets')
    
    # Remove columns
    op.drop_column('datasets', 'file_type')
    op.drop_column('datasets', 'original_filename')
