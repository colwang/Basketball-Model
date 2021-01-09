import torch
import torch.optim as optim
from tqdm import tqdm
import tensorflow as tf
from ML_data_generation import *
from ML_net import *

data = data_gen(2017, 2020)
data.generate_h2h_data_points(0)
shuffled_game_data = data.shuffle_data()

# print("Home Wins:", data.home_wins)
# print("Away Wins:", data.away_wins)

data.balance_data(True)

train_X, train_y, test_X, test_y = data.create_tensors(shuffled_game_data, .2)

BATCH_SIZE = 50                     # number of games we run each time
EPOCHS = 50                          # how many times we run through the training data in general


# OPTIMIZATION STEP
optimizer = optim.Adam(h2h_net.parameters(), lr=8e-5)
loss_function = nn.MSELoss()


for epoch in tqdm(range(EPOCHS)):
    for i in range(0, len(train_X), BATCH_SIZE):
    
        batch_X = train_X[i:i+BATCH_SIZE].view(-1, 9)
        batch_y = train_y[i:i+BATCH_SIZE]

        h2h_net.zero_grad()
        
        outputs = h2h_net(batch_X)
        loss = loss_function(outputs, batch_y)
        loss.backward()
        optimizer.step()

    # print(f"Epoch: {epoch + 1}. Loss: {loss}")

overestimated_home_team = 0
underestimated_home_team = 0
correct = 0
total = 0
with torch.no_grad():
    for i in range(len(test_X)):
        real_class = torch.argmax(test_y[i])
        net_out = h2h_net(test_X[i].view(-1, 9))
        predicted_class = torch.argmax(net_out)

        # print("Predicted:", predicted_class)
        # print("Actual:", real_class)

        if predicted_class > real_class:
            overestimated_home_team += 1
        elif predicted_class < real_class: 
            underestimated_home_team += 1
        elif predicted_class == real_class:
            correct += 1
        total += 1

print("Total Test cases:", total)
accuracy = round(correct/total, 3)
print("Accuracy: ", accuracy)
print("Overestimated home team", overestimated_home_team, "times")
print("Underestimated home team", underestimated_home_team, "times")




# SPECIFIC CASE TESTING

for spread in range(-10, 20):
    tensor_X, home_team, away_team, spread = data.generate_matchup("Washington Wizards", "Miami Heat", spread, 2021)

    with torch.no_grad():
        net_out = h2h_net(tensor_X.view(-1, 9))
        predicted_class = torch.argmax(net_out)

        if predicted_class.tolist() == 1:
            predicted_winner = home_team
        else:
            predicted_winner = away_team

        print("Predicted winner for away spread", spread, ":", predicted_winner)

# tensor_X, home_team, away_team, spread = data.generate_matchup("Detroit Pistons", "Phoenix Suns", 0, 2021)

# with torch.no_grad():
#     net_out = h2h_net(tensor_X.view(-1, 9))
#     predicted_class = torch.argmax(net_out)

#     if predicted_class.tolist() == 1:
#         predicted_winner = home_team
#     else:
#         predicted_winner = away_team

#     print("Predicted winner for away spread", spread, ":", predicted_winner)




# # BACKTESTING

# playoff_year = data.start_year
# for i in range(data.end_year - data.start_year + 1):
#     print("------------ TESTING AGAINST", playoff_year, "NBA SCHEDULE ------------")

#     backtesting_data = data_gen(playoff_year, playoff_year)

#     # backtesting_data.generate_h2h_data_points(5)
#     shuffled_backtesting_data = backtesting_data.shuffle_data()

#     empty_X, empty_y, backtesting_X, backtesting_y = data.create_tensors(shuffled_backtesting_data, 1)

#     overestimated_home_team = 0
#     underestimated_home_team = 0
#     correct = 0
#     total = 0
#     with torch.no_grad():
#         for i in range(len(backtesting_X)):
#             real_class = torch.argmax(backtesting_y[i])
#             net_out = h2h_net(backtesting_X[i].view(-1, 9))
#             predicted_class = torch.argmax(net_out)

#             # print("Predicted:", predicted_class)
#             # print("Actual:", real_class)

#             if predicted_class > real_class:
#                 overestimated_home_team += 1
#             elif predicted_class < real_class:
#                 underestimated_home_team += 1
#             elif predicted_class == real_class:
#                 correct += 1
#             total += 1

#     print("Total Test cases:", total)
#     accuracy = round(correct/total, 3)
#     print(playoff_year, "Accuracy: ", accuracy)
#     print("Overestimated home team", overestimated_home_team, "times")
#     print("Underestimated home team", underestimated_home_team, "times")
#     print()

#     playoff_year += 1
