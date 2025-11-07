from enum import Enum

class DeductionType(str, Enum):
    TAX = "TAX"
    HEALTH = "HEALTH"
    PENSION = "PENSION"
    OTHER = "OTHER"
