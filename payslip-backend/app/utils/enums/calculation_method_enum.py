import enum

class CalculationMethod(enum.Enum):
    FIXED = "fixed"
    PERCENTAGE = "percentage"
    PER_DAY = "per_day"
    PER_MEAL = "per_meal"
