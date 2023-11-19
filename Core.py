width = 1920
height = 1080
shootingDelta = 10


import pygame
import pygame_gui
import sys
import json
from random import randint
from Player import *
from Asteroid import *
from pygame import mixer
from pygame_gui.elements import UILabel, UIButton, UITextEntryBox, UITextBox

pygame.init()
mixer.init()
explode = mixer.Sound("hit.mp3")
lvlup = mixer.Sound("levelup.mp3")

screen = pygame.display.set_mode((width, height))
surface = pygame.display.get_surface()
pygame.display.set_caption("Asteroids")
clock = pygame.time.Clock()
manager = pygame_gui.UIManager((width, height))

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
            out += S["name"] + ": " + str(S["score"]) + "<br>"
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

score = 0
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
#speedLabel.hide()

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

playerName = UITextEntryBox(
        relative_rect=pygame.Rect((width/2)-150, (height/2)+200, 200, 50),
        manager = manager
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
level = 0


accelRate = 20
player = Player((width/2,height/2), surface)


def spawnAsteroids(qty):
    for n in range(qty):
        x = randint(0,width)
        y = randint(0,height)
        while abs(x-player.getPosX()) < 50 or abs(y-player.getPosY()) < 50:
            x = randint(0,width)
            y = randint(0,height)
        asteroids.append(Asteroid(30, (x,y), (0.4*randint(-40,40), 0.4*randint(-40,40)), surface))

while True:
    
    time_delta = clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == startButton:
                startButton.hide()
                titleLabel.hide()
                started = True
                spawnAsteroids(level)
            elif event.ui_element == saveBtn:
                toAddName = playerName.get_text()
                playerName.set_text("")
                
                if not toAddName == "":
                    record(toAddName, score)
                    level = 1
                    score = 0
                    asteroids = []
                    bullets = []
                    started = True
                    spawnAsteroids(level)
                    leaderboard.hide()
                    gameOverLabel.hide()
                    saveBtn.hide()
                    playerName.hide()
                    player = Player((width/2,height/2), surface)
  
        elif event.type == pygame.KEYDOWN and started:
            if event.key == pygame.K_LEFT:
                player.rotateCW()
            elif event.key == pygame.K_RIGHT:
                player.rotateCCW()
            elif event.key == pygame.K_UP:
                player.accelFW()
            elif event.key == pygame.K_DOWN:
                player.accelBW()
            elif event.key == pygame.K_SPACE:
                if currentFrame - lastShot > shootingDelta:
                    bullets.append(player.shoot())
                    lastShot = currentFrame
                    score -= 1
            elif event.key == pygame.K_END:
                sys.exit()    
        
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player.stopRotate()
            elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                player.stopAccel()

      
        manager.process_events(event)
        
    if score < 0:
        score = 0        
    if started:
        scoreLabel.set_text("Score:" + str(score))
        levelLabel.set_text("Niveau " + str(level))
        if len(asteroids) < 1:
            level+=1
            spawnAsteroids(level)
            lvlup.play()
    
    manager.update(time_delta/1000)

    pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(0, 0, width, height))

    manager.draw_ui(screen)
    
    if started:
        player.draw(screen)
        speedLabel.set_text(str(player.getSpeed()))
        for A in asteroids:
            A.draw(screen)
            if player.getPosX() - A.getPosX() < A.getRadius() and player.getPosX() - A.getPosX() > -A.getRadius():
                if player.getPosY() - A.getPosY() < A.getRadius() and player.getPosY() - A.getPosY() > -A.getRadius():
                    started = False
                    leaderboard.set_text(getScores())
                    gameOverLabel.show()
                    leaderboard.show()
                    playerName.show()
                    saveBtn.show()
            
            for B in bullets:
                    if B.getPosX() - A.getPosX() < A.getRadius() and B.getPosX() - A.getPosX() > -A.getRadius():
                        if B.getPosY() - A.getPosY() < A.getRadius() and B.getPosY() - A.getPosY() > -A.getRadius():
                            asteroids.pop(asteroids.index(A))
                            bullets.pop(bullets.index(B))
                            explode.play()
                            score += 50
                            if A.getRadius() > 10:
                                asteroids.append(Asteroid(A.getRadius()-10, (A.getPosX()+10, A.getPosY()+10), (0.4*randint(-40,40), 0.4*randint(-40,40)), surface))
                                asteroids.append(Asteroid(A.getRadius()-10, (A.getPosX()-10, A.getPosY()-10), (0.4*randint(-40,40), 0.4*randint(-40,40)), surface))
                
    
        for B in bullets:
            if not B.draw(screen):
                bullets.pop(bullets.index(B))
        
    
    pygame.display.flip()
    currentFrame += 1