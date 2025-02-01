import pygame as pg
import random
import constants as c
from constants import enemySpawnData

class World():
    def __init__(self, data, mapImage):
        self.level = 1
        self.gameSpeed = 1
        self.health = c.health
        self.money = c.money
        self.waypoints = []
        self.levelData = data
        self.image = mapImage
        self.enemyList = []
        self.spawnedEnemies = 0
        self.killedEnemies = 0
        self.missedEnemies = 0


    def processData(self):
        # look through data to extract relevant data
        for layer in self.levelData['layers']:
            if layer['name'] == 'tilemap':
                self.tileMap = layer['data']
            elif layer['name'] == 'waypoints':
                for obj in layer['objects']:
                    waypointData = obj['polyline']
                    self.processWaypoints(waypointData)


    def processWaypoints(self, data):
        # iterate through waypoints to extract co-ords
        for point in data:
            tempX = point.get('x')
            tempY = point.get('y')
            self.waypoints.append((tempX, tempY))
    

    def processEnemies(self):
        enemies = enemySpawnData[self.level - 1]
        for enemyType in enemies:
            enemiesToSpawn = enemies[enemyType]
            for enemy in range(enemiesToSpawn):
                self.enemyList.append(enemyType)
        random.shuffle(self.enemyList)


    def checkLevelComplete(self):
        if self.killedEnemies + self.missedEnemies == len(self.enemyList):
            return True
    
    
    def resetLevel(self):
        self.spawnedEnemies = 0
        self.killedEnemies = 0
        self.missedEnemies = 0
        

    def draw(self, surface):
        surface.blit(self.image, (0, 0))