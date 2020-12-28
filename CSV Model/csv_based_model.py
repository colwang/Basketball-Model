import csv
import basic_model_functions as basic

# mavs = basic.Team('Dallas Mavericks')
#
# if mavs.loaded_info:
#     # print("The Dallas Mavericks have averaged {} ppg this season".format(mavs.points))
#     # print("The Dallas Mavericks had on average {} ppg scored against them this season".format(mavs.opp_points))
#     # print('''Dallas Mavericks Four Factor Stats:
#     #         Shooting: {}
#     #         Turnovers: {}
#     #         Rebounding: {}
#     #         Free Throws: {}
#     #         Net Rating: {}'''.format(mavs.shooting_factor, mavs.turnover_factor, mavs.rebounding_factor, mavs.free_throw_factor, mavs.net_rating)
#     #      )
#     # print('''Dallas Mavericks
#     #         Shooting Possessions per game: {}
#     #         Offensive Rebounding: {}
#     #         Oppenent Offensive Rebounding: {}
#     #         Game Pace: {}'''.format(mavs.shooting_possessions, mavs.o_rebound_rating, mavs.opp_o_rebound_rating, mavs.game_pace))
#     # print('Dallas Mavericks calculated PPG: {}'.format(mavs.calculated_ppg))
#     pass


# team_dict = basic.generate_teams()
# team_ranking = basic.sort_teams(team_dict)
#
# for key, value in team_ranking.items():
#     print(key + str(value))

# r_sq, intercept, slope = basic.calculate_defensive_factor_ratio(team_ranking)
# print('Points Scored Difference = {} * Defensive Rating + {}'.format(slope, intercept))
# print("r_sq = {}".format(r_sq))



# # Interesting Test Cases
#
# hawks = basic.Team('Atlanta Hawks')
# cavs = basic.Team('Cleveland Cavaliers')
# # the hawks and the cavs are two of the worst teams in the NBA, but also two of the most underrated opp_team_stats
# # both have average offensive eFG, but while the hawks are badly out offensively rebounded, the cavs out offensively rebound their opponents
# # INSIGHT - they are bad because of the fact that they have so many turnovers. Pace in my model is shooting possessions, not all possessions
# # so as a result, turnovers have a disproportionately large impact.
# # CORRECTION - change the turnover impact ratio by 18/21 (approx 90 shooting possession every 105 real possessions)
#
# grizzlies = basic.Team('Memphis Grizzlies')
# rockets = basic.Team('Houston Rockets')
# seventy_sixers = basic.Team('Philadelphia 76ers')
# magic = basic.Team('Orlando Magic')
#
# print('''Hawks Stats:
#         Offensive Rebound rate: {}
#         Opponent Offensive Rebound rate: {}
#         Game Pace: {}
#         Shooting Possessions: {}
#         eFG: {}
#         Field Goals Attempted: {}
#         '''.format(hawks.o_rebound_rating, hawks.opp_o_rebound_rating, hawks.game_pace, hawks.shooting_possessions, hawks.offensive_eFG, hawks.field_goals_attempted))
#
# print('''Cavs Stats:
#         Offensive Rebound rate: {}
#         Opponent Offensive Rebound rate: {}
#         Game Pace: {}
#         Shooting Possessions: {}
#         eFG: {}
#         Field Goals Attempted: {}
#         '''.format(cavs.o_rebound_rating, cavs.opp_o_rebound_rating, cavs.game_pace, cavs.shooting_possessions, cavs.offensive_eFG, cavs.field_goals_attempted))
#
# print('''Grizzlies Stats:
#         Offensive Rebound rate: {}
#         Opponent Offensive Rebound rate: {}
#         Game Pace: {}
#         Shooting Possessions: {}
#         eFG: {}
#         Field Goals Attempted: {}
#         '''.format(grizzlies.o_rebound_rating, grizzlies.opp_o_rebound_rating, grizzlies.game_pace, grizzlies.shooting_possessions, grizzlies.offensive_eFG, grizzlies.field_goals_attempted))
#
# print('''Rockets Stats:
#         Offensive Rebound rate: {}
#         Opponent Offensive Rebound rate: {}
#         Game Pace: {}
#         Shooting Possessions: {}
#         eFG: {}
#         Field Goals Attempted: {}
#         '''.format(rockets.o_rebound_rating, rockets.opp_o_rebound_rating, rockets.game_pace, rockets.shooting_possessions, rockets.offensive_eFG, rockets.field_goals_attempted))
#
# print('''76ers Stats:
#         Offensive Rebound rate: {}
#         Opponent Offensive Rebound rate: {}
#         Game Pace: {}
#         Shooting Possessions: {}
#         eFG: {}
#         Field Goals Attempted: {}
#         '''.format(seventy_sixers.o_rebound_rating, seventy_sixers.opp_o_rebound_rating, seventy_sixers.game_pace, seventy_sixers.shooting_possessions, seventy_sixers.offensive_eFG, seventy_sixers.field_goals_attempted))
#
# print('''Magic Stats:
#         Offensive Rebound rate: {}
#         Opponent Offensive Rebound rate: {}
#         Game Pace: {}
#         Shooting Possessions: {}
#         eFG: {}
#         Field Goals Attempted: {}
#         '''.format(magic.o_rebound_rating, magic.opp_o_rebound_rating, magic.game_pace, magic.shooting_possessions, magic.offensive_eFG, magic.field_goals_attempted))

# # Mock matchups
# hawks = basic.Team('Atlanta Hawks')
# bucks = basic.Team('Milwaukee Bucks')
# magic = basic.Team('Orlando Magic')
# celtics = basic.Team('Boston Celtics')
# rockets = basic.Team('Houston Rockets')
# thunder = basic.Team('Oklahoma City Thunder')
# blazers = basic.Team('Portland Trail Blazers')
# lakers = basic.Team('Los Angeles Lakers')
# warriors = basic.Team('Golden State Warriors', 2019)
#
# # winner, loser, spread, winner_points, loser_points = basic.calculate_matchup_points(bucks, hawks)
# winner, loser, spread, winner_points, loser_points = basic.calculate_matchup_FF_spread(lakers, rockets)
# print("Prediction: {} - {}, {} - {}, Spread: {}".format(winner, winner_points, loser, loser_points, spread))



# correct_percentage, average_spread_difference, average_point_total_difference = basic.testing_schedule(2020, "january")
correct_percentage, average_spread_difference, average_point_total_difference = basic.testing_schedule()
#
print("The model was {}% correct, with an average spread difference of {} and an average point total difference of {}".format(correct_percentage, average_spread_difference, average_point_total_difference))
