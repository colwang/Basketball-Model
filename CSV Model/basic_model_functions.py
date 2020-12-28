import csv
import string
import numpy as np
from sklearn.linear_model import LinearRegression

class Team():

    def __init__(self, team_name = "League Average", playoffs_year = 2020):

        team_statsheet =  str(playoffs_year) + '_team_per_game_stats' + '.csv'
        opponent_statsheet = str(playoffs_year) + '_opp_team_per_game_stats'  + '.csv'

        with open(team_statsheet) as file:
            team_stats = csv.reader(file)

            self.loaded_info = False

            for team in team_stats:
                name = team[1].replace('*','')
                if name == team_name:
                    self.name = name
                    self.minutes_played = float(team[3])
                    self.field_goals_attempted = float(team[5])
                    self.three_points_made = float(team[7])
                    self.two_points_made = float(team[10])
                    self.free_throws_made = float(team[13])
                    self.free_throws_attempted = float(team[14])
                    self.o_rebound = float(team[16])
                    self.d_rebound = float(team[17])
                    self.steals = float(team[20])
                    self.blocks = float(team[21])
                    self.turnovers = float(team[22])
                    self.fouls = float(team[23])
                    self.points = float(team[24])

                    self.loaded_info = True

            if not self.loaded_info:
                print("Could not find team")

        with open(opponent_statsheet) as file:
            opp_team_stats = csv.reader(file)

            self.loaded_info = False

            for team in opp_team_stats:
                name = team[1].replace('*','')
                if name == team_name:
                    self.opp_field_goals_attempted = float(team[5])
                    self.opp_three_points_made = float(team[7])
                    self.opp_two_points_made = float(team[10])
                    self.opp_free_throws_made = float(team[13])
                    self.opp_free_throws_attempted = float(team[14])
                    self.opp_o_rebound = float(team[16])
                    self.opp_d_rebound = float(team[17])
                    self.opp_steals = float(team[20])
                    self.opp_turnovers = float(team[22])
                    self.opp_fouls = float(team[23])
                    self.opp_points = float(team[24])

                    self.loaded_info = True

            if not self.loaded_info:
                print("Could not find team matchups")

        self.offensive_eFG = (self.two_points_made + 1.5 * self.three_points_made) / self.field_goals_attempted
        self.defensive_eFG = (self.opp_two_points_made + 1.5 * self.opp_three_points_made) / self.opp_field_goals_attempted

        self.offensive_TOV_rate =  self.turnovers / (self.field_goals_attempted + .44 * self.free_throws_attempted + self.turnovers)
        self.defensive_TOV_rate =  self.opp_turnovers / (self.opp_field_goals_attempted + .44 * self.opp_free_throws_attempted + self.opp_turnovers)

        self.free_throw_rate = self.free_throws_made / self.free_throws_attempted

        self.o_rebound_rating = self.o_rebound / (self.o_rebound + self.opp_d_rebound)
        self.opp_o_rebound_rating = self.opp_o_rebound / (self.d_rebound + self.opp_o_rebound)
        self.d_rebound_rating = 1 - self.opp_o_rebound_rating

        #Four Factors
        self.shooting_factor = self.offensive_eFG - self.defensive_eFG
        self.turnover_factor = self.defensive_TOV_rate - self.offensive_TOV_rate
        self.rebounding_factor = self.o_rebound_rating - self.opp_o_rebound_rating
        self.free_throw_factor = self.free_throw_rate

        self.net_rating = self.shooting_factor * .4 * 100 + self.turnover_factor * .25 * 100 + self.rebounding_factor * .2 * 100 + self.free_throw_factor * .15
        # Note: net_rating is roughly accurate, but too severely penalizes team focused on shooting such as the Rockets and the Thunder while
        # inflating teams who score in the paint such as the 76ers and the Lakers

        # self.defensive_rating = (self.defensive_TOV_rate * 100 * .25 + self.d_rebound_rating * 100 * .25 - self.defensive_eFG * 100 * .4 + (self.steals + self.blocks) / (self.opp_field_goals_attempted + self.opp_turnovers) * 100 * .1)
        self.defensive_rating = (self.defensive_TOV_rate * 100 * .30 + self.d_rebound_rating * 100 * .20 - self.defensive_eFG * 100 * .4 + (self.steals + self.blocks) / (self.opp_field_goals_attempted + self.opp_turnovers) * 100 * .1) + 4
        self.offensive_rating = (self.offensive_eFG * 100 * .4 + self.o_rebound_rating * 100 * .20 + self.free_throw_rate * 100 * .05 - self.offensive_TOV_rate * 100 * .25) / 8
        # Defensive rating ranks teams properly, but scale seems difficult to manage
        # Offensive rating seems to have very limited use

        self.game_pace = self.field_goals_attempted + self.opp_field_goals_attempted
        self.shooting_possessions = (1 / (1 - self.o_rebound_rating)) / ((1 / (1 - self.o_rebound_rating)) + (1 / (1 - self.opp_o_rebound_rating))) * self.game_pace + (self.steals - self.opp_steals) - (self.turnovers - self.opp_turnovers) * (18 / 21) - (self.fouls - self.opp_fouls) / 4

        self.calculated_ppg = self.shooting_possessions * self.offensive_eFG * 2 + self.free_throws_made
        # self.calculated_ppg = self.field_goals_attempted * self.offensive_eFG * 2 + self.free_throws_made
        # different ways to calculate ppg

        #for diagnostics
        self.shooting_possessions_diff = self.field_goals_attempted - self.shooting_possessions
        self.calculated_ppg_diff = self.points - self.calculated_ppg
        # appears as if I am overrating the good teams and underrating the bad ones
        # implementing a defensive factor into the calculated PPG might help

    def __str__(self):
        # return("Team stats for {}".format(self.name))
        # return(" Calculated PPG Difference: {}, Shooting Posessions Difference: {}".format(self.calculated_ppg_diff, self.shooting_possessions_diff))
        return (" Net Rating: {}".format(self.net_rating))

