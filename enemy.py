import pygame as pg
from pygame.math import Vector2
import math
import constants as c
from constants import enemyData

class Enemy(pg.sprite.Sprite):
    def __init__(self, enemyType, waypoints, images):
        pg.sprite.Sprite.__init__(self)
        self.waypoints = waypoints
        self.pos = Vector2(self.waypoints[0])
        self.targetWaypoint = 1
        self.health = enemyData.get(enemyType)['health']
        self.speed = enemyData.get(enemyType)['speed']
        self.angle = 0
        self.originalImage = images.get(enemyType)
        self.image = pg.transform.rotate(self.originalImage, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
    

    def update(self, world):
        self.move(world)
        self.rotate()
        self.checkAlive(world)
    

    def move(self, world):
        # define a target waypoint
        if self.targetWaypoint < len(self.waypoints):
            self.target = Vector2(self.waypoints[self.targetWaypoint])
            self.movement = self.target - self.pos
        else:
            # enemy has reached the end of the path
            self.kill()
            world.health -= 1
            world.missedEnemies += 1

        # calculate distance to target
        dist = self.movement.length()
        # check if remaining distance is greater than the enemy speed
        if dist >= (self.speed * world.gameSpeed):
            self.pos += self.movement.normalize() * (self.speed * world.gameSpeed)
        else:
            if dist != 0:
                self.pos += self.movement.normalize() * dist
            self.targetWaypoint += 1
        
    
    def rotate(self):
        #calculate distance to next waypoint
        dist = self.target - self.pos
        #use distance to calculate angle
        self.angle = math.degrees(math.atan2(-dist[1], dist[0]))
        #rotate image and update rectangle
        self.image = pg.transform.rotate(self.originalImage, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
    

    def checkAlive(self, world):
        if self.health <= 0:
            world.killedEnemies += 1
            world.money += c.killReward
            self.kill()