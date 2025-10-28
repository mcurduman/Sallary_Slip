# | PayrollID | INT | Primary Key | Unique ID for this specific payslip/pay run. |
# | EmployeeID | INT | Foreign Key | The employee who received the pay. |
# | PayPeriodStart | DATE | NOT NULL | Start date of the pay cycle e.g., first of the month. |
# | PayPeriodEnd | DATE | NOT NULL | End date of the pay cycle e.g., last of the month. |
# | GrossPay | DECIMAL10, 2 | NOT NULL | Total earnings before any deductions. |
# | TotalDeductions | DECIMAL10, 2 | NOT NULL | Total amount deducted taxes, funds, etc.. |
# | NetPay | DECIMAL10, 2 | NOT NULL | The final take-home amount Gross – Deductions. |
# | RunDate | DATETIME | NOT NULL | When the payroll was actually processed. |
# | ProcessedByUserID | INT | Foreign Key | Links to tbl_User for audit trail. |