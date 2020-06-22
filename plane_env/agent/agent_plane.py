import gym
import plane_env
import time
import numpy as np
import pickle
from collections import defaultdict
#import matplotlib.pyplot as plt

env = gym.make("PlaneEnv-v3")

Q = defaultdict(lambda: [-1.5, -1, 0.5, 0, 0.5, 1, 1.5])
lr, factor = 0.7, 0.95
episodes = 30  # 训练100次
score_list = []  # 记录所有分数
epislon = 0.05
counter = 0
for i in range(episodes):
    # s = (200, 300, 0, 0)
    s = env.reset()
    reward = 0
    score = 0
    while True:
        env.render()
        a = np.argmax(Q[s])
        print(a)
        epsilon = 0.5 * (0.99 ** i)
        if epislon > np.random.uniform(0,1):
            print("random")
            a = np.random.choice([-1.5, -1, -0.5, 0, 0.5, 1, 1.5])

        # 执行动作
        next_s, reward, done, out, _ = env.step(a)
        reward = reward - 0.1

        if done:
            reward += 1000
            env.reset()
        # next_s = transform_state(next_s)
        # 根据上面的公式更新Q-Table
        Q[s][a] = (1 - lr) * Q[s][a] + lr * (reward + factor * max(Q[next_s]))
        score += reward
        s = next_s

        if out or done:
            break
env.close()

with open('plane-v3-q-learning.pickle', 'wb') as f:
    pickle.dump(dict(Q), f)
    print('model saved')
