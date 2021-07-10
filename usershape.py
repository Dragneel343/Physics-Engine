#Controls the user object
from globals import SCREEN_WIDTH
from circle import Circle
from shape import Shape
import cv2
import numpy
import pynput
from pynput import keyboard

class UserShape(Circle):
    def __init__(self, x=0, y=0, radius=5, color=(255,255,255)):
        super().__init__(x=x, y=y,radius = radius, color=color)
        self.acceleration.ddy == 0
        self.mass == 1000000

    def Movement(self,event):
        # print('Received event {}'.format(event.key))
        input = format(event.key, '')

        if input == "'a'":
            # print('a pressed')
            self.center.x -= 10

        if input == "'d'":
            # print('d pressed')
            self.center.x += 10

        if input == "'w'":
            # print('w pressed')
            self.center.y -= 10

        if input == "'s'":
            # print('s pressed')
            self.center.y += 10