import logging

import numpy as np

import random

import gym
from gym import spaces
from gym.utils import seeding

import math
import time

logger = logging.getLogger(__name__)


class PlaneWorldEnv(gym.Env):


    metadata = {
        'render.modes': ['human', 'rgb_array'],
        'video.frames_per_second': 10
    }


    def __init__(self):
        self.viewer = None
        # self.init_states = [1,2,3,4]
        # self.init_x = [450,350,350,450]
        # self.init_y = [350,350,250,250]
        # self.state = [400,300,0,0,0]
        self.timestep = 0.1
        # self.action = []
        self.acc_mag = 1
        # 重力加速度
        self.g = 10
        self.action_space = spaces.Discrete(4)

        # self.observation_space = spaces.Box(-high, high, dtype=np.float32)
        self.pitch = 0
        self.seed()

    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def step(self, action):
        # assert self.action_space.contains(action), "%r (%s) invalid" % (action, type(action))
        # # time.sleep(1)
        # # print(action)
        # pos_x, pos_y, vel_x, vel_y = self.state
        #
        # if action == 1:
        #     acc_x = 0
        #     acc_y = self.acc_mag
        # elif action == 0:
        #     acc_x = 0
        #     acc_y = -self.acc_mag
        # elif action == 2:
        #     acc_y = 0
        #     acc_x = self.acc_mag
        # elif action == 3:
        #     acc_y = 0
        #     acc_x = -self.acc_mag
        pos_x, pos_y, vel_x, vel_y = self.state
        acc_y, pitch = action
        self.pitch = pitch



        # acc_x = -((math.atan2(pos_y - 200, pos_x) - (math.atan2(100, 300))) * 10.0)

        #print("acc_x: %f\t acc_y: %f\n" % (acc_x, acc_y))


        vel_x += self.g * pitch * self.timestep
        vel_y += acc_y * self.timestep
        vel = math.sqrt(math.pow(vel_x, 2) + math.pow(vel_y, 2))
        pos_x = (pos_x /100 + vel_x * self.timestep + 0.5 * self.g * pitch * self.timestep) *100
        pos_y = (pos_y /100 + vel_y * self.timestep + 0.5 * acc_y * self.timestep) *100
        print("vel_x: %f\t vel_y: %f\n" % (vel_x, vel_y))
        print("pos_x: %f\t pos_y: %f\n" % (pos_x / 100, pos_y / 100))
        #conditions where the game is ended
        #pos_x=290-310 pos_y=290-310 vel=(-2, 2)

        #out->out of the frame
        #success
        #done->end of a episode
        out = pos_x < 270 \
              or pos_x > 330 \
              or pos_y > 130 \
              or pos_y < 70
        out = bool(out)

        success = pos_x > 290 \
                  and pos_x < 310 \
                  and pos_y > 90 \
                  and pos_y < 110 \
                  and vel < 5 \
                  and vel > -5


        done = bool(out) \
               or bool(success)
        done = bool(done)
        # the art of the whole games: reward
        if out:
            reward = - 100.0
        elif success:
            reward = + 100.0
        else:
            reward = - 1.0


        # distance = math.sqrt(math.pow(pos_x-300,2) + math.pow(pos_y-300,2))
        # if distance < 100:
        #     reward = 0.1 * (100 - distance)
        # elif distance > 100:
        #     reward = -0.1 * distance
        # else:
        #     reward = 0
        self.state = (pos_x, pos_y, vel_x, vel_y)
        # print(self.state)
        return np.array(self.state), reward, done, {}

    def reset(self):
        # self.state = (280, 300, 0, 0)
        #initial pos_x, pos_y=(280,300)  vel_x, vel_y=0
        self.state = np.array([self.np_random.uniform(low=290, high=310), self.np_random.uniform(low=90, high=110), \
                               0, 0])
        return np.array(self.state)

    def reset_x(self):
        # self.state = (280, 300, 0, 0)
        #initial pos_x, pos_y=(280,300)  vel_x, vel_y=0
        self.state = np.array([self.np_random.uniform(low=270, high=280), self.np_random.uniform(low=95, high=105), \
                               0, 0])
        return np.array(self.state)

    def reset_z(self):
        # self.state = (280, 300, 0, 0)
        #initial pos_x, pos_y=(280,300)  vel_x, vel_y=0
        self.state = np.array([self.np_random.uniform(low=299.9, high=300.1), self.np_random.uniform(low=105, high=125), \
                               0, 0])
        return np.array(self.state)

    def render(self, mode='human', close=False):

        screen_width = 700
        screen_height = 400
        planewidth = 30
        planeheight = 8
        laserwidth = 360
        laserheight = 2
        if self.viewer is None:
            from gym.envs.classic_control import rendering

            self.viewer = rendering.Viewer(screen_width,screen_height)
            # create a plane block
            l,r,t,b = -planewidth/2, planewidth/2, -planeheight/2, planeheight/2
            # create a laser block
            l_laser, r_laser, t_laser, b_laser = -laserwidth, 0, laserheight/2, -laserheight/2

            target_plane = rendering.FilledPolygon([(l,b), (l,t), (r,t), (r,b)])
            target_plane.add_attr(rendering.Transform(translation=(300,100)))


            plane = rendering.FilledPolygon([(l,b), (l,t), (r,t), (r,b)])
            laser = rendering.FilledPolygon([(l_laser,b_laser), (l_laser,t_laser), (r_laser,t_laser),(r_laser,b_laser)])

            self.planetrans = rendering.Transform()
            self.lasertrans = rendering.Transform()
            plane.add_attr(self.planetrans)
            laser.add_attr(self.lasertrans)

            self.viewer.add_geom(target_plane)
            self.viewer.add_geom(plane)
            self.viewer.add_geom(laser)

            target_plane.set_color(0, 1, 0)
            plane.set_color(0, 0, 1)
            laser.set_color(1, 0, 0)
            # create a receiver
            self.receiver = rendering.Line((10,150),(10,50))
            self.receiver.set_color(0,0,0)
            self.viewer.add_geom(self.receiver)

        if self.state is None: return None

        pos_x = self.state[0]
        pos_y = self.state[1]
        pitch = self.pitch
        # pitch = float('%.3f' % ((math.atan2(pos_y -200, pos_x))-(math.atan2(100, 300))))
        self.planetrans.set_translation(pos_x, pos_y)
        self.planetrans.set_rotation(pitch)
        pitch_angle = float('%.3f' % (pitch * 180 /3.1415))
        print("pitch angle: %f" % pitch_angle)

        self.lasertrans.set_translation(pos_x, pos_y)
        self.lasertrans.set_rotation(pitch)

        return self.viewer.render(return_rgb_array=mode == 'rgb_array')

    def close(self):
        if self.viewer:
           self.viewer.close()
           self.viewer = None

