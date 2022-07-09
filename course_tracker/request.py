from enum import Enum, auto

# Represents the possible types that a CourseRequest can be
class RequestType(Enum):
    TRACK = auto()
    UNTRACK = auto()

# Represents a request to manipulate tracking.json
class CourseRequest:
    def __init__(self, type: RequestType, crn: str, subject: str, authorID: str) -> None:
        self.type = type
        self.crn = crn
        self.subject = subject
        self.authorID = authorID