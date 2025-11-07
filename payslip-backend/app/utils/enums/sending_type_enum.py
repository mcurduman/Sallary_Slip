from enum import Enum

class SendingType(str, Enum):
    DEFAULT = "DEFAULT"
    BULK = "BULK"
    SANDBOX = "SANDBOX"
