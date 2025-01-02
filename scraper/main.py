from driver import driver
import time

driver = driver()
driver.login()
test=driver.get_teams()
print(test)

time.sleep(6000)