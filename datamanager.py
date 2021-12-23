import json

with open("example.json", "r") as f:
    data = json.load(f)

for crn in data["CRNs"]:
    if crn["last_seen_status"] == "OPEN":
        crn["last_seen_status"] = "CLOSED"
    else:
        crn["last_seen_status"] = "OPEN"

with open("example.json", "w") as f:
    json.dump(data, f, indent = 4)



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
    pass

# Called via the sms command 'untrack <CRN>'. Removes a phone number from the 'tracked_by' list for a course. If they were the only person tracking said course, then
# the entire course is removed.
# param CRN: the unique identifier for the course
# param phoneNum: the phone number of the user requesting to track the course
def untrackCourse(CRN, phoneNum):
    pass