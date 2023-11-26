width = 800
height = 600
shootingDelta = 10
allowBrake = True
minimumAsteroids = 3

bulletCost = 1
asteroidsReward = 50


import pygame
import requests
import os
import pygame_gui
import sys
import json
from random import randint
baseResourcesURL = "https://hctel.net/dev/share/perso/IN2L/dl/"
#def checkFile(path):
#   if not os.path.isfile(path):
#      response = requests.get(baseResourcesURL + path) 
#     open(path, 'wb').write(response.content)
        
#def checkDir(path):
#   if not os.path.isdir(path):
#      os.mkdir(path)
from Player import *
from Asteroid import *
from pygame import mixer
from pygame_gui.elements import UILabel, UIButton, UITextEntryLine, UITextBox


pygame.init()
mixer.init()
explode = mixer.Sound("res/bangMedium.wav")
lvlup = mixer.Sound("res/levelup.mp3")



screen = pygame.display.set_mode((width, height))
surface = pygame.display.get_surface()
pygame.display.set_caption("Asteroids")
pygame.display.set_icon(pygame.image.load("res/icon.png"))
clock = pygame.time.Clock()
manager = pygame_gui.UIManager((width, height), "conf/theme.json")


def getString(filepath):
    try:
        with open(filepath) as file:
            return file.read()
    except FileNotFoundError:
        print("Fichier non trouve!")
        return 404
    except IOError:
        print("Erreur d'entree-sortie")
        return 400

def getJson(string):
    if string:
        return json.loads(string)
    
def getScores():
    txt = getString("scores.json")
    if type(txt) == int:
        if txt == 404:
            return("Pas encore de scores...")
        elif txt == 400:
            return("Erreur de fichier!")
    else:
        jsont = getJson(txt)
        scores = sorted(jsont, key=lambda x: x["score"], reverse=True)
        out = ""
        for S in scores:
            out +=  S["name"] + ":" + str(S["score"]) + "<br>"
    return out
        
def record(name, score):
    try:
        with open("scores.json", 'r') as fichier_scores:
            scores = json.load(fichier_scores)
    except FileNotFoundError:
        scores = []

    scores.append({"name": name, "score": score})


    with open('scores.json', 'w') as fichier_scores:
        json.dump(scores, fichier_scores, indent=2)


scoreLabel = UILabel(
        relative_rect=pygame.Rect(0, 0, 100, 50),
        text='',
        manager = manager,
    )

levelLabel = UILabel(
        relative_rect=pygame.Rect(100, 0, 100, 50),
        text = '',
        manager = manager
    )

speedLabel = UILabel(
        relative_rect = pygame.Rect(700, 0, 100, 50),
        text = '',
        manager = manager
    )
speedLabel.hide()

titleLabel = UILabel(
        relative_rect=pygame.Rect((width/2)-50, (height/2)-25-(height/10), 100, 50),
        text='Asteroids',
        manager = manager,
    )

startButton = UIButton(
        relative_rect=pygame.Rect((width/2)-50, (height/2)-25+(height/10), 100,50),
        text='Start',
        manager = manager
    )
pauseLabel = UILabel(
        relative_rect=pygame.Rect((width/2)-50, (height/2)-25, 100,50),
        text="Paused",
        manager = manager
    )
pauseLabel.hide()

gameOverLabel = UILabel(
        relative_rect=pygame.Rect((width/2)-50, 0, 100, 50),
        text='Game Over!',
        manager = manager,
    )
gameOverLabel.hide()

leaderboard = UITextBox(
        relative_rect=pygame.Rect((width/2)-150, (height/2)-200, 300, 400),
        html_text="",
        manager = manager
    )
leaderboard.hide()

playerName = UITextEntryLine(
        relative_rect=pygame.Rect((width/2)-150, (height/2)+200, 200, 50),
        manager = manager,
        placeholder_text = "Enter your name"
    )
playerName.hide()

saveBtn = UIButton(
        relative_rect=pygame.Rect((width/2)+50, (height/2)+200, 100, 50),
        text="Save",
        manager = manager
    )
saveBtn.hide()



bullets = []
asteroids = []


lastShot = 0
currentFrame = 0

started = False
paused = False
score = 0
level = 0

player = Player((width/2,height/2), surface)


def spawnAsteroids(qty):
    for n in range(qty):
        x = randint(0,width)
        y = randint(0,height)
        while abs(x-player.getPosX()) < 70 or abs(y-player.getPosY()) < 70:
            x = randint(0,width)
            y = randint(0,height)
        asteroids.append(Asteroid(40, (x,y), (0.4*randint(-40,40), 0.4*randint(-40,40)), surface))

        

