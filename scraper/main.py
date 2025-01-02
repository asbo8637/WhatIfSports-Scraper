from web_driver import driver
import time

driver = driver()
driver.login()
test=driver.get_teams()
print(test)
for player in test:
    driver.get_consider(player[2])

time.sleep(6000)