from pydantic import BaseModel
from typing import List
from app.schemas.email.recipient import Recipient

class SalaryBatch(BaseModel):
    recipients: List[Recipient]
    base_vars: dict = {}
    company_info_name: str = "FakeCompany"
    company_info_address: str = "1234 Fake St, Faketown, FK 12345"
    company_info_country: str = "Fakeland"
    company_info_city: str = "Faketown"
    company_info_zip_code: str = "12345"
    sent_date: str = ""  # e.g., "March 2024"
    month: str = ""      # e.g., "March"