def start():
    global level
    global score
    global asteroids
    global bullets
    global started
    global player
    global asteroids
    level = 1
    score = 0
    asteroids = []
    bullets = []
    spawnAsteroids(level+minimumAsteroids-1)
    leaderboard.hide()
    gameOverLabel.hide()
    saveBtn.hide()
    playerName.hide()
    startButton.hide()
    titleLabel.hide()
    player = Player((width/2,height/2), surface)
    started = True
    
def displayMenu():
    leaderboard.hide()
    gameOverLabel.hide()
    saveBtn.hide()
    playerName.hide()
    startButton.show()
    titleLabel.show()

while True:
    
    time_delta = clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == startButton:
                start()
            elif event.ui_element == saveBtn:
                toAddName = playerName.get_text()
                playerName.set_text("")
                
                if not toAddName == "":
                    record(toAddName, score)
                    displayMenu()
                else:
                    displayMenu()
  
        elif event.type == pygame.KEYDOWN:
            if started and not paused:
                if event.key == pygame.K_LEFT or event.key == pygame.K_q:
                    player.rotateCW()
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    player.rotateCCW()
                elif event.key == pygame.K_UP  or event.key == pygame.K_z:
                    player.accelFW()
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    player.accelBW()
                elif event.key == pygame.K_SPACE and currentFrame - lastShot > shootingDelta and not paused:
                    bullets.append(player.shoot())
                    lastShot = currentFrame
                    score -= bulletCost
            if event.key == pygame.K_ESCAPE:
                paused = not paused
            if event.key == pygame.K_RETURN and saveBtn._get_visible():
                toAddName = playerName.get_text()
                playerName.set_text("")
                
                if not toAddName == "":
                    record(toAddName, score)
                    displayMenu()
                else:
                    displayMenu()
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_q or event.key == pygame.K_d:
                player.stopRotate()
            elif event.key == pygame.K_UP or event.key == pygame.K_DOWN or event.key == pygame.K_z or event.key == pygame.K_s:
                player.stopAccel()

      
        manager.process_events(event)
        
    if score < 0:
        score = 0        
    if started:
        scoreLabel.set_text("Score:" + str(score))
        levelLabel.set_text("Niveau " + str(level))
        if len(asteroids) < 1:
            level+=1
            spawnAsteroids(level+minimumAsteroids-1)
            lvlup.play()
    
    manager.update(time_delta/1000)

    pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(0, 0, width, height))

    manager.draw_ui(screen)
    
    if started:
        player.draw(screen)
        speedLabel.set_text(str(player.getSpeed()))
        if paused:
            player.freeze()
            pauseLabel.show()
        else:
            player.unFreeze()
            pauseLabel.hide()
        for A in asteroids:
            A.draw(screen)
            if paused:
                A.freeze()
            else:
                A.unFreeze()
            if player.getPosX() - A.getPosX() < A.getRadius() and player.getPosX() - A.getPosX() > -A.getRadius():
                if player.getPosY() - A.getPosY() < A.getRadius() and player.getPosY() - A.getPosY() > -A.getRadius():
                    started = False
                    leaderboard.set_text(getScores())
                    gameOverLabel.show()
                    leaderboard.show()
                    playerName.show()
                    saveBtn.show()
            
            for B in bullets:
                    if B.getPosX() - A.getPosX() < A.getRadius()+5 and B.getPosX() - A.getPosX() > -A.getRadius()-5:
                        if B.getPosY() - A.getPosY() < A.getRadius() and B.getPosY() - A.getPosY() > -A.getRadius():
                            asteroids.pop(asteroids.index(A))
                            bullets.pop(bullets.index(B))
                            explode.play()
                            score += asteroidsReward
                            if A.getRadius() > 20:
                                asteroids.append(Asteroid(A.getRadius()-10, (A.getPosX()+10, A.getPosY()+10), (0.4*randint(-40,40), 0.4*randint(-40,40)), surface))
                                asteroids.append(Asteroid(A.getRadius()-10, (A.getPosX()-10, A.getPosY()-10), (0.4*randint(-40,40), 0.4*randint(-40,40)), surface))
                
    
        for B in bullets:
            if not B.draw(screen):
                bullets.pop(bullets.index(B))
            if paused:
                B.freeze()
            else:
                B.unFreeze()
        
    pygame.display.flip()
    currentFrame += 1