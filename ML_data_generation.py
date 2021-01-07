import csv
import pandas as pd
import numpy as np
import torch
from tqdm import tqdm
import math
import random
from calculate_teams import Team

class data_gen:

    def __init__(self, first_playoff_year, last_playoff_year):

        self.data_points = []
        self.start_year = first_playoff_year
        self.end_year = last_playoff_year
        self.LABELS = {"Away Win": 0, "Home Win": 1}
        
        # for h2h data balancing
        self.home_wins = 0
        self.away_wins = 0

        # for spread data balancing
        self.home_wins_6 = 0
        self.home_wins_5 = 0
        self.home_wins_4 = 0
        self.home_wins_3 = 0
        self.home_wins_2 = 0
        self.home_wins_1 = 0
        self.buzzer_beater = 0
        self.away_wins_1 = 0
        self.away_wins_2 = 0
        self.away_wins_3 = 0
        self.away_wins_4 = 0
        self.away_wins_5 = 0


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

    
    def generate_raw_team_data(self):
        playoff_year = self.start_year
        for i in range(self.end_year - self.start_year + 1):

            file_name = str(playoff_year) + "_team_per_game_stats.csv"
            team_names = pd.read_csv(file_name)["Team"]
            team_names = team_names.sort_values()
            
            teams_data_file = str(playoff_year) + "_team_raw_ff_data.csv"
            with open(teams_data_file, "w") as out_file:
                data_writer = csv.writer(out_file, delimiter=',')
                data_writer.writerow(["Team", "Shooting Factor", "Turnover Factor", "Rebounding Factor", "Free Throw Factor"])

                for name in team_names:
                    team_ff = Team(name, playoff_year)
                    data_writer.writerow(team_ff.get_team_ff_data())
            
            playoff_year += 1

    def generate_z_score_data(self):
        playoff_year = self.start_year
        for i in range(self.end_year - self.start_year + 1):

            raw_file_name = str(playoff_year) + "_team_raw_ff_data.csv"
            ff_df = pd.read_csv(raw_file_name)
            team_names = ff_df["Team"]
            team_names = team_names.sort_values()

            averages = ff_df.mean()
            shooting_avg = averages["Shooting Factor"]
            turnover_avg = averages["Turnover Factor"]
            rebound_avg = averages["Rebounding Factor"]
            ft_avg = averages["Free Throw Factor"]

            # print(averages)
            # print(averages["Shooting Factor"])

            deviations = ff_df.std()
            shooting_std = deviations["Shooting Factor"]
            turnover_std = deviations["Turnover Factor"]
            rebound_std = deviations["Rebounding Factor"]
            ft_std = deviations["Free Throw Factor"]

            # print(deviations)
            # print(deviations["Shooting Factor"])

            z_data_file = str(playoff_year) + "_team_z_ff_data.csv"
            ff_df = ff_df.set_index("Team")

            with open(z_data_file, "w") as out_file:
                data_writer = csv.writer(out_file, delimiter=',')
                data_writer.writerow(["Team", "Shooting Factor", "Turnover Factor", "Rebounding Factor", "Free Throw Factor"])

                for name in team_names:
                    ff_z_scores = [name]
                    ff_z_scores.append((ff_df.loc[name]["Shooting Factor"] - shooting_avg) / shooting_std)
                    ff_z_scores.append((ff_df.loc[name]["Turnover Factor"] - turnover_avg) / turnover_std)
                    ff_z_scores.append((ff_df.loc[name]["Rebounding Factor"] - rebound_avg) / rebound_std)
                    ff_z_scores.append((ff_df.loc[name]["Free Throw Factor"] - ft_avg) / ft_std)

                    data_writer.writerow(ff_z_scores)

            playoff_year += 1
    
    def generate_h2h_data_points(self, spread_for_away):           
        self.data_points = []              
        playoff_year = self.start_year
        for i in range(self.end_year - self.start_year + 1):
        
            with open(str(playoff_year) + "_NBA_schedule.csv", "r") as schedule_file, open(str(playoff_year) + "_team_z_ff_data.csv", "r") as team_file:
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
                    home_pts = int(game[5])

                    away_ff = teams_ff_df.loc[away_team]
                    home_ff = teams_ff_df.loc[home_team]

                    spread_changer = random.randint(-25, 25)
                    spread = spread_for_away + spread_changer

                    # away ff data, home ff data
                    X = [away_ff.iloc[0], away_ff.iloc[1], away_ff.iloc[2], away_ff.iloc[3],
                         home_ff.iloc[0], home_ff.iloc[1], home_ff.iloc[2], home_ff.iloc[3],
                         spread_for_away]

                    # if away_pts + spread > home_pts:
                    if away_pts + spread_for_away > home_pts:
                        y = np.eye(2)[0].tolist()
                        self.away_wins += 1
                    else:
                        y = np.eye(2)[1].tolist()
                        self.home_wins += 1

                    self.data_points.append([X, y])
            
            playoff_year += 1

        return self.data_points

    def generate_spread_data_points(self):
        self.data_points = []    
        playoff_year = self.start_year
        for i in range(self.end_year - self.start_year + 1):
        
            with open(str(playoff_year) + "_NBA_schedule.csv", "r") as schedule_file, open(str(playoff_year) + "_team_z_ff_data.csv", "r") as team_file:
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
                    home_pts = int(game[5])

                    away_ff = teams_ff_df.loc[away_team]
                    home_ff = teams_ff_df.loc[home_team]

                    # away ff data, home ff data
                    X = [away_ff.iloc[0], away_ff.iloc[1], away_ff.iloc[2], away_ff.iloc[3],
                         home_ff.iloc[0], home_ff.iloc[1], home_ff.iloc[2], home_ff.iloc[3]]

                    if away_pts - 18 > home_pts:
                        y = np.eye(12)[0].tolist()
                        self.away_wins_5 += 1
                    elif away_pts - 12 > home_pts:
                        y = np.eye(12)[1].tolist()
                        self.away_wins_4 += 1
                    elif away_pts - 8 > home_pts:
                        y = np.eye(12)[2].tolist()
                        self.away_wins_3 += 1
                    elif away_pts - 5 > home_pts:
                        y = np.eye(12)[3].tolist()
                        self.away_wins_2 += 1
                    elif away_pts - 2 > home_pts:
                        y = np.eye(12)[4].tolist()
                        self.away_wins_1 += 1
                    elif home_pts - 20 > away_pts:
                        y = np.eye(12)[11].tolist()
                        self.home_wins_6 += 1
                    elif home_pts - 14 > away_pts:
                        y = np.eye(12)[10].tolist()
                        self.home_wins_5 += 1
                    elif home_pts - 10 > away_pts:
                        y = np.eye(12)[9].tolist()
                        self.home_wins_4 += 1
                    elif home_pts - 7 > away_pts:
                        y = np.eye(12)[8].tolist()
                        self.home_wins_3 += 1
                    elif home_pts - 5 > away_pts:
                        y = np.eye(12)[7].tolist()
                        self.home_wins_2 += 1
                    elif home_pts - 2 > away_pts:
                        y = np.eye(12)[6].tolist()
                        self.home_wins_1 += 1
                    else:
                        y = np.eye(12)[5].tolist()
                        self.buzzer_beater += 1
                    

                    self.data_points.append([X, y])
            
            playoff_year += 1

        return self.data_points


    def shuffle_data(self):

        np_data = np.array(self.data_points, dtype=object)
        np.random.shuffle(np_data)
        self.data_points = np_data.tolist()

        return self.data_points

    def create_tensors(self, data, VAL_PCT): 

        X = torch.Tensor([i[0] for i in data])
        y = torch.Tensor([i[1] for i in data])

        val_size = int(len(X) * VAL_PCT)
        train_X = X[:-val_size]
        train_y = y[:-val_size]

        test_X = X[-val_size:]
        test_y = y[-val_size:]
        # print(test_y)

        # print(len(train_X), len(test_X))

        return train_X, train_y, test_X, test_y

    def generate_matchup(self, home_team, away_team, spread_for_away, playoff_year):

        with open(str(playoff_year) + "_team_z_ff_data.csv", "r") as team_file:
            teams_ff_df = pd.read_csv(team_file)
            teams_ff_df = teams_ff_df.set_index("Team")

            away_ff = teams_ff_df.loc[away_team]
            home_ff = teams_ff_df.loc[home_team]

            # away ff data, home ff data
            X = [away_ff.iloc[0], away_ff.iloc[1], away_ff.iloc[2], away_ff.iloc[3],
                 home_ff.iloc[0], home_ff.iloc[1], home_ff.iloc[2], home_ff.iloc[3],
                 spread_for_away]

            tensor_X = torch.Tensor(X)

            return tensor_X, home_team, away_team


    def balance_data(self, is_h2h):
        games_removed = 0

        if is_h2h:
            data_iterator = 0
            while self.home_wins * .9 > self.away_wins:

                if int(self.data_points[data_iterator][1][1]) == 1:
                    del self.data_points[data_iterator]
                    games_removed += 1
                    self.home_wins -= 1

                    # print("Removed Game")
                else:
                    data_iterator += 1

            while self.away_wins * .9 > self.home_wins:

                if int(self.data_points[data_iterator][1][0]) == 1:
                    del self.data_points[data_iterator]
                    games_removed += 1
                    self.away_wins -= 1

                    # print("Removed Game")
                else:
                    data_iterator += 1

        else:
            # wins_array = np.array([{"Home Win 6": self.home_wins_6}, {"Home Win 5": self.home_wins_5}, {"Home Win 4": self.home_wins_4}, 
            #                        {"Home Win 3": self.home_wins_3}, {"Home Win 2": self.home_wins_2}, {"Home Win 1": self.home_wins_1}, 
            #                        {"Buzzer Beater": self.buzzer_beater}, {"Away Win 1": self.away_wins_1}, {"Away Win 2": self.away_wins_2}
            #                        {"Away Win 3": self.away_wins_3}, {"Away Win 4": self.away_wins_4}, {"Away Win 5": self.away_wins_5}])

            wins_array = [{"Tensor": 11, "Count": self.home_wins_6}, {"Tensor": 10, "Count": self.home_wins_5}, {"Tensor": 9, "Count": self.home_wins_4}, 
                          {"Tensor": 8, "Count": self.home_wins_3}, {"Tensor": 7, "Count": self.home_wins_2}, {"Tensor": 6, "Count": self.home_wins_1}, 
                          {"Tensor": 5, "Count": self.buzzer_beater}, {"Tensor": 4, "Count": self.away_wins_1}, {"Tensor": 3, "Count": self.away_wins_2},
                          {"Tensor": 2, "Count": self.away_wins_3}, {"Tensor": 1, "Count": self.away_wins_4}, {"Tensor": 0, "Count": self.away_wins_5}]

            wins_array = sorted(wins_array, key = lambda i: i["Count"], reverse=True)
            max_count = wins_array[-1]["Count"] * 1.05

            # print(max_count)
            # print(wins_array)

            for result in wins_array:
                num_to_delete = math.ceil(result["Count"] - max_count)
                deleted = 0
                if num_to_delete < 0:
                    num_to_delete = 0
                data_iterator = 0
                tensor_num = result["Tensor"]

                # print("Tensor:", tensor_num)
                # print("Num to delete:", num_to_delete)

                while deleted < num_to_delete:
                    if int(self.data_points[data_iterator][1][tensor_num]) == 1:
                        del self.data_points[data_iterator]
                        deleted += 1
                        games_removed += 1
                        
                        if tensor_num == 0:
                            self.away_wins_5 -= 1
                        elif tensor_num == 1:
                            self.away_wins_4 -= 1
                        elif tensor_num == 2:
                            self.away_wins_3 -= 1
                        elif tensor_num == 3:
                            self.away_wins_2 -= 1
                        elif tensor_num == 4:
                            self.away_wins_1 -= 1
                        elif tensor_num == 5:
                            self.buzzer_beater -= 1
                        elif tensor_num == 6:
                            self.home_wins_1 -= 1
                        elif tensor_num == 7:
                            self.home_wins_2 -= 1
                        elif tensor_num == 8:
                            self.home_wins_3 -= 1
                        elif tensor_num == 9:
                            self.home_wins_4 -= 1
                        elif tensor_num == 10:
                            self.home_wins_5 -= 1
                        else:
                            self.home_wins_6 -= 1

                        # print("Removed Game")
                    else:
                        data_iterator += 1

        print("Removed", games_removed, "to balance data")









            

        

            
