from enum import Enum


class EnvEnum(Enum):
    DEV: str = "dev"
    STAGGING: str = "stagging"
    PROD: str = "prod"


class ResponseStatusEnum(Enum):
    PENDING: str = "pending"
    ASSIGNED: str = "assigned"
    COMPLETED: str = "completed"
