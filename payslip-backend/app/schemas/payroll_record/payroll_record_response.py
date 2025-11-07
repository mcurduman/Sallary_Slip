from pydantic import BaseModel

class PayrollRecordResponse(BaseModel):
    run_date: str
    payroll_month: int
    payroll_year: int
