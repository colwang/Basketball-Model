import torch
import torch.optim as optim
from tqdm import tqdm
from ML_data_generation import *
from ML_conv_net import *

data = data_gen(2020, 2020)
data.generate_data_points()
shuffled_game_data_2020 = data.shuffle_data()

# np.save("data_points.npy", shuffled_game_data_2020)
# training_data = np.load("data_points.npy", allow_pickle=True)
# print(len(training_data))

train_X, train_y, test_X, test_y = data.create_tensors(shuffled_game_data_2020, .2)

BATCH_SIZE = 50                     # number of games we run each time
EPOCHS = 5                          # how many times we run through the training data in general

learning_rate_accuracy = dict()
learning_rates = [8e-6, 9e-6, 1e-5, 2e-5, 3e-5,
                  4e-5, 5e-5, 6e-5, 7e-5, 8e-5,
                  9e-5, 1e-4, 2e-4, 3e-4, 4e-4,
                  5e-4, 6e-4, 7e-4, 8e-4, 9e-4, 
                  1e-3, 2e-3, 3e-3]

for k in tqdm(range(len(learning_rates))):

    # OPTIMIZATION STEP
    optimizer = optim.Adam(net.parameters(), lr=learning_rates[k])
    loss_function = nn.MSELoss()

    accuracies = []

    for i in range(10):

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
        # print("Accuracy: ", accuracy)

        accuracies.append(accuracy)

    learning_rate_accuracy[learning_rates[k]] = (sum(accuracies) / len(accuracies))

learning_rate_rankings = dict(sorted(learning_rate_accuracy.items(), key=lambda item: item[1]))

print(learning_rate_rankings)