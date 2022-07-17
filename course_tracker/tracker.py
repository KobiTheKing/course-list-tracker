import asyncio
import sys

from course_tracker import database
from course_tracker import scraper
from course_tracker import queue
from course_tracker import request
from course_tracker.hikari_lightbulb_bot import bot

# Controls the while loop that keeps the tracker running continuously
tracking = False

# All incoming requests from users to track a course or untrack a course are sent here
requestQueue = queue.Queue()

# Checks for course status changes on an infinite loop with some pause time inbetween each iteration.
# The purpose of the phases and queue of requests is to only update the tracking.json file at strict times to prevent simultanious requests to overwrite eachother's changes.
async def track() -> None:
    while tracking:
        print("tracker: Start of tracking loop...")

        # Phase 1: Check the status of all tracked courses, notify users of any changes.
        print("tracker: Start phase 1...")

        trackingData = database.getCourses()
        coursesToUpdate = []

        for course in trackingData:
            try:
                status = scraper.checkStatus(course[0], course[1])

                # Situations where users tracking the course should be notified (a change in status)
                if not status and course[2] == "OPEN":
                    coursesToUpdate.append((course[0], "CLOSED"))
                    await bot.sendDM(database.courseTrackedBy(course[0]), f"{course[0]} is now closed!")
                elif status and course[2] == "CLOSED":
                    coursesToUpdate.append((course[0], "OPEN"))
                    await bot.sendDM(database.courseTrackedBy(course[0]), f"{course[0]} is now open!")
                elif course[2] == "NONE":
                    coursesToUpdate.append((course[0], "OPEN" if status else "CLOSED"))
                    await bot.sendDM(database.courseTrackedBy(course[0]), f"{course[0]} is currently {'open' if status else 'closed'}.")
            except Exception:
                print(f"Error (tracker.py): Failed to check status of {course}.")

        database.updateCourses(coursesToUpdate)

        await asyncio.sleep(15)

        # Phase 2: Complete all requests that came in while Phase 1 was happening. Requests can be to track a course or untrack a course.
        print("tracker: Start phase 2...")

        fulfillRequests()

        print("tracker: End of tracking loop...")
        await asyncio.sleep(15)

    # If we exit the tracking loop, initiate a safe shutdown of the bot by fulfilling any remaining requests and then shutting down.
    fulfillRequests()

    await bot.shutdown()

    sys.exit()

# Fulfill all current requests
def fulfillRequests() -> None:
    for _ in range(len(requestQueue)):
        rqst = requestQueue.dequeue()
        
        if rqst.type == request.RequestType.TRACK:
            database.trackCourse(rqst.crn, rqst.subject, rqst.userID, rqst.username)
            print("tracker: Handled request to track a course.")
        elif rqst.type == request.RequestType.UNTRACK:
            database.untrackCourse(rqst.crn, rqst.userID)
            print("tracker: Handled request to untrack a course.")