import csv
import pandas as pd

class Team():

    def __init__(self, team_name = "League Average", playoffs_year = 2020):

        team_statsheet =  str(playoffs_year) + '_team_per_game_stats.csv'
        opponent_statsheet = str(playoffs_year) + '_opp_team_per_game_stats.csv'

        self.name = team_name

        teams_df = pd.read_csv(team_statsheet)
        teams_df = teams_df.set_index('Team')
        team_info = teams_df.loc[self.name]

        # print(team_df)
        # print(team_df.loc[self.name])
        # print(team_info)
        # print(type(team_info))

        self.field_goals_attempted = float(team_info['FGA'])
        # print(self.field_goals_attempted)
        self.three_points_made = float(team_info['3P'])
        # print(self.three_points_made)
        self.two_points_made = float(team_info['2P'])
        # print(self.two_points_made)
        self.free_throws_made = float(team_info['FT'])
        self.free_throws_attempted = float(team_info['FTA'])
        self.o_rebound = float(team_info['ORB'])
        self.d_rebound = float(team_info['DRB'])
        self.turnovers = float(team_info['TOV'])

        opps_df = pd.read_csv(opponent_statsheet)
        opps_df = opps_df.set_index('Team')
        opp_info = opps_df.loc[self.name]

        self.opp_field_goals_attempted = float(opp_info['FGA'])
        self.opp_three_points_made = float(opp_info['3P'])
        self.opp_two_points_made = float(opp_info['2P'])
        self.opp_free_throws_made = float(opp_info['FT'])
        self.opp_free_throws_attempted = float(opp_info['FTA'])
        self.opp_o_rebound = float(opp_info['ORB'])
        self.opp_d_rebound = float(opp_info['DRB'])
        self.opp_turnovers = float(opp_info['TOV'])

        self.offensive_eFG = (self.two_points_made + 1.5 * self.three_points_made) / self.field_goals_attempted
        # print(self.offensive_eFG)
        self.defensive_eFG = (self.opp_two_points_made + 1.5 * self.opp_three_points_made) / self.opp_field_goals_attempted

        self.offensive_TOV_rate =  self.turnovers / (self.field_goals_attempted + .44 * self.free_throws_attempted + self.turnovers)
        self.defensive_TOV_rate =  self.opp_turnovers / (self.opp_field_goals_attempted + .44 * self.opp_free_throws_attempted + self.opp_turnovers)

        self.free_throw_rate = self.free_throws_made / self.free_throws_attempted

        self.o_rebound_rating = self.o_rebound / (self.o_rebound + self.opp_d_rebound)
        self.opp_o_rebound_rating = self.opp_o_rebound / (self.d_rebound + self.opp_o_rebound)

        #Four Factors
        self.shooting_factor = self.offensive_eFG - self.defensive_eFG
        self.turnover_factor = self.defensive_TOV_rate - self.offensive_TOV_rate
        self.rebounding_factor = self.o_rebound_rating - self.opp_o_rebound_rating
        self.free_throw_factor = self.free_throw_rate

    def get_team_ff_data(self):
        ff_data = [self.name, self.shooting_factor * 10, self.turnover_factor * 10, self.rebounding_factor * 10, self.free_throw_factor]

        return ff_data