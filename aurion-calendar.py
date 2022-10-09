import os
from pathlib import Path
import json
import xml.etree.ElementTree as ET
import dateutil.parser
from dotenv import load_dotenv

from seleniumwire import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By

from icalendar import Calendar, Event, vText


# Setup variables and constants
load_dotenv()
CHROME_DRIVER_PATH = os.getenv('CHROME_DRIVER_PATH')
AURION_URL = "https://aurion.junia.com/"
AURION_EMAIL = os.getenv('AURION_EMAIL')
AURION_PASSWORD = os.getenv('AURION_PASSWORD')

capabilities = DesiredCapabilities.CHROME
capabilities["goog:loggingPrefs"] = {"performance": "ALL"}


# Initialise browser
driver = webdriver.Chrome(
    CHROME_DRIVER_PATH, desired_capabilities=capabilities)
driver.get(AURION_URL)


# Wait login page to be displayed
try:
    element_to_check = EC.presence_of_element_located(
        (By.XPATH, '//input[@id="username"]'))
    WebDriverWait(driver, 10).until(element_to_check)
except TimeoutException:
    print('Timed out waiting for page to load')
# Fill username
username_input = driver.find_element(By.ID, 'username')
username_input.send_keys(AURION_EMAIL)
# Fill password
password_input = driver.find_element(By.ID, 'password')
password_input.send_keys(AURION_PASSWORD)
# Submit form
driver.find_element(By.ID, 'j_idt28').click()


# Wait home page to be displayed
try:
    element_to_check = EC.presence_of_element_located(
        (By.ID, 'form:j_idt753'))
    WebDriverWait(driver, 10).until(element_to_check)
except TimeoutException:
    print('Timed out waiting for page to load')
# Navigate to planning page
driver.find_element(
    By.XPATH, """ //li[@class='ui-menuitem ui-widget ui-corner-all']//span[contains(text(), 'Mon Planning')] """).click()


# Wait planning to be displayed
try:
    element_to_check = EC.presence_of_element_located(
        (By.XPATH, '//div[@class="fc-content"]'))
    WebDriverWait(driver, 10).until(element_to_check)
except TimeoutException:
    print('Timed out waiting for page to load')
all_request = driver.requests
# Get planning response
for request in driver.requests:
    if request.url == "https://aurion.junia.com/faces/Planning.xhtml":
        print(
            'Get planning response from: ',
            request.url,
            request.response.status_code,
        )
        response_body = request.response.body


driver.close()


# Process planning response
decoded_response_body = str(response_body, 'utf-8')
parsed_response_body = ET.ElementTree(ET.fromstring(decoded_response_body))
events_string = parsed_response_body.find(
    './/update[@id="form:j_idt118"]').text
events_json = json.loads(events_string)


def clean_title(titles):
    titles.remove("\n")
    return [title.replace('\n', '') for title in titles]


# Create .ics file to export events
cal = Calendar()
for event in events_json['events']:
    # process title
    raw_title = str(event['title'])
    array_title = clean_title(raw_title.splitlines(True))
    title = f"{array_title[1]}"
    # process description
    description = f"{array_title[4]} - {array_title[0]}"
    # process date
    start = dateutil.parser.parse(event['start'])
    end = dateutil.parser.parse(event['end'])
    # create event
    event = Event()
    event.add('summary', title)
    event.add('description', description)
    event.add('dtstart', start)
    event.add('dtend', end)
    if "HEI" in title:
        event['location'] = vText(
            'HEI – Hautes Études d’Ingénieur 13 Rue de Toul, 59014 Lille, France')
    if "EURATECH" in title:
        event['location'] = vText(
            'Euratechnologies, 58 Allée Marie-thérèse Vicot-Lhermitte, 59000, Lille')
    cal.add_component(event)


# Save .ics file
directory = str(Path.home() / "Downloads") + "/"
print(".ics file will be generated at ", directory)
f = open(os.path.join(directory, 'aurion-events.ics'), 'wb')
f.write(cal.to_ical())
f.close()
