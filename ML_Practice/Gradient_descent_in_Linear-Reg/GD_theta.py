import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_regression

# Generate synthetic regression data
X, y = make_regression(n_samples=1000, n_features=1, noise=10, random_state=10)
y = y.reshape(-1, 1)
m = X.shape[0]
X_b = np.c_[np.ones((m, 1)), X]

# Define different learning rates
learning_rates = [0.001, 0.01, 0.1,0.98, 1.0]
n_iterations = 100
initial_theta = np.array([[2.0], [3.0]])

# Plot setup
plt.figure(figsize=(12, 6))
plt.scatter(X, y, color="blue", alpha=0.5, label="Actual Data")

# Run gradient descent for each learning rate
for rate in learning_rates:
    theta = initial_theta.copy()

    for _ in range(n_iterations):
        y_pred = X_b.dot(theta)
        gradients = (2 / m) * X_b.T.dot(y_pred - y)
        theta -= rate * gradients
        #theta -= rate * X_b.T.dot(y_pred - y)/m #makes your gradient too small, and training will be slower.

    plt.plot(X, X_b.dot(theta), label=f"LR={rate}")

# Final touches on plot
plt.xlabel("Feature")
plt.ylabel("Target")
plt.title("Effect of Learning Rate on Gradient Descent")
plt.legend()
plt.grid(True)
plt.show()
