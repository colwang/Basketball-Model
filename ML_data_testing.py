from ML_data_generation import *
from calculate_teams import *

data = data_gen(2021, 2021)

# data.strip_asterisks("2017_team_per_game_stats.csv")

data.generate_raw_team_data()
data.generate_z_score_data()

# game_data_2020 = data.generate_h2h_data_points(0)
# game_data_2020 = data.generate_spread_data_points()
# print(game_data_2020[0])

# shuffled_game_data_2020 = data.shuffle_data()
# print(shuffled_game_data_2020[0])

# data.create_tensors(shuffled_game_data_2020, .01)

# print("Home Wins:", data.home_wins)
# print("Away Wins:", data.away_wins)

# data.balance_data(True)

# print("Home Wins:", data.home_wins)
# print("Away Wins:", data.away_wins)

# print("Home Win 6:", data.home_wins_6)
# print("Home Win 5:", data.home_wins_5)
# print("Home Win 4:", data.home_wins_4)
# print("Home Win 3:", data.home_wins_3)
# print("Home Win 2:", data.home_wins_2)
# print("Home Win 1:", data.home_wins_1)
# print("Buzzer Beaters:", data.buzzer_beater)
# print("Away Win 1:", data.away_wins_1)
# print("Away Win 2:", data.away_wins_2)
# print("Away Win 3:", data.away_wins_3)
# print("Away Win 4:", data.away_wins_4)
# print("Away Win 5:", data.away_wins_5)

# data.balance_data(False)

# print("Home Win 6:", data.home_wins_6)
# print("Home Win 5:", data.home_wins_5)
# print("Home Win 4:", data.home_wins_4)
# print("Home Win 3:", data.home_wins_3)
# print("Home Win 2:", data.home_wins_2)
# print("Home Win 1:", data.home_wins_1)
# print("Buzzer Beaters:", data.buzzer_beater)
# print("Away Win 1:", data.away_wins_1)
# print("Away Win 2:", data.away_wins_2)
# print("Away Win 3:", data.away_wins_3)
# print("Away Win 4:", data.away_wins_4)
# print("Away Win 5:", data.away_wins_5)

# print(type(np.eye(2)[1]))
# print(type(np.eye(2)[1].tolist()))

# bucks = Team("Milwaukee Bucks", 2020)
# print(bucks.get_team_ff_data())

# y = torch.Tensor([1,0])
# print(y)