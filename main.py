import pygame as pg
import json
from enemy import Enemy
from world import World
from turret import Turret
from button import Button
import constants as c

pg.init()

# Create clock
clock = pg.time.Clock()

# Create game window
screen = pg.display.set_mode((c.screenWidth + c.sidePanel, c.screenHeight))
pg.display.set_caption('Tower Defence')

# Game variables
gameOver = False
gameOutcome = 0# -1 is loss and 1 is win
levelStarted = False
lastEnemySpawn = pg.time.get_ticks()
placingTurrets = False
selectedTurret = None

# Load images
mapImage = pg.image.load('levels/level.png').convert_alpha()
turretSpritesheets = []
for x in range(1, c.turretLevels+1):
    turretSheet = pg.image.load(f'assets/images/turrets/turret_{x}.png').convert_alpha()
    turretSpritesheets.append(turretSheet)
enemyImages = {
    'weak': pg.image.load('assets/images/enemies/enemy_1.png').convert_alpha(),
    'medium': pg.image.load('assets/images/enemies/enemy_2.png').convert_alpha(),
    'strong': pg.image.load('assets/images/enemies/enemy_3.png').convert_alpha(),
    'elite': pg.image.load('assets/images/enemies/enemy_4.png').convert_alpha(),
}
# buttons
cursorTurret = pg.image.load('assets/images/turrets/cursor_turret.png').convert_alpha()
enemyImage = pg.image.load('assets/images/enemies/enemy_1.png').convert_alpha()
buyTurretImage = pg.image.load('assets/images/buttons/buy_turret.png').convert_alpha()
cancelImage = pg.image.load('assets/images/buttons/cancel.png').convert_alpha()
upgradeTurretImage = pg.image.load('assets/images/buttons/upgrade_turret.png').convert_alpha()
beginImage = pg.image.load('assets/images/buttons/begin.png').convert_alpha()
restartImage = pg.image.load('assets/images/buttons/restart.png').convert_alpha()
fastForwardImage = pg.image.load('assets/images/buttons/fast_forward.png').convert_alpha()
# gui
heartImage = pg.image.load('assets/images/gui/heart.png').convert_alpha()
coinImage = pg.image.load('assets/images/gui/coin.png').convert_alpha()
logoImage = pg.image.load('assets/images/gui/logo.png').convert_alpha()

# Load sounds
shotFx = pg.mixer.Sound('assets/audio/shot.wav')
shotFx.set_volume(0.5)

# Load json data for level
with open('levels/level.tmj') as file:
    worldData = json.load(file)

# Load fonts
textFont = pg.font.SysFont('Consolas', 24, bold = True)
largeFont = pg.font.SysFont('Consolas', 36)

def drawText(text, font, textCol, x, y):
    img = font.render(text, True, textCol)
    screen.blit(img, (x, y))

def displayData():
    # draw panel
    pg.draw.rect(screen, 'maroon', (c.screenWidth, 0, c.sidePanel, c.screenHeight))
    pg.draw.rect(screen, 'grey0', (c.screenWidth, 0, c.sidePanel, 400), 2)
    screen.blit(logoImage, (c.screenWidth, 400))
    # display data
    drawText('LEVEL: ' + str(world.level), textFont, 'grey100', c.screenWidth + 10, 10)
    screen.blit(heartImage, (c.screenWidth + 10, 35))
    drawText(str(world.health), textFont, 'grey100', c.screenWidth + 50, 40)
    screen.blit(coinImage, (c.screenWidth + 10, 65))
    drawText(str(world.money), textFont, 'grey100', c.screenWidth + 50, 70)

def createTurret(mousePos):
    mouseTileX = mousePos[0] // c.tileSize
    mouseTileY = mousePos[1] // c.tileSize
    # calculate the sequential number of the tile
    mouseTileNum = (mouseTileY * c.cols) + mouseTileX
    # check if tile is grass
    if world.tileMap[mouseTileNum] == 7:
        # check that there isn't already a turret there
        spaceIsFree = True
        for turret in turretGroup:
            if (mouseTileX, mouseTileY) == (turret.tileX, turret.tileY):
                spaceIsFree = False
        if spaceIsFree:
            newTurret = Turret(turretSpritesheets, mouseTileX, mouseTileY, shotFx)
            turretGroup.add(newTurret)
            world.money -= c.buyCost

def selectTurret(mousePos):
    mouseTileX = mousePos[0] // c.tileSize
    mouseTileY = mousePos[1] // c.tileSize
    for turret in turretGroup:
        if (mouseTileX, mouseTileY) == (turret.tileX, turret.tileY):
            return turret


def clearSection():
    for turret in turretGroup:
        turret.selected = False

