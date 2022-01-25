# course-list-tracker

This program web scrapes William and Mary's Open Course List Website (https://courselist.wm.edu/courselist/). It allows users to track the Open/Closed status of specific courses. Courses are tracked via SMS messages using the Twilio API.

## SMS Commands

- Track a new course: 'track {CRN} {subject}'
- Untrack a course: 'untrack {CRN}'