def generate_teams():

    team_dict = dict()

    with open('team_per_game_stats_2020.csv') as file:
        teams = csv.DictReader(file)
        for team in teams:
            team_name = team['Team'].replace("*",'')
            mascot = team_name.split()[-1]
            team_dict[mascot] = Team(team_name)

    return team_dict

def sort_teams(team_dict):

    team_ranking = {key: value for key, value in sorted(team_dict.items(), key=lambda item: item[1].net_rating, reverse=True)}

    return team_ranking

def calculate_defensive_factor_ratio(team_dict):

    defensive_rating = []
    opponent_points = []

    for team in team_dict.values():
        defensive_rating.append(team.defensive_rating)
        opponent_points.append(float(team.opp_points/team.minutes_played - team_dict['Average'].opp_points/team_dict['Average'].minutes_played) * 240)

    x = np.array(defensive_rating).reshape(-1,1)
    y = np.array(opponent_points)

    model = LinearRegression().fit(x, y)
    # model = LinearRegression(fit_intercept=False).fit(x, y)

    r_sq = model.score(x,y)
    intercept = model.intercept_
    slope = model.coef_

    # print('Points Scored Difference = {} * Defensive Rating + {}'.format(slope, intercept))
    return r_sq, intercept, slope

def calculate_matchup_points(team1, team2):
    # Without factoring in OT minutes: Points Scored Difference = [-2.71860127] * Defensive Rating + 9.201332686838144
    # Factoring in OT Minutes: Points Scored Difference = [-2.57157722] * Defensive Rating + 8.712697490051784

    game_pace = team1.field_goals_attempted + team2.field_goals_attempted

    # Team 1
    team1_shooting_possessions = (1 / (1 - team1.o_rebound_rating)) / ((1 / (1 - team1.o_rebound_rating)) + (1 / (1 - team2.opp_o_rebound_rating))) * game_pace + (team1.steals - team2.opp_steals) - (team1.turnovers - team2.opp_turnovers) * (18 / 21) - (team1.fouls - team2.opp_fouls) / 4
    team2_defense_effect = -2.57157722 * team2.defensive_rating + 8.712697490051784
    team1_game_points = team1.shooting_possessions * team1.offensive_eFG * 2 + team1.free_throws_made + team2_defense_effect
    # team1_game_points = team1.field_goals_attempted * team1.offensive_eFG * 2 + team1.free_throws_made + team2_defense_effect

    # print("{} shooting possessions: {}".format(team1.name, team1_shooting_possessions))
    # print("{} defense effect: {}".format(team2.name, team2_defense_effect))
    # print("{} game points: {}".format(team1.name, team1_game_points))

    # Team 2
    team2_shooting_possessions = (1 / (1 - team2.o_rebound_rating)) / ((1 / (1 - team1.o_rebound_rating)) + (1 / (1 - team2.opp_o_rebound_rating))) * game_pace + (team2.steals - team1.opp_steals) - (team2.turnovers - team1.opp_turnovers) * (18 / 21) - (team2.fouls - team1.opp_fouls) / 4
    team1_defense_effect = -2.57157722 * team1.defensive_rating + 8.712697490051784
    team2_game_points = team2.shooting_possessions * team2.offensive_eFG * 2 + team2.free_throws_made + team1_defense_effect
    # team2_game_points = team2.field_goals_attempted * team2.offensive_eFG * 2 + team2.free_throws_made + team1_defense_effect

    # print("{} shooting possessions: {}".format(team2.name, team2_shooting_possessions))
    # print("{} defense effect: {}".format(team1.name, team1_defense_effect))
    # print("{} game points: {}".format(team2.name, team2_game_points))

    total_game_points = team1_game_points + team2_game_points

    if team1_game_points > team2_game_points:
        winner = team1.name
        loser = team2.name
        spread = team2_game_points - team1_game_points
        winner_points = team1_game_points
        loser_points = team2_game_points
    else:
        winner = team2.name
        loser = team1.name
        spread = team1_game_points - team2_game_points
        winner_points = team2_game_points
        loser_points = team1_game_points

    return winner, loser, spread, winner_points, loser_points

