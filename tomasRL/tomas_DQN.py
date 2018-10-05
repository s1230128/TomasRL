import sys
import numpy as np
import time
import chainer
import chainer.functions as F
import chainer.links as L
import chainerrl
import pygame as pg
from pygame.locals import *
import tomasEnv



# Q-関数の定義
class QFunction(chainer.Chain):
    def __init__(self, n_obs, n_act, n_node=10):
        super(QFunction, self).__init__()
        with self.init_scope():
            self.l0=L.Linear(n_obs , n_node)
            self.l1=L.Linear(n_node, n_node)
            self.l2=L.Linear(n_node, n_act )

    def __call__(self, x, test=False):
        h = F.tanh(self.l0(x))
        h = F.tanh(self.l1(h))
        return chainerrl.action_value.DiscreteActionValue(self.l2(h))


# 学習の設定
alpha = 0.5
gamma = 0.99
max_step  = 500
n_episode = 300

env = tomasEnv.TomasEnv()

qFunc = QFunction(6, 6)
optimizer = chainer.optimizers.Adam(eps=1e-2)
optimizer.setup(qFunc)
explorer = chainerrl.explorers.LinearDecayEpsilonGreedy(start_epsilon=1.0,\
                                                        end_epsilon=0.2,\
                                                        decay_steps=n_episode,\
                                                        random_action_func=env.random_act)
replayBuffer = chainerrl.replay_buffer.ReplayBuffer(capacity=10 ** 6)
#phi = lambda x: x.astype(np.float32, copy=False)
agent = chainerrl.agents.DQN(qFunc, optimizer, replayBuffer, gamma, explorer,\
                             replay_start_size=500, update_interval=1, target_update_interval=100)


# 学習
if sys.argv[1] == '-train':
    for eps in range(n_episode):
        obs = env.reset()
        reward = 0
        sum_reward = 0
        done = False

        for t in range(max_step):
            #if eps % 100 == 0: env.render()
            act = agent.act_and_train(obs, reward)
            obs, reward, done, info = env.step(act)
            sum_reward += reward
            if done: break

        agent.stop_episode_and_train(obs, reward, done)
        if eps % 10 == 0: print('episode: {:>3}  R: {:>1}'.format(eps, sum_reward))

    agent.save('tomas_agent')


# テスト
if sys.argv[1] == '-test':
    agent.load('tomas_agent')

    clock = pg.time.Clock()
    framerate = 60

    for _ in range(5):
        obs = env.reset()
        done = False

        while not done:
            # フレームレート
            clock.tick(framerate)

            # 終了判定
            for e in pg.event.get():
                if e.type == QUIT: sys.exit()

            act = agent.act(obs)

            obs, reward, done, info = env.step(act)
            env.render()
