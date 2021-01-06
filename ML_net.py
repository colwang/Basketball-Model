import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

class Net(nn.Module):

	def __init__(self):
		super().__init__()
		self.fc1 = nn.Linear(1*8, 64)
		self.fc2 = nn.Linear(64, 64)
		self.fc3 = nn.Linear(64, 64)
		self.fc4 = nn.Linear(64, 64)
		self.fc5 = nn.Linear(64, 64)
		self.fc6 = nn.Linear(64, 64)
		self.fc7 = nn.Linear(64, 64)

		self.fc8 = nn.Linear(64, 2)			# for h2h predictions
		# self.fc8 = nn.Linear(64, 12)		# for spread predictions

	def forward(self, x):
		x = F.relu(self.fc1(x))
		x = F.relu(self.fc2(x))
		x = F.relu(self.fc3(x))
		x = F.relu(self.fc4(x))
		x = F.relu(self.fc5(x))
		x = F.relu(self.fc6(x))
		x = F.relu(self.fc7(x))
		x = self.fc8(x)
		return F.log_softmax(x, dim=1)

net = Net()
# print(net)