# Create world
world = World(worldData, mapImage)
world.processData()
world.processEnemies()

# Create groups
enemyGroup = pg.sprite.Group()
turretGroup = pg.sprite.Group()

# Create buttons
turretButton = Button(c.screenWidth + 30, 120, buyTurretImage, True)
cancelButton = Button(c.screenWidth + 50, 180, cancelImage, True)
upgradeButton = Button(c.screenWidth + 5, 180, upgradeTurretImage, True)
beginButton = Button(c.screenWidth + 60, 300, beginImage, True)
restartButton = Button(310, 300, restartImage, True)
fastForwardButton = Button(c.screenWidth + 50, 300, fastForwardImage, False)


# Game loop
run = True
while run:

    clock.tick(c.fps)

    ##################
    # Updating section

    if gameOver == False:
        if world.health <= 0:
            gameOver = True
            gameOutcome = -1
        if world.level > c.totalLevels:
            gameOver = True
            gameOutcome = 1

        # update groups
        enemyGroup.update(world)
        turretGroup.update(enemyGroup, world)

        # highlight selected turret
        if selectedTurret:
            selectedTurret.selected = True

    #################
    # Drawing section

    # draw level
    world.draw(screen)

    # draw groups
    enemyGroup.draw(screen)
    for turret in turretGroup:
        turret.draw(screen)
    
    displayData()
    
    if gameOver == False:
        if levelStarted == False:
            if beginButton.draw(screen):
                levelStarted = True
        else:
            # fast forward option
            world.gameSpeed = 1
            if fastForwardButton.draw(screen):
                world.gameSpeed = 10
            # Spawn enemies
            if pg.time.get_ticks() - lastEnemySpawn > c.spawnCooldown:
                if world.spawnedEnemies < len(world.enemyList):
                    enemyType = world.enemyList[world.spawnedEnemies]
                    enemy = Enemy(enemyType, world.waypoints, enemyImages)
                    enemyGroup.add(enemy)
                    world.spawnedEnemies += 1
                    lastEnemySpawn = pg.time.get_ticks()
        
        # check if the wave is finished
        if world.checkLevelComplete() == True:
            world.money += c.levelCompleteReward
            world.level += 1
            levelStarted = False
            lastEnemySpawn = pg.time.get_ticks()
            world.resetLevel()
            world.processEnemies()

        # Draw buttons
        drawText(str(c.buyCost), textFont, 'grey100', c.screenWidth + 215, 135)
        screen.blit(coinImage, (c.screenWidth + 260, 130))
        if turretButton.draw(screen):
            placingTurrets = True
        # if placing turrets then show the cancel button as well
        if placingTurrets == True:
            # show cursor turret
            cursorRect = cursorTurret.get_rect()
            cursorPos = pg.mouse.get_pos()
            cursorRect.center = cursorPos
            if cursorPos[0] <= c.screenWidth:
                screen.blit(cursorTurret, cursorRect)
            if cancelButton.draw(screen):
                placingTurrets = False
        # if a turret is selected then show the upgrade button
        if selectedTurret:
            if selectedTurret.upgradeLevel < c.turretLevels:
                drawText(str(c.upgradeCost), textFont, 'grey100', c.screenWidth + 215, 195)
                screen.blit(coinImage, (c.screenWidth + 260, 190))
                if upgradeButton.draw(screen):
                    if world.money >= c.upgradeCost:
                        selectedTurret.upgrade()
                        world.money -= c.upgradeCost
    else:
        pg.draw.rect(screen, 'dodgerblue', (200, 200, 400, 200), border_radius = 30)
        if gameOutcome == -1:
            drawText('GAME OVER', largeFont, 'grey0', 310, 230)
        elif gameOutcome == 1:
            drawText('YOU WIN', largeFont, 'grey0', 315, 230)
        # restart level
        if restartButton.draw(screen):
            gameOver = False
            levelStarted = False
            placingTurrets = False
            selectedTurret = None
            lastEnemySpawn = pg.time.get_ticks()
            world = World(worldData, mapImage)
            world.processData()
            world.processEnemies()
            enemyGroup.empty()

    
    # event handler
    for event in pg.event.get():
        # quit program
        if event.type == pg.QUIT:
            run = False
        # mouse click
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            mousePos = pg.mouse.get_pos()
            # check if mouse is in the game area
            if mousePos[0] < c.screenWidth and mousePos[1] < c.screenHeight:
                # clear turrets
                selectedTurret = None
                clearSection()
                if placingTurrets == True:
                    # check balance
                    if world.money >= c.buyCost:
                        createTurret(mousePos)
                else:
                    selectedTurret = selectTurret(mousePos)

    # update display
    pg.display.flip()

pg.quit()

# write stuff here
# 2:27
