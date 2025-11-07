from enum import Enum

class BenefitType(str, Enum):
    MEAL = "MEAL"
    TRANSPORT = "TRANSPORT"
    HEALTH = "HEALTH"
    BONUS = "BONUS"
    OTHER = "OTHER"
