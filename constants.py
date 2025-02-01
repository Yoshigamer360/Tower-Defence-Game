rows = 15
cols = 15
tileSize = 48
sidePanel = 300
screenWidth = tileSize * cols
screenHeight = tileSize * rows
fps = 60
health = 50
money = 650
totalLevels = 15

# Turret constants
turretLevels = 4
buyCost = 200
upgradeCost = 100
killReward = 10
levelCompleteReward = 100
animationSteps = 8
animationDelay = 15
damage = 5

turretData = [
    {
        #1
        'range': 90,
        'cooldown': 1500,
    },
    {
        #2
        'range': 110,
        'cooldown': 1200,
    },
    {
        #3
        'range': 125,
        'cooldown': 1000,
    },
    {
        #4
        'range': 150,
        'cooldown': 900,
    }
]

# Enemy constants
spawnCooldown = 400

enemySpawnData = [
  {
    #1
    "weak": 15,
    "medium": 0,
    "strong": 0,
    "elite": 0
  },
  {
    #2
    "weak": 3,#0,
    "medium": 0,
    "strong": 0,
    "elite": 0
  },
  {
    #3
    "weak": 20,
    "medium": 5,
    "strong": 0,
    "elite": 0
  },
  {
    #4
    "weak": 30,
    "medium": 15,
    "strong": 0,
    "elite": 0
  },
  {
    #5
    "weak": 5,
    "medium": 20,
    "strong": 0,
    "elite": 0
  },
  {
    #6
    "weak": 15,
    "medium": 15,
    "strong": 4,
    "elite": 0
  },
  {
    #7
    "weak": 20,
    "medium": 25,
    "strong": 5,
    "elite": 0
  },
  {
    #8
    "weak": 10,
    "medium": 20,
    "strong": 15,
    "elite": 0
  },
  {
    #9
    "weak": 15,
    "medium": 10,
    "strong": 5,
    "elite": 0
  },
  {
    #10
    "weak": 0,
    "medium": 100,
    "strong": 0,
    "elite": 0
  },
  {
    #11
    "weak": 5,
    "medium": 10,
    "strong": 12,
    "elite": 2
  },
  {
    #12
    "weak": 0,
    "medium": 15,
    "strong": 10,
    "elite": 5
  },
  {
    #13
    "weak": 20,
    "medium": 0,
    "strong": 25,
    "elite": 10
  },
  {
    #14
    "weak": 15,
    "medium": 15,
    "strong": 15,
    "elite": 15
  },
  {
    #15
    "weak": 25,
    "medium": 25,
    "strong": 25,
    "elite": 25
  }
]

enemyData = {
    "weak": {
    "health": 10,
    "speed": 2
  },
    "medium": {
    "health": 15,
    "speed": 3
  },
    "strong": {
    "health": 20,
    "speed": 4
  },
    "elite": {
    "health": 30,
    "speed": 6
  }
}
