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
        # Set up undetected-chromedriver. Bypasses bot security. 
        options = uc.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-blink-features=AutomationControlled')  # Disables bot detection features
        options.add_argument('--disable-popup-blocking')

        options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

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

    def get_player_ids(self, link, get_team):
        '''
        gets the list of player id's to work with. 
        '''
        # Navigate to the provided link in the new tab
        if(get_team):
            self.chrome.get(link)
            self.wait.until(EC.visibility_of_element_located((By.ID, "office_default")))
            
            #This is the query for the players. From cookies will get the team. 
            self.chrome.get('https://www.whatifsports.com/hd/Recruiting/TeamRecruitingPool.aspx?filterView=1&decisionStatus=2&view=1&includeHS=True&includeJUCO=True&includeTransfers=True&includeInternational=True&projDivision=4&ratingFilter1=1&ratingFilter2=1&ratingFilter3=1&ratingFilter4=1&primarySortField=1&primarySortDirection=1&page=1&search=True')
            self.wait.until(EC.visibility_of_element_located((By.ID ,'recruiting_teamrecruitingpool')))
        else: 
            self.chrome.get(link)
            self.wait.until(EC.visibility_of_element_located((By.ID ,'recruiting_teamrecruitingpool')))

        players = self.chrome.find_elements(By.XPATH, '//*[@title="Open Recruit Profile"]')
        miles=self.chrome.find_elements(By.CLASS_NAME, "right.miles")
        states = self.chrome.find_elements(By.CLASS_NAME, "sec1")
        miles = [item for item in miles if item.text.lower() != "miles"]
        physicals = [
            item for item in self.chrome.find_elements(By.CLASS_NAME, "sec4.borderRight")
            if item.text in {'A', 'B', 'C', 'D', 'F'}
        ]

        defenses = [
            item for item in self.chrome.find_elements(By.CLASS_NAME, "sec2.borderRight")
            if item.text in {'A', 'B', 'C', 'D', 'F'}
        ]

        offenses = [
            item for item in self.chrome.find_elements(By.CLASS_NAME, "sec3.borderRight")
            if item.text in {'A', 'B', 'C', 'D', 'F'}
        ]

        states = [
            item for item in states
            if item.text.lower() != "state"
            and len(item.text) == 2
            and '-' not in item.text
            and '+' not in item.text
            and item.text.lower() != "we"
            and item.text.lower() != "ft"
        ]
        playerPages=[]
        for player, mile, state, physical, defense, offense in zip(players, miles, states, physicals, defenses, offenses):
            if player.text != "":
                print("Found player: ", player.text)
                name=player.text.split()
                url=player.get_attribute('href').replace("Default", "ConsideringList")
                playerPages.append([name[0], name[1], url, mile.text, state.text, physical.text, defense.text, offense.text])
        
        newLink = None
        try:
            newLink = self.chrome.find_element(By.CLASS_NAME, "nextpage")
            if newLink:
                href_value = newLink.find_element(By.TAG_NAME, "a").get_attribute('href')
                playerPages.extend(self.get_player_ids(href_value, False))
        except:
            print("The element with class 'nextpage' was not found.")
        

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
            if team.text!="":
                link = team.find_element(By.TAG_NAME, 'a')
                hrefs.append(link.get_attribute('href'))
        
        playerPages=[]
        for href in hrefs:
            print(f"Link to click: {href}")
            playerPages.append(["FAKE", "FAKE", href, 0, 0, 0, 0, 0])
            playerPages.extend(self.get_player_ids(href, True))
        
        return playerPages
        

    def get_consider(self, url):
        self.chrome.get(url)
        self.wait.until(EC.visibility_of_element_located((By.ID ,'recruitprofile')))
        # Find the parent element with the class name 'legend'
        legend = self.chrome.find_element(By.CLASS_NAME, 'legend')

        # Find all child elements with the class name 'iconLegend' within the parent 'legend' element
        icon_legends = legend.find_elements(By.CLASS_NAME, 'iconLegend')

        # Extract the text from the second 'iconLegend' element\
        overall = "na"
        if len(icon_legends) > 1:
            overall = icon_legends[1].text
            if not "Ranked Overall" in overall:
                overall = "na"
        else:
            print("Second iconLegend not found.")
        values = []
        tableClasses=["odd", "even", "even.highlight", "odd.highlight"]
        for tableClass in tableClasses:
            values.extend(self.chrome.find_elements(By.CLASS_NAME, tableClass))
        
        player_considering=[]
        for value in values:
            cells=[]
            cells.extend(value.find_elements(By.TAG_NAME, 'td'))
            cells = [cell.text for cell in cells]
            player_considering.append(cells)

        return overall, player_considering

    def go_to_team(self, url):
        self.chrome.get(url)
        self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "teampage.mainPage2Col.mainPage")))

    def close_browser(self):
        """
        Properly closes the undetected Chrome browser instance.

        Args:
            driver: The Chrome WebDriver instance to be closed.
        """
        try:
            if self.chrome:
                self.chrome.quit()  # Closes all browser windows and ends the WebDriver session
                print("Browser closed successfully.")
        except Exception as e:
            print(f"Error while closing the browser: {e}")
    




                    


