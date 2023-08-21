from selenium import webdriver as wd
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait 
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import time
import datetime
import calendar

# customize Chrome options
chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_driver = 'C:/Users/Abdulla/Documents/chromedriver_win32/chromedriver.exe'

roomList = ['572','571','570','574','573','569','568','567'] # List of rooms to iterate and try to book

cboDuration = '03:00' # booking time
cboStartTime = '8:00 AM' # booking start time
cboEndTime = '11:00 AM' # booking end time
dt_now = datetime.datetime.now() 
currentDay = int(dt_now.day) # current day
selectMonth = dt_now.month # current month
selectYear = dt_now.year # current month
monthDays = calendar.monthrange(dt_now.year, dt_now.month)[1] # max days in a month

# determines what day it will be in 7 days
if currentDay + 7 > monthDays: # if +7 days will be a new month
    print(currentDay+7,"new month")
    selectDay = (currentDay + 7) - monthDays
    if dt_now.month == 12: # if current month is December(12), transition to January(1) and iterate year
        selectMonth = 1
        selectYear += 1
    else: selectMonth += 1
    print(f"month = {selectMonth}")
else: 
    selectDay = currentDay + 7

# pull the credentials(username & password) from a file
credentials = {}
with open(r"C:\Users\Abdulla\Documents\Coding\RoomBooking\Account details.txt") as f:
    for line in f:
       (key, val) = line.strip().split('- ')
       credentials[key] = val

# initialize Chrome web service
wb = wd.Chrome(service=Service(
    r'C:/Users/Abdulla/Documents/chromedriver_win64/chromedriver.exe'), options=chrome_options)
wb.implicitly_wait(10)
wb.get("https://booking.carleton.ca/")

def check_exists_by_xpath(xpath: str) -> bool:
    """
    Returns True if element is found on page otherwise returns False
    """
    try:
        wb.find_element(By.XPATH,xpath)
    except NoSuchElementException:
        return False
    return True

def main() -> None:
    """
    Books a room one week in advance at a specified time
    """
    openLogin = wb.find_element(By.ID, 'spanLogin').click()


    WebDriverWait(wb, timeout= 10).until(lambda d: d.find_element(By.ID, 'txtUsername'))


    username = wb.find_element(By.ID,"txtUsername").send_keys(credentials["username"])
    password = wb.find_element(By.ID,"txtPassword").send_keys(credentials["password"])
    wb.find_element(By.ID, 'btnLogin').click()
    WebDriverWait(wb, timeout= 10).until(lambda e: e.find_element(By.LINK_TEXT, 'Find a Room'))
    wb.find_element(By.LINK_TEXT, 'Find a Room').click()

    Select(wb.find_element(By.ID, 'cboDuration')).select_by_visible_text(cboDuration)
    Select(wb.find_element(By.ID, 'cboStartTime')).select_by_visible_text(cboStartTime)
    Select(wb.find_element(By.ID, 'cboEndTime')).select_by_visible_text(cboEndTime)
    time.sleep(2)
    wb.find_element(By.ID, 'btnAnyDate').click()
    WebDriverWait(wb, timeout= 10).until(lambda e: e.find_element(By.CLASS_NAME, 'imgHint'))
    calendarMonth = f'{calendar.month_name[selectMonth]} {selectYear}'

    selectedDate = wb.find_element(By.XPATH, f"//*[@class='calendarTable' and contains(.,'{calendarMonth}')]//div[text()='{selectDay}']").click()
    time.sleep(2)

    for room in roomList:
        wb.find_element(By.XPATH, f"//div[contains(@data-caption,'{cboStartTime}')]//div[@class='imgBackArrow' and @aria-label='Previous Page']").click() #defaults to first page
        time.sleep(1)
        if check_exists_by_xpath(f"//div[contains(@data-caption,'{cboStartTime}')]//tr[@class='ClickableRow' and contains(.,'{room}')]"):
            roomRow = wb.find_element(By.XPATH, f"//div[contains(@data-caption,'{cboStartTime}')]//tr[@class='ClickableRow' and contains(.,'{room}')]").click()
            break
        else:
            wb.find_element(By.XPATH, f"//div[contains(@data-caption,'{cboStartTime}')]//div[@class='imgNextArrow' and @aria-label='Next Page']").click()
            time.sleep(1)
            if check_exists_by_xpath(f"//div[contains(@data-caption,'{cboStartTime}')]//tr[@class='ClickableRow' and contains(.,'{room}')]"):
                roomRow = wb.find_element(By.XPATH, f"//div[contains(@data-caption,'{cboStartTime}')]//tr[@class='ClickableRow' and contains(.,'{room}')]").click()
                break


    WebDriverWait(wb, timeout= 10).until(lambda e: e.find_element(By.CLASS_NAME, 'MessageBoxWindow'))

    time.sleep(2)
    wb.find_element(By.ID,'btnOK').click()
    WebDriverWait(wb, timeout= 10).until(lambda e: e.find_element(By.XPATH, "//*[@class='pageHeader' and contains(.,'Booking Confirmation')]"))
    time.sleep(2)
    wb.find_element(By.ID,'btnConfirm').click()
    WebDriverWait(wb, timeout= 10).until(lambda e: e.find_element(By.CLASS_NAME, "MessageBoxCaption"))
    wb.find_element(By.ID,'btnOK').click()
    time.sleep(2)

main()