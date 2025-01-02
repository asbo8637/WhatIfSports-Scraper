from driver import driver
import time

driver = driver()
driver.login()
driver.get_teams()

time.sleep(6000)