from course_tracker import datamanager
from course_tracker import scraper
from course_tracker import queue
from course_tracker import request
from course_tracker.hikari_lightbulb_bot import bot
import asyncio

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

        trackingData = datamanager.getData()

        for course in trackingData["Courses"]:
            try:
                status = scraper.checkStatus(course["crn"], course["subject"])

                # Situations where users tracking the course should be notified (a change in status)
                if not status and course["last_seen_status"] == "OPEN":
                    course["last_seen_status"] = "CLOSED"
                    await bot.sendDM(course["tracked_by"], f"{course['crn']} is now closed!")
                elif status and course["last_seen_status"] == "CLOSED":
                    course["last_seen_status"] = "OPEN"
                    await bot.sendDM(course["tracked_by"], f"{course['crn']} is now open!")
                elif course["last_seen_status"] == "NONE":
                    course["last_seen_status"] = "OPEN" if status else "CLOSED"
                    await bot.sendDM(course["tracked_by"], f"{course['crn']} is currently {'open' if status else 'closed'}.")
            except Exception as e:
                print(f"Error (tracker.py): Failed to check status of {course}.")

        datamanager.updateData(trackingData)

        await asyncio.sleep(15)

        # Phase 2: Complete all requests that came in while Phase 1 was happening. Requests can be to track a course or untrack a course.
        print("tracker: Start phase 2...")

        for _ in range(len(requestQueue)):
            rqst = requestQueue.dequeue()
            
            if rqst.type == request.RequestType.TRACK:
                datamanager.trackCourse(rqst.crn, rqst.subject, rqst.authorID)
                print("tracker: Handled request to track a course.")
            elif rqst.type == request.RequestType.UNTRACK:
                datamanager.untrackCourse(rqst.crn, rqst.authorID)
                print("tracker: Handled request to untrack a course.")

        print("tracker: End of tracking loop...")
        await asyncio.sleep(15)