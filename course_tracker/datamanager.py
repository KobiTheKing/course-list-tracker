import json

# Retrieves info from tracking.json
# return: The json data converted into python objects
def getData() -> dict:
    with open("tracking.json", "r") as f:
        return json.load(f)

# Overwrites tracking.json. A call to this function will ALWAYS have a call to getData() first.
# param data: The data to be dumped into the json file
def updateData(data: dict) -> None:
    with open("tracking.json", "w") as f:
        json.dump(data, f, indent = 4)

# Called via the discord command 'track <CRN> <subject>'. Adds a discord user id to the 'tracked_by' list for a course if someone else is already tracking it or
# adds the course to the list if they are the first person to track it.
# param CRN: the unique identifier for the course
# param subject: the subject of the course
# param id: identification of the user requesting to track the course
def trackCourse(CRN: str, subject: str, id: str) -> None:
    trackingData = getData()
    
    for course in trackingData["Courses"]:
        if course["crn"] == CRN:
            course["tracked_by"].append(id)
            updateData(trackingData)
            return

    # If the course is not yet being tracked by anyone
    newEntry = {
        "crn": CRN,
        "subject": subject,
        "last_seen_status": "NONE",
        "tracked_by": [id]
    }

    trackingData["Courses"].append(newEntry)
    updateData(trackingData)

# Called via the discord command 'untrack <CRN>'. Removes a discord user id from the 'tracked_by' list for a course. If they were the only person tracking said course, then
# the entire course is removed.
# param CRN: the unique identifier for the course
# param identification: identification of the user requesting to track the course
# return: True for success, false if one of the arguments is invalid
def untrackCourse(CRN: str, identification: str) -> bool:
    trackingData = getData()

    for course in trackingData["Courses"]:
        if course["crn"] == CRN:
            if len(course["tracked_by"]) == 1 and course["tracked_by"][0] == identification:
                # If the course is only being tracked by one person and it is the person specified by the discord user id, delete the whole course.
                trackingData["Courses"].remove(course)
                updateData(trackingData)
                return True
            elif identification in course["tracked_by"]:
                # If other people also track the course, only delete the specified id from the list of people tracking.
                course["tracked_by"].remove(identification)
                updateData(trackingData)
                return True

    return False