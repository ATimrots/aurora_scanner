from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from dotenv import load_dotenv
import os
import requests
import time

load_dotenv()

APP_ENV = os.getenv('APP_ENV')
THRESHOLD = int(os.getenv('KP_INDEX_THRESHOLD', 5))

class attribute_has_changed(object):
  def __init__(self, locator, val, attr):
    self.locator = locator
    self.val = val
    self.attr = attr

  def __call__(self, driver):
    element = driver.find_element(*self.locator)   # Finding the referenced element

    if self.attr == 'text':
        check_value = element.text
    else:
        check_value = element.get_attribute(self.attr)

    if self.val not in check_value:
        return element
    else:
        return False

def ntfy(message, tag = 'star_struck'):
    h = {
        "Tags": tag,
        # "Actions": "view, Open portal, https://www.gi.alaska.edu/monitors/aurora-forecast"
    }

    requests.post("https://ntfy.sh/atimrots-aurora-alerts", data=message, headers=h)

# service = Service(executable_path='/usr/bin/chromedriver')
# service = Service()
# options = webdriver.ChromeOptions()
# options.add_argument("--window-size=1920,1200")

if APP_ENV == 'production':
    display = Display(visible=0, size=(800, 600))
    display.start()

driver = webdriver.Chrome()

driver.get("https://www.gi.alaska.edu/monitors/aurora-forecast")

print(driver.title)
print(driver.current_url)

img_src = driver.find_element(By.XPATH, '//*[@id="alaska"]').get_attribute('src')

to_europe = driver.find_element(By.XPATH, '//*[@id="eu-map"]')

driver.execute_script("arguments[0].click();", to_europe)

wait = WebDriverWait(driver, 5)
img_elem = wait.until(attribute_has_changed((By.XPATH, '//*[@id="alaska"]'), img_src, 'src'))

kp_index = driver.find_element(By.XPATH, '//*[@id="kp_value"]').text

print("EUROPE KP INDEX: "+kp_index)
print('EUROPE Image '+img_elem.get_attribute('src'))

if int(kp_index) >= THRESHOLD:
    message = ('You can see aurora today! KP INDEX: '+kp_index).encode(encoding='utf-8')
    # print('You should go out and find some Aurora today!')

    ntfy(message)
else:
    print('You can\'t see aurora today!')

    next_button = driver.find_element(By.XPATH, '//*[@id="right-nav"]')

    current_date = driver.find_element(By.ID, 'local-date')
    date_text = current_date.text

    for i in range(7):
        next_button.click()
        wait = WebDriverWait(driver, 5)
        date = wait.until(attribute_has_changed((By.ID, 'local-date'), date_text, 'text'))
        date_text = date.text

        kp_index = driver.find_element(By.XPATH, '//*[@id="kp_value"]').text

        if int(kp_index) >= THRESHOLD:
            message = ('Next aurora after '+str(i)+' days on '+date_text+' KP INDEX: '+kp_index).encode(encoding='utf-8')
            # print(message)
            ntfy(message, 'calendar')
            break

driver.quit()
