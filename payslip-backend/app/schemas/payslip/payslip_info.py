from __future__ import annotations
from pydantic import BaseModel, Field

# ----------------------------
# Pydantic model
# ----------------------------
class PayslipInfo(BaseModel):
    employee_full_name: str = Field(..., alias="employeeFullName")
    employee_national_id: str = Field(..., alias="employeeNationalId")
    employee_position: str = Field(..., alias="employeePosition")
    employee_department: str = Field(..., alias="employeeDepartment")

    employee_base_salary: float = Field(..., alias="employeeBaseSalary")
    employee_net_salary: float = Field(..., alias="employeeNetSalary")
    employee_net_income: float = Field(..., alias="employeeNetIncome")
    employee_base_before_taxes: float = Field(..., alias="employeeBaseBeforeTaxes")

    employee_tax_percentage: float = Field(..., alias="employeeTaxPercentage")
    employee_tax_amount: float = Field(..., alias="employeeTaxAmount")
    employee_health_percent: float = Field(..., alias="employeeHealthPercent")
    employee_health_amount: float = Field(..., alias="employeeHealthAmount")
    employee_pension_amount: float = Field(..., alias="employeePensionAmount")
    employee_pension_percent: float = Field(..., alias="employeePensionPercent")
    employee_other_deductions: float = Field(..., alias="employeeOtherDeductions")

    employee_worked_days: int = Field(..., alias="employeeWorkedDays")
    employee_leave_days: int = Field(..., alias="employeeLeaveDays")

    payroll_year: int = Field(..., alias="payrollYear")
    payroll_month: int = Field(..., alias="payrollMonth")

    employee_meal_ticket_amount: float = Field(..., alias="employeeMealTicketAmount")
    employee_other_benefits: float = Field(..., alias="employeeOtherBenefits")
    employee_bonus_amount: float = Field(..., alias="employeeBonusAmount")