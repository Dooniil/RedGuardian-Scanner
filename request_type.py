from enum import Enum


class RequestType(Enum):
    KEY = 0
    SAVE_TASK = 1
    RUN_TASK = 2
    ERROR = 3
    RESULT = 4
