from enum import Enum, auto

class RequestType(Enum):
    """Represents the possible types that a CourseRequest can be."""

    TRACK = auto()
    UNTRACK = auto()

class CourseRequest:
    """Represents a request to track or untrack a course.

    Attributes:
        type: The type of request. Represented by 'RequestType'.
        crn: The unique identifier for the course.
        subject: The subject of the course.
        userID: The unique Discord ID for the user who submitted the request.
        username: The Discord username for the user who submitted the request.
    """
    def __init__(self, type: RequestType, crn: int, subject: str, userID: int, username: str) -> None:
        self.type = type
        self.crn = crn
        self.subject = subject
        self.userID = userID
        self.username = username