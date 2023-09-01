import os
import time
from dotenv import load_dotenv
from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from wait_rules import attribute_has_changed
from ntfy import ntfy

load_dotenv()

APP_ENV = os.getenv('APP_ENV')
THRESHOLD = int(os.getenv('KP_INDEX_THRESHOLD', 5))

# The following code is commented, because newer versions of Selenium doesn't require to install the driver, it finds and uses it by itself.
# In case you still need to specify specific driver, add it to Service executable_path.
# service = Service(executable_path='/usr/bin/chromedriver')
# service = Service()
# options = webdriver.ChromeOptions()
# options.add_argument("--window-size=1920,1200")

# The main idea is to schedule and run the program on the server with a cronjob at background,
# so the actual browser display is not necessary and we can use virtual display instead.
if APP_ENV == 'production':
    display = Display(visible=0, size=(800, 600))
    display.start()

driver = webdriver.Chrome()

driver.get("https://www.gi.alaska.edu/monitors/aurora-forecast")

print('Title: '+driver.title)
print('Url: '+driver.current_url)

img_src = driver.find_element(By.XPATH, '//*[@id="alaska"]').get_attribute('src')
to_europe = driver.find_element(By.XPATH, '//*[@id="eu-map"]')
current_date = driver.find_element(By.ID, 'local-date').text

# The execute_script has been used, because element.click() doesn't work sometimes. Don't know why yet.
driver.execute_script("arguments[0].click();", to_europe)

wait = WebDriverWait(driver, 5)
img_elem = wait.until(attribute_has_changed((By.XPATH, '//*[@id="alaska"]'), img_src, 'src'))

# Print out to verify if region has changed to Europe for test reasons only.
print('Image of opened region: '+img_elem.get_attribute('src'))

next_button = driver.find_element(By.XPATH, '//*[@id="right-nav"]')
driver.execute_script("arguments[0].click();", next_button)

wait = WebDriverWait(driver, 5)
today_date = wait.until(attribute_has_changed((By.ID, 'local-date'), current_date, 'text')).text

kp_index = driver.find_element(By.XPATH, '//*[@id="kp_value"]').text

print("EUROPE KP INDEX: "+kp_index+' ON "'+today_date+'"')

if int(kp_index) >= THRESHOLD:
    message = ('Hoorah! You can see aurora today! KP INDEX: '+kp_index).encode(encoding='utf-8')
    print(message)
    ntfy(message)
else:
    print('You can\'t see aurora today!')

    date_text = today_date

    for i in range(1, 7):
        driver.execute_script("arguments[0].click();", next_button)
        wait = WebDriverWait(driver, 5)
        date = wait.until(attribute_has_changed((By.ID, 'local-date'), date_text, 'text'))
        date_text = date.text

        kp_index = driver.find_element(By.XPATH, '//*[@id="kp_value"]').text

        if int(kp_index) >= THRESHOLD:
            message = ('Next aurora will be visible after '+str(i)+' days on "'+date_text+'" with KP INDEX: '+kp_index).encode(encoding='utf-8')
            print(message)
            ntfy(message, 'calendar')
            break

if APP_ENV == 'production':
    display.stop()

driver.quit()
