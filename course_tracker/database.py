import os
import dotenv
import datetime

import psycopg2

dotenv.load_dotenv()

credentials = {
    "host": os.environ["HOST_NAME"],
    "dbname": os.environ["DATABASE_NAME"],
    "user": os.environ["USERNAME"],
    "password": os.environ["PASSWORD"],
    "port": os.environ["PORT_ID"]
}

# Retrieves all of the courses currently being tracked.
def getCourses() -> list:
    try:
        with psycopg2.connect(**credentials) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM course;")
                
                return cur.fetchall()
    except Exception as e:
        print("Error: " + str(e))
    finally:
        conn.close()

# Update a list of courses with a specific status.
# List comes in the form of [(crn, status), (crn, status), ...]
def updateCourses(courses: list) -> None:
    try:
        with psycopg2.connect(**credentials) as conn:
            with conn.cursor() as cur:
                for course in courses:
                    cur.execute("UPDATE course SET status = %s, last_changed = %s WHERE crn = %s", (course[1], datetime.datetime.now(), course[0]))
    except Exception as e:
        print("Error: " + str(e))
    finally:
        conn.close()

# Returns a list of all users who are tracking the given course.
def courseTrackedBy(CRN: int) -> list:
    try:
        with psycopg2.connect(**credentials) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT FK_discord_id FROM tracking WHERE FK_crn = %s", (CRN,))
                return [user[0] for user in cur.fetchall()]
    except Exception as e:
        print("Error: " + str(e))
    finally:
        conn.close()

# Called via the discord command 'track <CRN> <subject>'. Adds a new user entry if this is the first course they are tracking. Adds a new course entry if this is the first person
# to track this course. Adds a tracking entry.
# param CRN: the unique identifier for the course
# param subject: the subject of the course
# param identification: identification of the user requesting to track the course
# param name: name of user
def trackCourse(CRN: int, subject: str, identification: int, name: str) -> None:
    try:
        with psycopg2.connect(**credentials) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM person WHERE discord_id = %s", (identification,))
                if len(cur.fetchall()) != 1:
                    # Insert new person entry
                    personEntry = "INSERT INTO person (discord_id, name, first_joined) VALUES (%s, %s, %s)"
                    personVals = (identification, name, datetime.datetime.now())

                    cur.execute(personEntry, personVals)

                cur.execute("SELECT * FROM course WHERE crn = %s", (CRN,))
                if len(cur.fetchall()) != 1:
                    # Insert new course entry
                    courseEntry = "INSERT INTO course (crn, subject, status, last_changed) VALUES (%s, %s, %s, %s)"
                    courseVals = (CRN, subject, "NONE", datetime.datetime.now())
                    cur.execute(courseEntry, courseVals)

                # Insert new tracking entry
                trackingEntry = "INSERT INTO tracking (fk_discord_id, fk_crn, started_tracking) VALUES (%s, %s, %s)"
                trackingVals = (identification, CRN, datetime.datetime.now())
                cur.execute(trackingEntry, trackingVals)
    except Exception as e:
        print("Error: " + str(e))
    finally:
        conn.close()

# Called via the discord command 'untrack <CRN>'. Removes a tracking entry corresponding to the person and course. If they were the only person tracking said course, then
# the entire course is removed.
# param CRN: the unique identifier for the course
# param identification: identification of the user requesting to track the course
def untrackCourse(CRN: int, identification: int) -> None:
    try:
        with psycopg2.connect(**credentials) as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM tracking WHERE FK_discord_id = %s AND FK_crn = %s", (identification, CRN))

                cur.execute("SELECT * FROM tracking WHERE FK_crn = %s", (CRN,))
                if len(cur.fetchall()) == 0:
                    # Delete the whole course entry if no one else is tracking it
                    cur.execute("DELETE FROM course WHERE crn = %s", (CRN,))
    except Exception as e:
        print("Error: " + str(e))
    finally:
        conn.close()