import pygame as pg
import math
import constants as c
from constants import turretData

class Turret(pg.sprite.Sprite):
    def __init__(self, spriteSheets, tileX, tileY, shotFx):
        pg.sprite.Sprite.__init__(self)
        self.upgradeLevel = 1
        self.range = turretData[self.upgradeLevel-1].get('range')
        self.cooldown = turretData[self.upgradeLevel-1].get('cooldown')
        self.lastShot = pg.time.get_ticks()
        self.selected = False
        self.target = None

        # position vars
        self.tileX = tileX
        self.tileY = tileY
        # calculate center co-ords
        self.x = (self.tileX + 0.5) * c.tileSize
        self.y = (self.tileY + 0.5) * c.tileSize
        # shot sound effect
        self.shotFx = shotFx

        # animation variables
        self.spriteSheets = spriteSheets
        self.animationList = self.loadImages(self.spriteSheets[self.upgradeLevel - 1])
        self.frameIndex = 0
        self.updateTime = pg.time.get_ticks()

        # update image
        self.angle = 90
        self.originalImage = self.animationList[self.frameIndex]
        self.image = pg.transform.rotate(self.originalImage, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

        # create transparent circle showing range
        self.rangeImage = pg.Surface((self.range * 2, self.range * 2))
        self.rangeImage.fill((0, 0, 0))
        self.rangeImage.set_colorkey((0, 0, 0))
        pg.draw.circle(self.rangeImage, 'grey100', (self.range, self.range), self.range)
        self.rangeImage.set_alpha(100)
        self.rangeRect = self.rangeImage.get_rect()
        self.rangeRect.center = self.rect.center

    def loadImages(self, spriteSheet):
        size = spriteSheet.get_height()
        animationList = []
        for x in range(c.animationSteps):
            tempImg = spriteSheet.subsurface(x * size, 0, size, size)
            animationList.append(tempImg)
        return animationList
    

    def update(self, enemyGroup, world):
        if self.target:
            self.playAnimation()
        else:
            # search for new turret once turret has cooled down
            if pg.time.get_ticks() - self.lastShot > (self.cooldown / world.gameSpeed):
                self.pickTarget(enemyGroup)
    

    def pickTarget(self, enemyGroup):
        # find an enemy to target
        xDist = 0
        yDist = 0
        for enemy in enemyGroup:
            if enemy.health > 0:
                xDist = enemy.pos[0] - self.x
                yDist = enemy.pos[1] - self.y
                dist = math.sqrt(xDist ** 2 + yDist ** 2)
                if dist < self.range:
                    self.target = enemy
                    self.angle = math.degrees(math.atan2(-yDist, xDist))
                    self.target.health -= c.damage
                    self.shotFx.play()
                    break


    def playAnimation(self):
        # update image
        self.originalImage = self.animationList[self.frameIndex]
        # check if enough time has passed since the last update
        if pg.time.get_ticks() - self.updateTime > c.animationDelay:
            self.updateTime = pg.time.get_ticks()
            self.frameIndex += 1
            # check if the animation has finished
            if self.frameIndex >= len(self.animationList):
                self.frameIndex = 0
                # record completed time and clear target
                self.lastShot = pg.time.get_ticks()
                self.target = None
    

    def upgrade(self):
        self.upgradeLevel += 1
        self.range = turretData[self.upgradeLevel-1].get('range')
        self.cooldown = turretData[self.upgradeLevel-1].get('cooldown')
        # upgrade turret image
        self.animationList = self.loadImages(self.spriteSheets[self.upgradeLevel - 1])
        self.originalImage = self.animationList[self.frameIndex]

        # upgrade range circle
        self.rangeImage = pg.Surface((self.range * 2, self.range * 2))
        self.rangeImage.fill((0, 0, 0))
        self.rangeImage.set_colorkey((0, 0, 0))
        pg.draw.circle(self.rangeImage, 'grey100', (self.range, self.range), self.range)
        self.rangeImage.set_alpha(100)
        self.rangeRect = self.rangeImage.get_rect()
        self.rangeRect.center = self.rect.center


    def draw(self, surface):
        self.image = pg.transform.rotate(self.originalImage, self.angle - 90)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        surface.blit(self.image, self.rect)
        if self.selected:
            surface.blit(self.rangeImage, self.rangeRect)