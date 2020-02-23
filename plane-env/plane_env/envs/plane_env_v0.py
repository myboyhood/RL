import logging
import numpy as np
import random
from gym import spaces
import gym
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
        self.init_states = [1,2,3,4]
        self.init_x = [450,350,350,450]
        self.init_y = [350,350,250,250]
        self.state = [400,300,0,0,0]
        self.timestep = 0.3
        # self.action = []

    def step(self,action):
        # assert self.action_space.contains(action), "%r (%s) invalid" % (action, type(action))
        # time.sleep(1)
        pos_x, pos_y, vel_x, vel_y = self.state
        acc_y = action
        acc_x = - float('%.1f' % ((math.atan2(pos_y -200, pos_x)-(math.atan2(100, 300)))*10.0))
        vel_x += acc_x * self.timestep
        vel_y += acc_y * self.timestep
        pos_x += vel_x * self.timestep + 0.5*acc_x * self.timestep
        pos_y += vel_y * self.timestep + 0.5*acc_y * self.timestep

        print("vel_x: %f\t vel_y: %f\n" % (vel_x, vel_y))
        done = bool(pos_x > 290 and pos_x == 310 and pos_y > 290 and pos_y <310)
        out = bool(pos_x < 0 or pos_x > 500 or pos_y > 600 or pos_y < 50)
        # reward = -1.0
        distance = math.sqrt(math.pow(pos_x-300,2) + math.pow(pos_y-300,2))
        if distance < 100:
            reward = 0.1*(100 - distance)
        elif distance > 100:
            reward = -0.1 * distance
        else:
            reward = 0
        self.state = (pos_x, pos_y, vel_x, vel_y)
        return self.state, reward, done, out, {}

    def reset(self):
        self.state = (280,300,0,0)
        return self.state


    def render(self, mode='human', close=False):

        screen_width = 700
        screen_height = 500
        planewidth = 40
        planeheight = 10

        if self.viewer is None:
            from gym.envs.classic_control import rendering

            self.viewer = rendering.Viewer(screen_width,screen_height)
            # create a plane block
            l,r,t,b = -planewidth/2, planewidth/2, planeheight, 0
            plane = rendering.FilledPolygon([(l,b), (l,t), (r,t), (r,b)])
            target_plane = rendering.FilledPolygon([(l,b), (l,t), (r,t), (r,b)])
            target_plane.add_attr(rendering.Transform(translation=(300,300)))
            target_plane.set_color(1, 0.5, 0)
            self.planetrans = rendering.Transform()

            plane.add_attr(self.planetrans)
            self.viewer.add_geom(plane)
            self.viewer.add_geom(target_plane)

            # self.plane.set_color(1,0,0)
            # create a receiver
            self.receiver = rendering.Line((10,200),(10,100))
            self.receiver.set_color(1.0,0,0)
            self.viewer.add_geom(self.receiver)

        if self.state is None: return None

        pos_x = self.state[0]
        pos_y = self.state[1]
        pitch = float('%.3f' % ((math.atan2(pos_y -200, pos_x))-(math.atan2(100, 300))))
        self.planetrans.set_translation(pos_x,pos_y)
        self.planetrans.set_rotation(pitch)
        pitch_angle = float('%.1f' % (pitch * 180 /3.1415))
        print("pitch angle: %f" % pitch_angle)

        return self.viewer.render(return_rgb_array=mode == 'rgb_array')

    def close(self):
        if self.viewer:
            self.viewer.close()
            self.viewer = None

