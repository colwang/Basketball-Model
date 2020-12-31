import torch
import torch.optim as optim
from tqdm import tqdm
from ML_data_generation import *
from ML_net import *

data = data_gen(2020, 2020)
data.generate_data_points()
shuffled_game_data_2020 = data.shuffle_data()

# np.save("data_points.npy", shuffled_game_data_2020)
# training_data = np.load("data_points.npy", allow_pickle=True)
# print(len(training_data))

train_X, train_y, test_X, test_y = data.create_tensors(shuffled_game_data_2020, .2)

BATCH_SIZE = 50                     # number of games we run each time
EPOCHS = 20                          # how many times we run through the training data in general


# OPTIMIZATION STEP
optimizer = optim.Adam(net.parameters(), lr=8e-5)
loss_function = nn.MSELoss()


for epoch in range(EPOCHS):
    for i in range(0, len(train_X), BATCH_SIZE):
    
        batch_X = train_X[i:i+BATCH_SIZE].view(-1, 8)
        batch_y = train_y[i:i+BATCH_SIZE]

        net.zero_grad()
        
        outputs = net(batch_X)
        loss = loss_function(outputs, batch_y)
        loss.backward()
        optimizer.step()

    # print(f"Epoch: {epoch + 1}. Loss: {loss}")


correct = 0
total = 0
with torch.no_grad():
    for i in range(len(test_X)):
        real_class = torch.argmax(test_y[i])
        net_out = net(test_X[i].view(-1, 8))
        predicted_class = torch.argmax(net_out)

        if predicted_class == real_class:
            correct += 1
        total += 1

accuracy = round(correct/total, 3)
print("Accuracy: ", accuracy)
