import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
import time

# Set up undetected-chromedriver
options = uc.ChromeOptions()
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-blink-features=AutomationControlled')  # Disables bot detection features

# Start the browser
driver = uc.Chrome(options=options)
driver.get('https://www.whatifsports.com/locker/lockerroom.asp')

time.sleep(10)

# search_box = driver.find_element(By.NAME, "email")
# search_box.send_keys("Selenium key inputs")

time.sleep(600)
driver.quit()
