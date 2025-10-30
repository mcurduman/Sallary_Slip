import enum

class CalculationMethod(enum.Enum):
    fixed = "fixed"
    percentage = "percentage"
    per_day = "per_day"
    per_meal = "per_meal"
