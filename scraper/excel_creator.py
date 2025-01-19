import pandas as pd
import os

grade_to_rank = {
    "A+": 9, "A": 8, "A-": 7,
    "B+": 6, "B": 5, "B-": 4,
    "C+": 3, "C": 2, "C-": 1,
    "D": 0, "F": -1, "": -2
}

class excel_editor:
    def __init__(self):
        self.first_names=[]
        self.last_names=[]
        self.miles=[]
        self.states=[]
        self.positions=[]

        self.highest_team=[]
        self.highest_coach=[]
        self.highest_division=[]
        self.overall_rating=[]
        self.physical=[]
        self.defense=[]
        self.offense=[]
        self.above_low_interest=[]
        self.highest_prestige=[]
        self.human_coaches=[]
        self.offers=[]
        self.offers1=[]
        self.offers2=[]
        self.offers3=[]
        
    def add_player(self, first_name, last_name, miles, state, physical, defense, offense, position, overall, stats):
        self.first_names.append(first_name)    
        self.last_names.append(last_name)
        self.miles.append(miles)
        self.states.append(state)
        self.physical.append(physical)
        self.defense.append(defense)
        self.offense.append(offense)
        self.overall_rating.append(overall)
        self.positions.append(position)
        self.read_considering(stats)

        

    def read_considering(self, stats):
        above_low=[]
        highestPrestige=""
        offered=0
        offered1=0
        offered2=0
        offered3=0
        coaches=0
        highest_coach=""
        highest_division=4
        highest_team=""

        for stat in stats:
            division=len(stat[2])-1
            if stat[4].find("Low") == -1:
                interest=stat[0] + ": " + stat[4]
                above_low.append(interest)

            if grade_to_rank.get(stat[3], -4) > grade_to_rank.get(highestPrestige):
                highestPrestige=stat[3]
                highest_coach=stat[1]
                highest_team=stat[0]

            if stat[5]=="Yes":
                offered+=1
                if division==1:
                    offered1+=1
                elif division==2:
                    offered2+=1
                else:
                    offered3+=1

            if division < highest_division:
                highest_division=division

            if stat[1]!= "Sim AI":
                coaches+=1

        if highest_division==4:
            highest_division="NA"
        
        self.highest_team.append(highest_team)
        self.above_low_interest.append(above_low)
        self.highest_prestige.append(highestPrestige)
        self.human_coaches.append(coaches)
        self.offers.append(offered)
        self.offers1.append(offered1) 
        self.offers2.append(offered2)
        self.offers3.append(offered3) 
        self.highest_coach.append(highest_coach)
        self.highest_division.append(highest_division)



    

    def print_players(self):
        for first, last, above, highest, human, offers in zip(self.first_names, self.last_names, self.above_low_interest, self.highest_prestige, self.human_coaches, self.offers):
            print(first," ", last, "low: " , above, ", highest int: ", highest, ", humans: ", human, ", offers: ", offers)


    def create_sheet(self):
        data = {
            "First Name": self.first_names,
            "Last Name": self.last_names,
            "Miles": self.miles,
            "State": self.states,
            "Position": self.positions,
            "Overall" : self.overall_rating,
            "Offense" : self.offense,
            "Defense" : self.defense,
            "Physical" : self.physical,
            "Teams above low interest": self.above_low_interest,
            "Highest Considering Team": self.highest_team,
            "Highest Considering Divsion": self.highest_division,
            "Highest Considering Coach": self.highest_coach,
            "Highest Prestige": self.highest_prestige,
            "Offers " : self.offers,
            "Offers in D1" : self.offers1,
            "Offers in D2" : self.offers2,
            "Offers in D3" : self.offers3,
            "Human Coaches": self.human_coaches
        }
        # Base filename
        base_filename = "hoops_stats"
        extension = ".xlsx"
        counter = 1

        # Generate a unique filename
        filename = f"{base_filename}{extension}"
        while os.path.exists(filename):
            filename = f"{base_filename}_{counter}{extension}"
            counter += 1

        df = pd.DataFrame(data)
        df.to_excel(filename, index=False)
        print(f"DataFrame saved to {filename}")




# # Create a DataFrame
# data = {
#     "ID": [1, 2, 3],
#     "Name": ["Alice", "Bob", "Charlie"],
#     "Age": [25, 30, 35]
# }
# df = pd.DataFrame(data)

# # Save the DataFrame to an Excel file
# df.to_excel("example.xlsx", index=False)

# print("Excel file created: example.xlsx")