def calculate_matchup_FF_spread(team1, team2):

    game_pace = team1.field_goals_attempted + team2.field_goals_attempted

    # Team 1
    team1_shooting_possessions = (1 / (1 - team1.o_rebound_rating)) / ((1 / (1 - team1.o_rebound_rating)) + (1 / (1 - team2.opp_o_rebound_rating))) * game_pace + (team1.steals - team2.opp_steals) - (team1.turnovers - team2.opp_turnovers) * (18 / 21) - (team1.fouls - team2.opp_fouls) / 4
    team2_defense_effect = -2.57157722 * team2.defensive_rating + 8.712697490051784
    team1_game_points = team1.shooting_possessions * team1.offensive_eFG * 2 + team1.free_throws_made + team2_defense_effect
    # team1_game_points = team1.field_goals_attempted * team1.offensive_eFG * 2 + team1.free_throws_made + team2_defense_effect

    # print("{} shooting possessions: {}".format(team1.name, team1_shooting_possessions))
    # print("{} defense effect: {}".format(team2.name, team2_defense_effect))
    # print("{} game points: {}".format(team1.name, team1_game_points))

    # Team 2
    team2_shooting_possessions = (1 / (1 - team2.o_rebound_rating)) / ((1 / (1 - team1.o_rebound_rating)) + (1 / (1 - team2.opp_o_rebound_rating))) * game_pace + (team2.steals - team1.opp_steals) - (team2.turnovers - team1.opp_turnovers) * (18 / 21) - (team2.fouls - team1.opp_fouls) / 4
    team1_defense_effect = -2.57157722 * team1.defensive_rating + 8.712697490051784
    team2_game_points = team2.shooting_possessions * team2.offensive_eFG * 2 + team2.free_throws_made + team1_defense_effect
    # team2_game_points = team2.field_goals_attempted * team2.offensive_eFG * 2 + team2.free_throws_made + team1_defense_effect

    # print("{} shooting possessions: {}".format(team2.name, team2_shooting_possessions))
    # print("{} defense effect: {}".format(team1.name, team1_defense_effect))
    # print("{} game points: {}".format(team2.name, team2_game_points))

    total_game_points = team1_game_points + team2_game_points

    # ff_spread = ((team1.shooting_factor - team2.shooting_factor) * .4 + (team1.turnover_factor - team2.turnover_factor) * .25 + (team1.rebounding_factor - team2.rebounding_factor) * .2 + (team1.free_throw_rate - team2.free_throw_rate) * 100 * .15) * 2
    # print("Team1 net rating: {}".format(team1.net_rating))
    # print("Team2 net rating: {}".format(team2.net_rating))
    ff_spread = (team1.net_rating - team2.net_rating) * 2
    # print("ff_spread: {}".format(ff_spread))

    if ff_spread > 0:
        winner = team1.name
        loser = team2.name
        spread = -1 * ff_spread
        winner_points = (total_game_points - ff_spread) / 2 + ff_spread
        loser_points = (total_game_points - ff_spread) / 2
    else:
        winner = team2.name
        loser = team1.name
        spread = ff_spread
        winner_points = (total_game_points + ff_spread) / 2 - ff_spread
        loser_points = (total_game_points + ff_spread) / 2

    return winner, loser, spread, winner_points, loser_points

