import mailtrap as mt
from app.core.config import get_settings
from app.utils.enums.sending_type_enum import SendingType

def get_client(type_: SendingType) -> mt.MailtrapClient:
    if type_ == SendingType.DEFAULT:
        return mt.MailtrapClient(token=get_settings().mail.PASSWORD.get_secret_value())
    elif type_ == SendingType.BULK:
        return mt.MailtrapClient(token=get_settings().mail.PASSWORD.get_secret_value(), bulk=True)
    raise ValueError(f"Invalid sending type: {type_}")

