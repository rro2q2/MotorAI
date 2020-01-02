import pygame
import math
import numpy as np
import nms

class Car:
    def __init__(self, screen, x, y, speed=0):
        pygame.sprite.Sprite.__init__(self)
        self.timer = 0
        self.screen = screen
        self.pos = [x, y]
        self.width = 25
        self.length = 50
        self.speed = speed
        self.vel = [0, 0]
        self.angle = 0
        self.steering_angle = 0
        # load original image
        self.originalImage = pygame.image.load("../assets/red_car.png").convert_alpha()
        # resize original image
        self.originalImage = pygame.transform.scale(self.originalImage, (self.length, self.width))
        # The variable that is changed whenever the car is rotated.
        self.image = self.originalImage.copy()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        # Maximum steering angle
        self.maxSteer = math.pi / 2  # constant max steering angle
        self.acceleration_rate = 5
        self.speed_dampening = 0.1
        #self.maxSpeed = 300  # 60 Mph
        self.delta = 1 / 60
        # self.steering_elasticity = 5
        self.steering_elasticity = 5 / 60

        self.gear = "STOP"
        self.constant_speed = False

        self.init_state = (self.pos[0], self.pos[1], self.angle,
                             self.steering_angle, self.vel[0], self.vel[1], self.speed)
        self.sliding_history = np.zeros((1, 10))


    def update(self, delta, action, stop):
        self.timer += delta
        self.delta = delta
        self.angle += self.steering_angle * delta * self.speed / 100

        self.vel[0] = int(math.cos(self.angle) * self.speed)
        self.vel[1] = int(math.sin(self.angle) * self.speed)

        self.pos[0] += int(self.vel[0] * delta)
        self.pos[1] += int(self.vel[1] * delta)

        #self.steering_angle = dampenSteering(self.steering_angle, self.steering_elasticity)

        oldCenter = self.rect.center
        car_img = self.originalImage.copy()

        if self.speed == 0:  # if the car slows down
            if action == 'UP':
                self.angle = -(math.pi / 2) # Rotate 90 degrees in radians
            elif action == 'DOWN':
                self.angle = (math.pi / 2)
            elif action == 'LEFT':
                self.angle = math.pi
            elif action == 'RIGHT':
                self.angle = 0
            if stop == 'S':
                # Perform nms
                rects = nms.locateBoundingBoxes(nms.gray)
                nms_rects = nms.nms(rects, 0.2)
                nms.displayImage(rects, nms_rects)

            self.image = pygame.transform.rotate(car_img, (-self.angle * 360 / (2 * math.pi)))
        self.speed = 300

        self.image = pygame.transform.rotate(car_img, (-self.angle * 360 / (2 * math.pi)))
        self.rect = self.image.get_rect()
        self.rect.center = oldCenter
        w, h = self.image.get_size()
        self.screen.blit(self.image, (self.pos[0] - w / 2, self.pos[1] - h / 2))

        return self.pos


def dampenSteering(angle, elasticity):
    if angle == 0:
        return 0
    elif angle > 0:
        # new_angle = angle - elasticity*delta
        new_angle = angle - elasticity
        if new_angle <= 0:
            new_angle = 0
        return new_angle
    elif angle < 0:
        # new_angle = angle + elasticity*delta
        new_angle = angle + elasticity
        if new_angle >= 0:
            new_angle = 0
        return new_angle
