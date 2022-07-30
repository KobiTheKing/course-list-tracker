"""Controls all web scraping tasks."""

import requests
from requests.exceptions import RequestException

from bs4 import BeautifulSoup

# The base url for the WM Open Course List that can be added too
BASE_URL = "https://courselist.wm.edu/courselist/courseinfo/searchresults?term_code=202310&term_subj=&attr=0&attr2=0&levl=0&status=0&ptrm=0&search=Search"

def check_status(CRN: int, subject: str) -> bool:
    """Scrape the W&M Open Course List to find the status of the specified course.

    The status can be OPEN or CLOSED.

    Args:
        CRN: The unique identifier for the course.
        subject: The subject of the course.

    Returns:
        True if the status is open, false if the status is closed.

    Raises:
        RequestException: If the URL does not exist OR there is a problem connecting to the site OR the CRN cannot be found.
    """
    try:
        soup = scrape(create_URL(subject))
    except requests.exceptions.RequestException:
        raise RequestException

    # Retrieves all of the cells in the table as a list
    table = soup.find("div", id = "results").table.tbody
    cells = table.find_all("td")

    for index, cell in enumerate(cells):
        # If the cell being looked at contains a CRN
        if index % 11 == 0:
            if cell.text.strip() == str(CRN):
                # Checks the cell that contains the status for this specific CRN
                if cells[index + 10].text.strip() == "OPEN":
                    return True
                elif cells[index + 10].text.strip() == "CLOSED":
                    return False
    
    # If we go through entire loop and can't find the CRN
    raise RequestException

def check_validity(CRN: int, subject: str) -> bool:
    """Determine the existence of the given params on the W&M Open Course List.

    Checks if the URL with the given subject exists. If so, checks if the given CRN exists on that URL.

    Args:
        CRN: The unique identifier for the course.
        subject: The subject of the course.

    Returns:
        True if the CRN and URL exist, false if the URL exists but the CRN does not.

    Raises:
        RequestException: If the URL does not exist OR there is a problem connecting to the site.
    """

    try:
        soup = scrape(create_URL(subject))
    except requests.exceptions.RequestException:
        raise RequestException

    # Retrieves all of the cells in the table as a list
    table = soup.find("div", id = "results").table.tbody
    cells = table.find_all('td')

    for index, cell in enumerate(cells):
        # If the cell being looked at contains a CRN
        if index % 11 == 0:
            if cell.text.strip() == str(CRN):
                return True

    # If we go through entire loop and can't find the CRN
    return False

def create_URL(subject: str) -> str:
    """Create a URL to a specific subject page on the W&M Open Course List.

    Args:
        subject: The subject of the course.
    
    Returns:
        The generated URL.
    """

    insertLocStr = "term_subj="
    insertLocIndex = BASE_URL.find(insertLocStr)

    return BASE_URL[:insertLocIndex + 10] + subject + BASE_URL[insertLocIndex + 10:]

def scrape(URL: str) -> BeautifulSoup:
    """Scrape a page on the W&M Open Course List.

    Args:
        URL: The URL to scrape.

    Returns:
        The HTML code of the web page.

    Raises:
        RequestException if the URL does not exist OR there is a problem retrieving it.
    """

    try:
        source = requests.get(URL, timeout = 10.000)
    except requests.exceptions.RequestException:
        raise RequestException

    soup = BeautifulSoup(source.text, "lxml")

    # Checks if the url leads to a special error page
    if soup.find("h1", class_ = "bannerTitle").a.text.strip() == "Error":
        raise RequestException

    return soup