def testing_schedule(year = 2020, month = 'february'):

    schedule_name = month + '_schedule_' + str(year) + '.csv'

    test_result = dict()
    test_result['right'] = 0
    test_result['wrong'] = 0

    spread_difference = list()

    point_total_difference = list()

    team_dict = generate_teams()

    with open(schedule_name) as schedule:
        matchup_reader = csv.reader(schedule)
        next(matchup_reader)

        for matchup in matchup_reader:
            visiting_team = matchup[2]
            visiting_team_points = matchup[3]
            home_team = matchup[4]
            home_team_points = matchup[5]
            actual_point_total = int(visiting_team_points) + int(home_team_points)

            if visiting_team_points > home_team_points:
                win = visiting_team
                loss = home_team
                actual_spread = int(visiting_team_points) - int(home_team_points)
                winner_points = visiting_team_points
                loser_points = home_team_points
            else:
                win = home_team
                loss = visiting_team
                actual_spread = int(home_team_points) - int(visiting_team_points)
                winner_points = home_team_points
                loser_points = visiting_team_points

            visitor_mascot = visiting_team.split()[-1]
            home_mascot = home_team.split()[-1]
            visitors = team_dict[visitor_mascot]
            home = team_dict[home_mascot]

            # predicted_winner, predicted_loser, predicted_spread, predicted_winner_points, predicted_loser_points = calculate_matchup_points(visitors, home)
            predicted_winner, predicted_loser, predicted_spread, predicted_winner_points, predicted_loser_points = calculate_matchup_FF_spread(visitors, home)
            predicted_point_total = predicted_winner_points + predicted_loser_points

            if predicted_winner == win:
                test_result['right'] += 1
            else:
                test_result['wrong'] += 1
                predicted_spread = -1 * predicted_spread

            spread_difference.append(actual_spread - predicted_spread)
            point_total_difference.append(actual_point_total - predicted_point_total)

        correct_percentage = test_result['right'] / (test_result['right'] + test_result['wrong']) * 100
        average_spread_difference = sum(spread_difference) / len(spread_difference)
        average_point_total_difference = sum(point_total_difference) / len(point_total_difference)

        return correct_percentage, average_spread_difference, average_point_total_difference
