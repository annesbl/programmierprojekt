import numpy as np
import random
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam

# Define the MNK game environment
class MNKGame:
    def __init__(self, M, N, K):
        self.board = np.zeros((M, N))  # 0 represents an empty cell
        self.M = M
        self.N = N
        self.K = K

    def reset(self):
        self.board = np.zeros((self.M, self.N))

    def is_winner(self, player):
        # Implement the logic to check if 'player' has won
        # You need to check rows, columns, and diagonals
        pass

    def is_full(self):
        return np.all(self.board != 0)

    def get_state(self):
        # Return a flattened representation of the game board
        return self.board.flatten()

# Define the Q-learning agent
class QLearningAgent:
    def __init__(self, state_size, action_size, learning_rate=0.001, discount_factor=0.9, exploration_prob=1.0, exploration_decay=0.995, exploration_min=0.1):
        self.state_size = state_size
        self.action_size = action_size
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_prob = exploration_prob
        self.exploration_decay = exploration_decay
        self.exploration_min = exploration_min

        # Initialize the Q-table (you can use a neural network for more complex problems)
        self.q_table = Sequential()
        self.q_table.add(Dense(24, input_dim=state_size, activation='relu'))
        self.q_table.add(Dense(24, activation='relu'))
        self.q_table.add(Dense(action_size, activation='linear'))
        self.q_table.compile(loss='mse', optimizer=Adam(lr=learning_rate))

    def choose_action(self, state):
        if np.random.rand() <= self.exploration_prob:
            return random.randrange(self.action_size)  # Exploration
        else:
            q_values = self.q_table.predict(np.array([state]))[0]
            return np.argmax(q_values)  # Exploitation

    def train(self, state, action, reward, next_state, done):
        target = reward if done else reward + self.discount_factor * np.max(self.q_table.predict(np.array([next_state]))[0])
        target_f = self.q_table.predict(np.array([state]))
        target_f[0][action] = target
        self.q_table.fit(np.array([state]), target_f, epochs=1, verbose=0)

        # Decay exploration rate
        if self.exploration_prob > self.exploration_min:
            self.exploration_prob *= self.exploration_decay

# Training the Q-learning agent
M = 3
N = 3
K = 3
state_size = M * N
action_size = M * N

env = MNKGame(M, N, K)
agent = QLearningAgent(state_size, action_size)

episodes = 1000

for episode in range(episodes):
    state = env.get_state()
    total_reward = 0

    while True:
        action = agent.choose_action(state)
        next_state = env.get_state()  # Assuming a synchronous environment
        reward = 1 if env.is_winner(1) else 0  # Reward 1 for winning
        done = env.is_winner(1) or env.is_full()

        agent.train(state, action, reward, next_state, done)

        total_reward += reward
        state = next_state

        if done:
            break

    print(f"Episode: {episode + 1}, Total Reward: {total_reward}")

# Evaluate the trained agent
# You can use the trained agent to make moves in the MNK game
