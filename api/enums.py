from enum import Enum


class StrEnum(str, Enum):
    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name


class EnvEnum(StrEnum):
    DEV: str = "dev"
    STAGGING: str = "stagging"
    PROD: str = "prod"


class ResponseStatusEnum(StrEnum):
    PENDING: str = "pending"
    ASSIGNED: str = "assigned"
    COMPLETED: str = "completed"
    ERROR: str = "error"
