import enum

class CalculationMethod(str, enum.Enum):
    FIXED = "FIXED"
    PERCENTAGE = "PERCENTAGE"
    PER_DAY = "PER_DAY"
    PER_MEAL = "PER_MEAL"
