from enum import Enum

class EmploymentStatus(str, Enum):
    ACTIVE = "ACTIVE"
    TERMINATED = "TERMINATED"
    RETIRED = "RETIRED"
    RESIGNED = "RESIGNED"
    SUSPENDED = "SUSPENDED"
    OTHER = "OTHER"
