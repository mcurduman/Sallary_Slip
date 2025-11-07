import base64
from io import BytesIO
import mailtrap as mt
from pydantic import EmailStr
from app.core.config import get_settings
from app.utils.email import get_client
from app.utils.enums.sending_type_enum import SendingType


class MailService:
    def _initialize_template_variables(self, month, sent_date, name):
        template_variables={
                "company_info_name":  get_settings().mail.COMPANY_NAME,
                "company_info_address": get_settings().mail.COMPANY_ADDRESS,
                "company_info_city":   get_settings().mail.COMPANY_CITY,
                "company_info_zip_code": get_settings().mail.COMPANY_ZIP_CODE,
                "company_info_country": get_settings().mail.COMPANY_COUNTRY,
                "sent_date": sent_date,
                "month": sent_date,
                "name": name
        }
        return template_variables
    
    def create_batch(self, month, sent_date, recipients) -> mt.BatchSendEmailParams:
        # 1) Base template
        base = mt.BatchMailFromTemplate(
            sender=mt.Address(
                email=get_settings().mail.DEFAULT_SENDER,
                name="PaySlip Service",
            ),
            template_uuid=get_settings().mail.TEMPLATE_UUID,
        )

        requests = []
        for r in recipients:
            pdf_b64_bytes = r.pdf_b64.encode("ascii")
            requests.append(
                mt.BatchEmailRequest(
                    to=[mt.Address(email=r.email, name=r.name or "Employee")],
                    template_variables=self._initialize_template_variables(month,sent_date,r.name),
                    attachments=[
                        mt.Attachment(
                            filename=f"Payslip_{r.name}_{month}.pdf",
                            content=pdf_b64_bytes,       # base64 BYTES
                            mimetype="application/pdf",
                            disposition=mt.Disposition.ATTACHMENT,
                        )
                    ],
                )
            )

        return mt.BatchSendEmailParams(base=base, requests=requests)

    def send_batch_email(self, month, sent_date, recipients) -> mt.BATCH_SEND_ENDPOINT_RESPONSE:
        client = get_client(SendingType.BULK)
        return client.batch_send(self.create_batch(month, sent_date, recipients))

    def send_single_email(self, manager_email: EmailStr, name: str, sent_date: str, month: str, file: BytesIO) -> mt.SEND_ENDPOINT_RESPONSE:
        client = get_client(SendingType.DEFAULT)
        encoded_csv = base64.b64encode(file.getvalue()).decode("utf-8")
        mail = mt.MailFromTemplate(
            sender=mt.Address(
                email=get_settings().mail.DEFAULT_SENDER,
                name="PaySlip Service",
            ),
            to=[mt.Address(email=manager_email, name=name)],
            template_uuid=get_settings().mail.TEMPLATE_UUID_SINGLE,
            template_variables=self._initialize_template_variables(month, sent_date, name),
            attachments=[
                mt.Attachment(
                    filename="employee_report.csv",
                    mimetype="text/csv",
                    content=encoded_csv
                )
            ],
        )
        return client.send(mail)
    