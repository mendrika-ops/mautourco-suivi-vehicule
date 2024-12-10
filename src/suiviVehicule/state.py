from enum import Enum

class State(Enum):
    CREATED = 1
    SCHEDULED = 2
    CONFIRMED = 3
    IN_PROGRESS = 4
    COMPLETED = 5
    CANCELED = 0
    CANCELED_TRIP = 6
    WAITING = 7
    