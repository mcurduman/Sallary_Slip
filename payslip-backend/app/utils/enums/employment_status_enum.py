from enum import Enum

class EmploymentStatus(str, Enum):
    ACTIVE = "active"
    TERMINATED = "terminated"
    RETIRED = "retired"
    RESIGNED = "resigned"
    SUSPENDED = "suspended"
    OTHER = "other"
