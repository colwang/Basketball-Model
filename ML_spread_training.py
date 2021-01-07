import torch
import torch.optim as optim
from tqdm import tqdm
import tensorflow as tf
from ML_data_generation import *
from ML_net import *

data = data_gen(2017, 2020)
data.generate_spread_data_points()
shuffled_game_data = data.shuffle_data()

# data.balance_data(False)

train_X, train_y, test_X, test_y = data.create_tensors(shuffled_game_data, .2)

BATCH_SIZE = 50                     # number of games we run each time
EPOCHS = 20                          # how many times we run through the training data in general


# OPTIMIZATION STEP
optimizer = optim.Adam(spread_net.parameters(), lr=1e-5)
loss_function = nn.MSELoss()


for epoch in tqdm(range(EPOCHS)):
    for i in range(0, len(train_X), BATCH_SIZE):
    
        batch_X = train_X[i:i+BATCH_SIZE].view(-1, 8)
        batch_y = train_y[i:i+BATCH_SIZE]

        spread_net.zero_grad()
        
        outputs = spread_net(batch_X)
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
        net_out = spread_net(test_X[i].view(-1, 8))
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




# # BACKTESTING

# playoff_year = data.start_year
# for i in range(data.end_year - data.start_year + 1):
#     print("------------ TESTING AGAINST", playoff_year, "NBA SCHEDULE ------------")

#     backtesting_data = data_gen(playoff_year, playoff_year)

#     backtesting_data.generate_spread_data_points()
#     shuffled_backtesting_data = backtesting_data.shuffle_data()

#     empty_X, empty_y, backtesting_X, backtesting_y = data.create_tensors(shuffled_backtesting_data, 1)

#     overestimated_home_team = 0
#     underestimated_home_team = 0
#     correct = 0
#     total = 0
#     with torch.no_grad():
#         for i in range(len(backtesting_X)):
#             real_class = torch.argmax(backtesting_y[i])
#             net_out = spread_net(backtesting_X[i].view(-1, 8))
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
