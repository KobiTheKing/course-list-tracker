from bs4 import BeautifulSoup
import requests

BASE_URL = "https://courselist.wm.edu/courselist/courseinfo/searchresults?term_code=202220&term_subj=&attr=0&attr2=0&levl=0&status=0&ptrm=0&search=Search"

def createURL(subject):
    insertLocStr = "term_subj="
    insertLocIndex = BASE_URL.find(insertLocStr)

    return BASE_URL[:insertLocIndex + 10] + subject + BASE_URL[insertLocIndex + 10:]

print(createURL("BIOL"))