from course_tracker import datamanager
from course_tracker import scraper
from course_tracker.hikari_lightbulb_bot import bot
import asyncio

# Controls the while loop that keeps the tracker running continuously
tracking = False

# Checks for course status changes on an infinite loop with some pause time inbetween each iteration.
async def track() -> None:
    while tracking:
        print("tracker: Start of tracking loop...")

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

        print("tracker: End of tracking loop...")
        await asyncio.sleep(15)