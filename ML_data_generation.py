import csv
import pandas as pd
import numpy as np

class data_gen:

    def __init__(self, first_playoff_year, last_playoff_year):

        self.training_data = []

        playoff_year = first_playoff_year
        for i in range(last_playoff_year - first_playoff_year + 1):
        
            with open(str(playoff_year) + "_NBA_schedule.csv") as file:       #open team per game and opp per game csvs simulatenously
                games = csv.reader(file)
                for game in games:
                    away_team = game[2]
                    away_pts = game[3]
                    home_team = game[4]
                    home_points = game[5]

            with open(str(playoff_year) + "_team_per_game_stats.csv") as file:
                team_df = pd.read_csv(file)
                print (team_df)

            
