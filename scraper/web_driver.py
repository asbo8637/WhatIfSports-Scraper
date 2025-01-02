import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import os
from dotenv import load_dotenv
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import requests

script_directory = os.path.dirname(os.path.abspath(__file__))
print(f"Script directory: {script_directory}")
# Load the .env file from the current working directory
load_dotenv(dotenv_path=os.path.join(script_directory, '.env'), override=True)

class driver:
    '''
    Driver class. Allows for simple manipluations of the website. 
    '''
    def __init__(self):
        # Set up undetected-chromedriver. Bypassess bot security. 
        options = uc.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-blink-features=AutomationControlled')  # Disables bot detection features

        # Start the browser
        self.chrome = uc.Chrome(options=options)
        self.wait = WebDriverWait(self.chrome, int(os.getenv("time_out")))

    def login(self):
        '''
        Logins with the .env variables. For whatifsports
        '''
        self.chrome.get('https://www.whatifsports.com/locker/lockerroom.asp')

        input_field = self.wait.until(EC.visibility_of_element_located((By.ID, "username")))
        input_field.click() 

        actions = ActionChains(self.chrome)
        actions.send_keys(os.getenv("username")).perform()
        
        input_field = self.chrome.find_element(By.ID, "password") 
        input_field.click() 
        actions.send_keys(os.getenv("password")).send_keys(Keys.RETURN).perform()

    def get_player_ids(self, link):
        '''
        gets the list of player id's to work with. 
        '''
        # Navigate to the provided link in the new tab
        self.chrome.get(link)
        self.wait.until(EC.visibility_of_element_located((By.ID, "office_default")))
        
        #This is the query for the players. From cookies will get the team. 
        self.chrome.get('https://www.whatifsports.com/hd/Recruiting/TeamRecruitingPool.aspx?filterView=1&decisionStatus=2&view=1&includeHS=True&includeJUCO=True&includeTransfers=True&includeInternational=True&projDivision=4&ratingFilter1=1&ratingFilter2=1&ratingFilter3=1&ratingFilter4=1&primarySortField=1&primarySortDirection=1&page=1&search=True')

        self.wait.until(EC.visibility_of_element_located((By.ID ,'recruiting_teamrecruitingpool')))
        players = self.chrome.find_elements(By.XPATH, '//*[@title="Open Recruit Profile"]')
        miles=self.chrome.find_elements(By.CLASS_NAME, "right.miles")
        miles = [item for item in miles if item.text.lower() != "miles"]
        playerPages=[]
        for player, mile in zip(players, miles):
            if player.text != "":
                print("Found player: ", player.text)
                name=player.text.split()
                url=player.get_attribute('href').replace("Default", "ConsideringList")
                playerPages.append([name[0], name[1], url, mile.text])

        return playerPages


    def get_teams(self):
        '''
        Finds each team and calls get_player 
        '''
        self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "teamName")))
        teams = self.chrome.find_elements(By.CLASS_NAME, 'teamName')
        hrefs = []
        for team in teams:
            print(team.text)
            if(team.text!=""):
                link = team.find_element(By.TAG_NAME, 'a')
                hrefs.append(link.get_attribute('href'))
        
        playerPages=[]
        for href in hrefs:
            print(f"Link to click: {href}")
            playerPages.extend(self.get_player_ids(href))
        
        return playerPages
        

    def get_consider(self, url):
        # Fetch the page content
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the table with the specified class
        table = soup.find('table', {'class': 'standard.history.sortable'})

        # List to store the extracted data
        data = []

        # Loop through the rows (both odd and even)
        for row in table.find_all('tr', class_=['odd', 'even']):
            # Extract all the <td> cells in the row
            columns = row.find_all('td')
            
            # If there are enough columns (to avoid IndexErrors)
            if len(columns) >= 6:
                team = columns[0].text.strip()
                coach = columns[1].text.strip()
                division = columns[2].text.strip()
                prestige = columns[3].text.strip()
                int_level = columns[4].text.strip()
                scholarship_offer = columns[5].text.strip()
                
                # Store the extracted data
                data.append({
                    'Team': team,
                    'Coach': coach,
                    'Division': division,
                    'Prestige': prestige,
                    'Int Level': int_level,
                    'Scholarship Offer?': scholarship_offer
                })

        # Print the extracted data
        for entry in data:
            print(entry)

                    


