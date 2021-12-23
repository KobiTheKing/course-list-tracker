import json

# Retrieves info from tracking.json
# return: The json data converted into python objects
def getData():
    with open("tracking.json", "r") as f:
        return json.load(f)

# Overwrites tracking.json. A call to this function will ALWAYS have a call to getData() first.
# param data: The data to be dumped into the json file
def updateData(data):
    with open("tracking.json", "w") as f:
        json.dump(data, f, indent = 4)

# Called via the sms command 'track <CRN> <subject>'. Adds phone number to the 'tracked_by' list for a course if someone else is already tracking it or
# adds the course to the list if they are the first person to track it.
# param CRN: the unique identifier for the course
# param subject: the subject of the course
# param phoneNum: the phone number of the user requesting to track the course
def trackCourse(CRN, subject, phoneNum):
    trackingData = getData()
    
    for course in trackingData["Courses"]:
        if course["crn"] == CRN:
            course["tracked_by"].append(phoneNum)
            updateData(trackingData)
            return

    # If the course is not yet being tracked by anyone
    newEntry = {
        "crn": CRN,
        "subject": subject,
        "last_seen_status": "NONE",
        "tracked_by": [phoneNum]
    }

    trackingData["Courses"].append(newEntry)
    updateData(trackingData)



# Called via the sms command 'untrack <CRN>'. Removes a phone number from the 'tracked_by' list for a course. If they were the only person tracking said course, then
# the entire course is removed.
# param CRN: the unique identifier for the course
# param phoneNum: the phone number of the user requesting to track the course
# return: True for success, false if one of the arguments is invalid
def untrackCourse(CRN, phoneNum):
    trackingData = getData()

    for course in trackingData["Courses"]:
        if course["crn"] == CRN:
            if len(course["tracked_by"]) == 1 and course["tracked_by"][0] == phoneNum:
                # If the course is only being tracked by one person and it is the person specified by the phoneNum argument, delete the whole course.
                trackingData["Courses"].remove(course)
                updateData(trackingData)
                return True
            elif phoneNum in course["tracked_by"]:
                # If other people also track the course, only delete the specified number from the list of people tracking
                course["tracked_by"].remove(phoneNum)
                updateData(trackingData)
                return True

    return False


# Testing
#trackCourse("20854", "FREN", "4349810169")
print(untrackCourse("20854", "1112223333"))