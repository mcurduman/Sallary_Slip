"""enums

Revision ID: da968855fee0
Revises: 35f68a14e007
Create Date: 2025-11-04 12:19:21.572461

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = 'da968855fee0'
down_revision: Union[str, Sequence[str], None] = '35f68a14e007'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # CalculationMethod enum
    op.execute("""
        ALTER TYPE calculationmethod RENAME TO calculationmethod_old;
        CREATE TYPE calculationmethod AS ENUM ('FIXED', 'PERCENTAGE', 'PER_DAY', 'PER_MEAL');
        ALTER TABLE emp_benefit ALTER COLUMN calculation_method TYPE calculationmethod USING calculation_method::text::calculationmethod;
        ALTER TABLE emp_deduction ALTER COLUMN calculation_method TYPE calculationmethod USING calculation_method::text::calculationmethod;
        DROP TYPE calculationmethod_old;
    """)

    # DeductionType enum
    op.execute("""
        ALTER TYPE deductiontype RENAME TO deductiontype_old;
        CREATE TYPE deductiontype AS ENUM ('TAX', 'HEALTH', 'PENSION', 'OTHER');
        ALTER TABLE emp_deduction ALTER COLUMN type TYPE deductiontype USING type::text::deductiontype;
        DROP TYPE deductiontype_old;
    """)

    # Periodicity enum
    op.execute("""
        ALTER TYPE periodicity RENAME TO periodicity_old;
        CREATE TYPE periodicity AS ENUM ('MONTHLY', 'DAILY', 'ONCE');
        ALTER TABLE emp_benefit ALTER COLUMN periodicity TYPE periodicity USING periodicity::text::periodicity;
        ALTER TABLE emp_deduction ALTER COLUMN periodicity TYPE periodicity USING periodicity::text::periodicity;
        DROP TYPE periodicity_old;
    """)


def downgrade() -> None:
    """Downgrade schema."""
    # No downgrade logic provided for enum value changes
    pass
    # ### end Alembic commands ###
