from bs4 import BeautifulSoup
import requests

# A basic url for the WM Open Course List that can be added too
BASE_URL = "https://courselist.wm.edu/courselist/courseinfo/searchresults?term_code=202220&term_subj=&attr=0&attr2=0&levl=0&status=0&ptrm=0&search=Search"


# Creates a url for a subject page on the WM Open Course List
# param subject: the subject identifier to be inserted into the URL (Examples: CSCI, BIOL, THEA, etc)
def createURL(subject):
    insertLocStr = "term_subj="
    insertLocIndex = BASE_URL.find(insertLocStr)

    return BASE_URL[:insertLocIndex + 10] + subject + BASE_URL[insertLocIndex + 10:]

print(createURL("BIOL"))