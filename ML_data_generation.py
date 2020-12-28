import csv
import pandas as pd
import numpy as np
from calculate_teams import Team

class data_gen:

    def __init__(self, first_playoff_year, last_playoff_year):

        self.data_points = []
        self.start_year = first_playoff_year
        self.end_year = last_playoff_year
        self.LABELS = {"Away Win": 0, "Home Win": 1}

    def strip_asterisks(self, file_name): 
        
        with open(file_name, "r") as in_file:
            reader = csv.reader(in_file, delimiter=',')
        
            all_rows = []
            for row in reader:
                row_elements = []
                for element in row:
                    row_elements.append(element)
                row_elements[1] = row_elements[1].replace("*","")
                all_rows.append(row_elements)


        with open(file_name, "w") as out_file:
                writer = csv.writer(out_file, delimiter=',')
                for row in all_rows:
                    writer.writerow(row)

    
    def generate_team_data(self):
        playoff_year = self.start_year
        for i in range(self.end_year - self.start_year + 1):

            playoff_year += i

            file_name = str(playoff_year) + "_team_per_game_stats.csv"
            team_names = pd.read_csv(file_name)["Team"]
            team_names = team_names.sort_values()
            
            teams_data_file = str(playoff_year) + "_team_ff_data.csv"
            with open(teams_data_file, "w") as out_file:
                data_writer = csv.writer(out_file, delimiter=',')
                data_writer.writerow(["Team", "Shooting Factor", "Turnover Factor", "Rebounding Factor", "Free Throw Factor"])

                for name in team_names:
                    team_ff = Team(name, playoff_year)
                    data_writer.writerow(team_ff.get_team_ff_data())
    
    def generate_data_points(self):
        playoff_year = self.start_year
        for i in range(self.end_year - self.start_year + 1):
        
            with open(str(playoff_year) + "_NBA_schedule.csv", "r") as schedule_file, open(str(playoff_year) + "_team_ff_data.csv", "r") as team_file:
                games = csv.reader(schedule_file)
                teams_ff_df = pd.read_csv(team_file)
                teams_ff_df = teams_ff_df.set_index("Team")

                # print(teams_ff_df.loc["Milwaukee Bucks"])
                # print(teams_ff_df.loc["Milwaukee Bucks"].iloc[0])

                header = next(games)
                for game in games:
                    away_team = game[2]
                    away_pts = int(game[3])
                    home_team = game[4]
                    home_points = int(game[5])

                    away_ff = teams_ff_df.loc[away_team]
                    home_ff = teams_ff_df.loc[home_team]

                    # away ff data, home ff data
                    X = [away_ff.iloc[0], away_ff.iloc[1], away_ff.iloc[2], away_ff.iloc[3],
                         home_ff.iloc[0], home_ff.iloc[1], home_ff.iloc[2], home_ff.iloc[3]]

                    if away_pts > home_points:
                        y = np.eye(2)[0].tolist()
                    else:
                        y = np.eye(2)[1].tolist()

                    self.data_points.append([X, y])

        return self.data_points






            

        

            
