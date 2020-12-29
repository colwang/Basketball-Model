from ML_data_generation import *
from calculate_teams import *

data = data_gen(2020, 2020)
# data.generate_team_data()
game_data_2020 = data.generate_data_points()
print(game_data_2020[0])

shuffled_game_data_2020 = data.shuffle_data()
print(shuffled_game_data_2020[0])

print("Home Wins:", data.home_wins)
print("Away Wins:", data.away_wins)


# print(type(np.eye(2)[1]))
# print(type(np.eye(2)[1].tolist()))

# bucks = Team("Milwaukee Bucks", 2020)
# print(bucks.get_team_ff_data())