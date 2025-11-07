# migrations/versions/8786c03f80c8_employee_benefits_base.py
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql as pg

# Reuse ONE enum object per named type, and keep create_type=False on columns.
calculation_method_enum = pg.ENUM(
    'FIXED', 'PERCENTAGE', 'PER_DAY', 'PER_MEAL',
    name='calculationmethod',
    create_type=False,
)
benefit_type_enum = pg.ENUM(
    'MEAL', 'TRANSPORT', 'HEALTH', 'BONUS', 'OTHER',
    name='benefittype',
    create_type=False,
)
periodicity_enum = pg.ENUM(
    'MONTHLY', 'DAILY', 'ONCE',
    name='periodicity',
    create_type=False,
)

revision = '8786c03f80c8'
down_revision = '3fa58860f259'
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Create types if missing (no-op if they already exist)
    calculation_method_enum.create(op.get_bind(), checkfirst=True)
    benefit_type_enum.create(op.get_bind(), checkfirst=True)
    periodicity_enum.create(op.get_bind(), checkfirst=True)

    op.create_table(
        'emp_benefit',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('employee_id', sa.UUID(), nullable=False),

        # Use the shared enum objects here (no auto-create during table DDL)
        sa.Column('type', benefit_type_enum, nullable=False),
        sa.Column('amount', sa.Numeric(12, 2), nullable=True),
        sa.Column('percentage', sa.Numeric(12, 2), nullable=True),
        sa.Column('calculation_method', calculation_method_enum, nullable=False),
        sa.Column('taxable', sa.Boolean(), nullable=False),
        sa.Column('periodicity', periodicity_enum, nullable=False),

        sa.Column('effective_start_date', sa.Date(), nullable=True),
        sa.Column('effective_end_date', sa.Date(), nullable=True),
        sa.ForeignKeyConstraint(['employee_id'], ['employee.id']),
        sa.PrimaryKeyConstraint('id'),
    )

def downgrade() -> None:
    op.drop_table('emp_benefit')

    # Only drop types if they were introduced by THIS migration.
    # If other tables also use them, dropping will fail — so safest is to skip dropping,
    # or wrap in DO blocks that only drop when unused. Easiest safe option: do nothing.
    # If you know these are exclusive to this table, you can uncomment:
    #
    # calculation_method_enum.drop(op.get_bind(), checkfirst=True)
    # benefit_type_enum.drop(op.get_bind(), checkfirst=True)
    # periodicity_enum.drop(op.get_bind(), checkfirst=True)
