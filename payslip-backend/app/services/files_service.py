from decimal import Decimal
from io import BytesIO
import os
import aiofiles
from datetime import date
from typing import Optional
from app.schemas.employee.emp_info import EmployeeInfo
from app.db.models.payroll_record import PayrollRecord
from app.schemas.payroll_record.payroll_record_response import PayrollRecordResponse
import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.pdfencrypt import StandardEncryption
from app.core.config import get_settings

class FilesService:
   async def employees_info_to_csv_file(self, employees: list[EmployeeInfo]) -> BytesIO:
       csv_data = [emp.model_dump(mode="json") for emp in employees]
       df = pd.DataFrame(csv_data)
       csv_buffer = BytesIO()
       df.to_csv(csv_buffer, index=False)
       csv_buffer.seek(0)
       return csv_buffer
   
   async def save_upload_file(self, filename, buffer, destination_folder: str):
        os.makedirs(destination_folder, exist_ok=True)
        file_path = os.path.join(destination_folder, filename)
        async with aiofiles.open(file_path, "wb") as out_file:
            await out_file.write(buffer.getvalue())
        return file_path
   
   async def get_file_content(self, file_path: str) -> BytesIO:
       async with aiofiles.open(file_path, "rb") as in_file:
           content = await in_file.read()
       return BytesIO(content)
   
   @staticmethod
   def _format_money(v: float, currency: str = "RON") -> str:
       return f"{v:,.2f} {currency}".replace(",", " ")

   @staticmethod
   def _month_name(m: int) -> str:
        return date(2000, m, 1).strftime("%B")
   
   def _render_employee_details_table(self, info: PayrollRecordResponse) -> Table:
        emp_data = [
              ["Employee", info.employee_full_name, "Position", info.employee_position],
              ["National ID", info.employee_national_id, "Department", info.employee_department],
              ["Worked Days", str(info.employee_worked_days), "Leave Days", str(info.employee_leave_days)],
         ]
        emp_tbl = Table(
              emp_data,
              colWidths=[28 * mm, 70 * mm, 28 * mm, 39 * mm],
              style=TableStyle(
                [
                     ("GRID", (0, 0), (-1, -1), 0.25, colors.lightgrey),
                     ("BACKGROUND", (0, 0), (-1, -1), colors.whitesmoke),
                     ("FONTSIZE", (0, 0), (-1, -1), 9),
                     ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                     ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                     ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#F0F3F5")),
                     ("BACKGROUND", (2, 0), (2, -1), colors.HexColor("#F0F3F5")),
                ]
              ),
         )
        return emp_tbl

   def _render_earnings_table(self, info: PayrollRecordResponse, style, currency: str) -> Table:
            meal_tickets_total = info.employee_worked_days * info.employee_meal_ticket_amount
            total_taxable_benefits = (
                info.employee_bonus_amount
                + info.employee_other_benefits
                + meal_tickets_total
            )
            earnings = [
                ["Item", "Amount"],
                ["Base Salary (A)", FilesService._format_money(info.employee_base_salary, currency)],
                ["Bonus (J)", FilesService._format_money(info.employee_bonus_amount, currency)],
                ["Other Benefits (K)", FilesService._format_money(info.employee_other_benefits, currency)],
                [f"Meal Tickets (L = {info.employee_worked_days} × {FilesService._format_money(info.employee_meal_ticket_amount, currency)})",
                FilesService._format_money(meal_tickets_total, currency)],
                ["Total Taxable Benefits (E=J+K+L)", FilesService._format_money(total_taxable_benefits, currency)],
            ]
    
            earn_tbl = Table(
                earnings,
                colWidths=[120 * mm, 45 * mm],
                style=style
            )
            return earn_tbl
   
   def _render_deductions_table(self, info: PayrollRecordResponse, style, currency: str) -> Table:
        percent = info.employee_tax_percentage / Decimal('100.0') if hasattr(info.employee_tax_percentage, 'as_tuple') else info.employee_tax_percentage / 100.0
        tax_amount = info.employee_base_before_taxes * percent
        deductions = [
            ["Item", "Amount"],
            [f"Health (B = {info.employee_health_percent:.2f}% of A)", FilesService._format_money(info.employee_health_amount, currency)],
            [f"Pension (C = {info.employee_pension_percent:.2f}% of A)", FilesService._format_money(info.employee_pension_amount, currency)],
            [f"Income Tax (G = {info.employee_tax_percentage:.2f}% of F)", FilesService._format_money(tax_amount, currency)],
            ["Other Deductions (X)", FilesService._format_money(info.employee_other_deductions, currency)],
        ]
        ded_tbl = Table(
            deductions,
            colWidths=[120 * mm, 45 * mm],
            style=style
        )
        return ded_tbl
   
   def _render_header(self, info: PayrollRecordResponse, styles) -> Table:
            company = {
                "name": get_settings().mail.COMPANY_NAME,
                "address": get_settings().mail.COMPANY_ADDRESS,
                "city": get_settings().mail.COMPANY_CITY,
                "zip_code": get_settings().mail.COMPANY_ZIP_CODE,
                "country": get_settings().mail.COMPANY_COUNTRY,
            }
            header_left = [
                [Paragraph(f"<b>{company.get('name', '')}</b>", styles["H1"])],
                [Paragraph(f"{company.get('address', '')}", styles["Small"])],
                [Paragraph(f"{company.get('city', '')} {company.get('zip_code', '')}", styles["Small"])],
                [Paragraph(f"{company.get('country', '')}", styles["Small"])],
            ]
            header_right = [
                [Paragraph("<b>Payslip</b>", styles["H1"])],
                [Paragraph(f"Period: {FilesService._month_name(info.payroll_month)} {info.payroll_year}", styles["Body"])],
                [Paragraph(f"Generated: {date.today().isoformat()}", styles["Small"])],
            ]
    
            header_tbl = Table(
                [[Table(header_left, colWidths=[95 * mm]), Table(header_right, colWidths=[70 * mm])]],
                colWidths=[95 * mm, 70 * mm],
                hAlign="LEFT",
                style=TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP")]),
            )
            return header_tbl
   
   def _render_summary_table(self, info: PayrollRecordResponse, style, currency: str) -> Table:
        summary_rows = [
            ["Gross (Base before taxes = A)", FilesService._format_money(info.employee_base_salary, currency)],
            ["Net Income (D=A-B-C-X)", FilesService._format_money(info.employee_net_income, currency)],
            ["Tax Base (F=D+E)", FilesService._format_money(info.employee_base_before_taxes, currency)],
            ["Income Tax Amount (G)", FilesService._format_money(info.employee_tax_amount, currency)],
            ["Net Salary (H= D-G)", FilesService._format_money(info.employee_net_salary, currency)],
        ]
        summary_tbl = Table(
            summary_rows,
            colWidths=[120 * mm, 45 * mm],
            style=style,
        )
        return summary_tbl
   
   def _encryption_settings(self, password: str) -> StandardEncryption:
        encrypt = StandardEncryption(
            userPassword=password,
            ownerPassword=None,
            canPrint=1,
            canModify=0,
            canCopy=0,
            canAnnotate=0
        )
        return encrypt
   
   def _set_styles(self):
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name="H1", parent=styles["Heading1"], fontSize=14, leading=16, spaceAfter=6))
        styles.add(ParagraphStyle(name="H2", parent=styles["Heading2"], fontSize=11, leading=13, spaceBefore=6, spaceAfter=4))
        styles.add(ParagraphStyle(name="Small", parent=styles["Normal"], fontSize=8, textColor=colors.grey))
        styles.add(ParagraphStyle(name="Body", parent=styles["Normal"], fontSize=9, leading=11))
        return styles

   def render_payslip_pdf(self, info: PayrollRecord, *,
                        currency: str = "RON", filename: Optional[str] = None) -> bytes:
        buf = BytesIO()
        encrypt = self._encryption_settings(info.employee_national_id)

        doc = SimpleDocTemplate(
            buf,
            pagesize=A4,
            leftMargin=15 * mm,
            rightMargin=15 * mm,
            topMargin=14 * mm,
            bottomMargin=14 * mm,
            title=f"Payslip {info.payroll_year}-{info.payroll_month:02d}",
            author="PaySlip Service",
            encrypt=encrypt
        )

        styles = self._set_styles()
        flow = []

        # Header
        header_tbl = self._render_header(info, styles)
        flow += [header_tbl, Spacer(1, 6)]

        # Employee Details
        emp_tbl = self._render_employee_details_table(info)
        flow += [Paragraph("Employee Details", styles["H2"]), emp_tbl, Spacer(1, 8)]

        _style = TableStyle(
                    [
                        ("GRID", (0, 0), (-1, -1), 0.25, colors.lightgrey),
                        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E9EEF3")),
                        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                        ("ALIGN", (1, 1), (1, -1), "RIGHT"),
                        ("FONTSIZE", (0, 0), (-1, -1), 9),
                    ]
                )
        # Earnings table
        earn_tbl = self._render_earnings_table(info, _style, currency)
        flow += [Paragraph("Earnings", styles["H2"]), earn_tbl, Spacer(1, 8)]

        # Deductions table
        ded_tbl = self._render_deductions_table(info, _style, currency)
        flow += [Paragraph("Deductions", styles["H2"]), ded_tbl, Spacer(1, 8)]

        # Summary table
        _summary_style=TableStyle( [ ("GRID", (0, 0), (-1, -1), 0.25, colors.lightgrey), 
                                    ("BACKGROUND", (0, 0), (-1, -2), colors.whitesmoke), 
                                    ("BACKGROUND", (0, -1), (-1, -1), colors.HexColor("#DFF0D8")), 
                                    ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"), 
                                    ("ALIGN", (1, 0), (1, -1), "RIGHT"),
                                    ("FONTSIZE", (0, 0), (-1, -1), 10), ] )
        
        summary_tbl = self._render_summary_table(info, _summary_style, currency)
        flow += [Paragraph("Summary", styles["H2"]), summary_tbl]

        # Footer
        flow += [Spacer(1, 12), Paragraph("This payslip is system-generated.", styles["Small"])]

        # Build
        doc.build(flow)
        pdf_bytes = buf.getvalue()
        if filename:
            with open(filename, "wb") as f:
                f.write(pdf_bytes)
        return pdf_bytes