import base64
from io import BytesIO
import mailtrap as mt
from reportlab.pdfgen import canvas

from app.schemas.email.salary_batch import SalaryBatch
from app.core.config import get_settings
from app.utils.email import get_client
from app.utils.enums.sending_type_enum import SendingType
from app.schemas.email.recipient import Recipient


class EmailService:
    def create_batch(self, salary_batch: SalaryBatch) -> mt.BatchSendEmailParams:
        # 1) Base template
        base = mt.BatchMailFromTemplate(
            sender=mt.Address(
                email=get_settings().mail.DEFAULT_SENDER,
                name="PaySlip Service",
            ),
            template_uuid=get_settings().mail.TEMPLATE_UUID,
        )

        # 2) Per-recipient requests
        requests = []
        for r in salary_batch.recipients:
            # Important: Mailtrap examples pass Base64 **bytes**
            pdf_b64_bytes = r.pdf_b64.encode("ascii")

            requests.append(
                mt.BatchEmailRequest(
                    to=[mt.Address(email=r.email, name=r.name or "Employee")],
                    template_variables={
                        "company_info_name":  salary_batch.company_info_name,
                        "company_info_address": salary_batch.company_info_address,
                        "company_info_city":   salary_batch.company_info_city,  # <-- your template needs this
                        "company_info_zip_code": salary_batch.company_info_zip_code,
                        "company_info_country": salary_batch.company_info_country,
                        "sent_date": salary_batch.sent_date,
                        "month": salary_batch.month,
                        "name": r.name or "Employee",
                    },
                    attachments=[
                        mt.Attachment(
                            filename="payslip.pdf",
                            content=pdf_b64_bytes,                # base64 BYTES
                            mimetype="application/pdf",
                            disposition=mt.Disposition.ATTACHMENT,
                        )
                    ],
                )
            )

        return mt.BatchSendEmailParams(base=base, requests=requests)

    def send_batch_email(self, salary_batch: SalaryBatch) -> mt.BATCH_SEND_ENDPOINT_RESPONSE:
        client = get_client(SendingType.BULK)
        return client.batch_send(self.create_batch(salary_batch))

# --------- quick test ----------
if __name__ == "__main__":
    # sample PDF
    buf = BytesIO()
    c = canvas.Canvas(buf)
    c.drawString(100, 750, "This is a sample payslip.")
    c.showPage(); c.save()
    pdf_b64 = base64.b64encode(buf.getvalue()).decode("utf-8")

    r1 = Recipient(email="curduman.miruna@gmail.com", name="Miruna Curduman", pdf_b64=pdf_b64)
    r2 = Recipient(email="curduman.miruna02@gmail.com", name="Miruna Curduman", pdf_b64=pdf_b64)

    batch = SalaryBatch(
        recipients=[r1, r2],
        company_info_name="FakeCompany",
        company_info_address="1234 Fake St",
        company_info_city="Faketown",                # <-- REQUIRED
        company_info_zip_code="FK 12345",
        company_info_country="Fakeland",
        sent_date="March 2024",
        month="March"
    )

    svc = EmailService()
    print(svc.send_batch_email(batch))
