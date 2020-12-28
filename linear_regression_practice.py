import numpy as np
from sklearn.linear_model import LinearRegression

x = np.array([5, 15, 25, 35, 45, 55]).reshape(-1,1)
y = np.array([5, 20, 14,32, 22, 38])

# model = LinearRegression(fit_intercept=False).fit(x, y)
model = LinearRegression().fit(x, y)

r_sq = model.score(x,y)
intercept = model.intercept_
slope = model.coef_

print('y = {} * x + {}'.format(slope, intercept))
