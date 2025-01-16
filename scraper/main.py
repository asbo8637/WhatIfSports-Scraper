from web_driver import driver
from excel_creator import excel_editor
import time

driver = driver()
excel = excel_editor()
driver.login()
test=driver.get_teams()
print(test)

results=[]
for player in test:
    if(player[0]=="FAKE"):
        driver.go_to_team(player[2])
    else:
        overall, results = driver.get_consider(player[2])
        excel.add_player(player[0], player[1], player[3], player[4], player[5], player[6], player[7], overall, results)

excel.print_players()
excel.create_sheet()
driver.close_browser()