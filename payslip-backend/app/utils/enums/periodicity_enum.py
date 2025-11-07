import enum

class Periodicity(str, enum.Enum):
    MONTHLY = "MONTHLY"
    DAILY = "DAILY"
    ONCE = "ONCE"
