width = 1920
height = 1080

shootingDelta = 10
bulletLifetime = 100
allowBrake = True
invincible = False

asteroidSpeedRatio = 1
asteroid_split = 2
minimumAsteroids = 3 
asteroidInitialSize = 40
lastSize = 20
sizeReduction = 10
lowlag = True
sides = 37

bulletCost = 1
asteroidsReward = 50
bulletEasyFactor = 5 #Augmentation de la zone de détection de collision des bullets pour rendre le jeu plus facile

minStarQty = 22
maxStarQty = 55
minStarRadius = 1
maxStarRadius = 3

import pygame
import pygame_gui
import sys
import json
from random import randint
from Player import *
from Asteroid import *
from pygame import mixer
from pygame_gui.elements import UILabel, UIButton, UITextEntryLine, UITextBox
from pygame_gui.core import ObjectID


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


def getString(filepath): #Permet re recuperer le texte dans le fichier de scores
    try:
        with open(filepath) as file:
            return file.read()
    except FileNotFoundError:
        print("Didn't find the scores file yet. Creating it...")
        return 404
    except IOError:
        print("I/O Error while reading the score file!")
        return 400

def getJson(string): #Convertit le String du fichier texte en objet JSON
    if string:
        return json.loads(string)
    
def getScores(): #Récupère tous les scores du JSON et renvoie l'ensemble des scores en String avec un <br> à la fin pour faire un retour à la ligne vu que les TextBoxes de pygameGUI prennent de l'HTML. (<br> fait un retour à la ligne)
    txt = getString("scores.json")
    if type(txt) == int:
        if txt == 404:
            return("No scores yet...")
        elif txt == 400:
            return("File error!")
    else:
        jsont = getJson(txt)
        scores = sorted(jsont, key=lambda x: x["score"], reverse=True)
        out = ""
        for S in scores:
            out +=  S["name"] + " : " + str(S["score"]) + "<br>"
    return out
        
def record(name, score): #Enregistre le score du joueur dans le JSON et enregistre le fichier
    try:
        with open("scores.json", 'r') as file:
            scores = json.load(file)
    except FileNotFoundError:
        scores = []

    scores.append({"name": name, "score": score})


    with open('scores.json', 'w') as file:
        json.dump(scores, file, indent=2)

stars = []

def spawnStars():
    qty = randint(minStarQty,maxStarQty)
    for i in range(qty):
        pos = (randint(0,width), randint(0,height))
        size = randint(minStarRadius,maxStarRadius)
        speed = (0,0)
        stars.append(Asteroid(size,pos,speed,surface).setStar())


#Toutes les definitions des UIElements
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

speedLabel = UILabel( #Label de debug, on peut mettre un peu la variable qu'on veut pour la vérifier en jeu
        relative_rect = pygame.Rect(700, 0, 100, 50),
        text = '',
        manager = manager
    )
speedLabel.hide() #On met cette ligne en commentaire pour l'activer

buttonQuit = UIButton(
        relative_rect=pygame.Rect(width-100, 0, 100, 50),
        text='Quit',
        manager = manager
    )

titleLabel = UILabel(
        relative_rect=pygame.Rect((width/2)-125, (height/2)-25-(height/10), 252, 50),
        text='Asteroids',
        manager = manager,
        object_id = ObjectID(class_id = "@titles", object_id="#main_title")
    )

startButton = UIButton(
        relative_rect=pygame.Rect((width/2)-50, (height/2)-25+(height/10), 100,50),
        text='Start',
        manager = manager
    )
howToPlay = UIButton(
        relative_rect=pygame.Rect((width/2)-50, (height/2)-25+(height/10)+50, 100,50),
        text='How to play',
        manager = manager,
        object_id = ObjectID(class_id = "@buttons", object_id = "#howtoplay_button")
    )

goToMenu = UIButton(
        relative_rect=pygame.Rect(0,0,100,50),
        text='Menu',
        manager = manager
    )
goToMenu.hide()


#Tous les UIElements pour le menu "HowToPlay"
#J'aurais pu faire bcp plus simple en itérant une liste de touches par exemple
zKey = UIButton(
        relative_rect=pygame.Rect((width/3)-25, (height/2)-100, 100,50),
        text='Z',
        manager = manager,
        object_id = ObjectID(class_id = "@howtoplay_buttons", object_id = "#howtoplay_z")
    )
zKey.hide()
qKey = UIButton(
        relative_rect=pygame.Rect((width/3)-25, (height/2)-50, 100,50),
        text='Q',
        manager = manager,
        object_id = ObjectID(class_id = "@howtoplay_buttons", object_id = "#howtoplay_q")
    )
qKey.hide()
sKey = UIButton(
        relative_rect=pygame.Rect((width/3)-25, (height/2), 100,50),
        text='S',
        manager = manager,
        object_id = ObjectID(class_id = "@howtoplay_buttons", object_id = "#howtoplay_s")
    )
sKey.hide()
dKey = UIButton(
        relative_rect=pygame.Rect((width/3)-25, (height/2)+50, 100,50),
        text='D',
        manager = manager,
        object_id = ObjectID(class_id = "@howtoplay_buttons", object_id = "#howtoplay_d")
    )
dKey.hide()
spKey = UIButton(
        relative_rect=pygame.Rect((width/3)-25, (height/2)+100, 100,50),
        text='SPACE',
        manager = manager,
        object_id = ObjectID(class_id = "@howtoplay_buttons", object_id = "#howtoplay_sp")
    )
spKey.hide()
zTxt = UILabel(
        relative_rect=pygame.Rect((2*width/3), (height/2)-100, 100,50),
        text='Forward',
        manager = manager,
        object_id = ObjectID(class_id = "@howtoplay_buttons", object_id = "#howtoplay_z")
    )
zTxt.hide()
qTxt = UILabel(
        relative_rect=pygame.Rect((2*width/3), (height/2)-50, 100,50),
        text='Backwards',
        manager = manager,
        object_id = ObjectID(class_id = "@howtoplay_buttons", object_id = "#howtoplay_q")
    )
qTxt.hide()
sTxt = UILabel(
        relative_rect=pygame.Rect((2*width/3), (height/2), 210,50),
        text='Rotate counter-clockwise',
        manager = manager,
        object_id = ObjectID(class_id = "@howtoplay_buttons", object_id = "#howtoplay_s")
    )
sTxt.hide()
dTxt = UILabel(
        relative_rect=pygame.Rect((2*width/3), (height/2)+50, 138,50),
        text='Rotate clockwise',
        manager = manager,
        object_id = ObjectID(class_id = "@howtoplay_buttons", object_id = "#howtoplay_d")
    )
dTxt.hide()
spTxt = UILabel(
        relative_rect=pygame.Rect((2*width/3), (height/2)+100, 100,50),
        text='Shoot',
        manager = manager,
        object_id = ObjectID(class_id = "@howtoplay_buttons", object_id = "#howtoplay_sp")
    )
spTxt.hide()



pauseLabel = UILabel(
        relative_rect=pygame.Rect((width/2)-90, (height/2)-34, 180,68),
        text="Paused",
        manager = manager,
        object_id = ObjectID(class_id = "@gameHUD", object_id = "#pause_label")
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
spawnStars()

def spawnAsteroids(qty):
    for n in range(qty):
        x = randint(0,width)
        y = randint(0,height)
        while abs(x-player.getPosX()) < 70 or abs(y-player.getPosY()) < 70:
            x = randint(0,width)
            y = randint(0,height)
        asteroids.append(Asteroid(asteroidInitialSize, (x,y), (asteroidSpeedRatio*randint(-40,40), asteroidSpeedRatio*randint(-40,40)), surface))
    if not lowlag:
        for A in asteroids:
            A.setPolygon(sides)
       

def start(): #Cache tout et initialise le joueur
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
    howToPlay.hide()
    started = True
    
def displayMenu():
    scoreLabel.hide()
    levelLabel.hide()
    leaderboard.hide()
    gameOverLabel.hide()
    saveBtn.hide()
    playerName.hide()
    startButton.show()
    titleLabel.show()
    howToPlay.show()
    
def displayHowToPlay():
    startButton.hide()
    titleLabel.hide()
    howToPlay.hide()
    goToMenu.show()
    zKey.show()
    zTxt.show()
    qKey.show()
    qTxt.show()
    sKey.show()
    sTxt.show()
    dKey.show()
    dTxt.show()
    spKey.show()
    spTxt.show()

def hideHowToPlay():
    zKey.hide()
    zTxt.hide()
    qKey.hide()
    qTxt.hide()
    sKey.hide()
    sTxt.hide()
    dKey.hide()
    dTxt.hide()
    spKey.hide()
    spTxt.hide()
    goToMenu.hide()
    startButton.show()
    titleLabel.show()
    howToPlay.show()

while True: #Boucle qui fait tout (le while true est interrompu avec le sys.exit())
    
    time_delta = clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == startButton:
                start()
            elif event.ui_element == howToPlay:
                displayHowToPlay()
            elif event.ui_element == goToMenu:
                hideHowToPlay()
            elif event.ui_element == buttonQuit:
                sys.exit()
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
                    bullets.append(player.shoot(bulletLifetime))
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
            if event.key == pygame.K_F9:
                sys.exit()
            if qKey.visible:
                if event.key == pygame.K_q:
                    qKey._set_active()
                elif event.key == pygame.K_d:
                    dKey._set_active()
                elif event.key == pygame.K_s:
                    sKey._set_active()
                elif event.key == pygame.K_z:
                    zKey._set_active()
                elif event.key == pygame.K_SPACE:
                    spKey._set_active()
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_q or event.key == pygame.K_d:
                player.stopRotate()
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN or event.key == pygame.K_z or event.key == pygame.K_s:
                player.stopAccel()
            if qKey.visible:
                if event.key == pygame.K_q:
                    qKey._set_inactive()
                elif event.key == pygame.K_d:
                    dKey._set_inactive()
                elif event.key == pygame.K_s:
                    sKey._set_inactive()
                elif event.key == pygame.K_z:
                    zKey._set_inactive()
                elif event.key == pygame.K_SPACE:
                    spKey._set_inactive()

      
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
    for S in stars:
        S.draw(screen)
        
    if started:
        player.draw(screen)
        speedLabel.set_text(str(player.getSpeed()))
        if paused:
            player.freeze()
            pauseLabel.show()
        else:
            player.unFreeze()
            pauseLabel.hide()
            
        toPop = []
        for A in asteroids:
            A.draw(screen)
            if paused:
                A.freeze()
            else:
                A.unFreeze()
            if player.getPosX() - A.getPosX() < A.getRadius() and player.getPosX() - A.getPosX() > -A.getRadius() and not invincible:
                if player.getPosY() - A.getPosY() < A.getRadius() and player.getPosY() - A.getPosY() > -A.getRadius():
                    started = False
                    leaderboard.set_text(getScores())
                    gameOverLabel.show()
                    leaderboard.show()
                    playerName.show()
                    saveBtn.show()
            
            for B in bullets:
                    if B.getPosX() - A.getPosX() < A.getRadius()+bulletEasyFactor and B.getPosX() - A.getPosX() > -A.getRadius()-bulletEasyFactor:
                        if B.getPosY() - A.getPosY() < A.getRadius()+bulletEasyFactor and B.getPosY() - A.getPosY() > -A.getRadius()-bulletEasyFactor:
                            toPop.append(A)
                            bullets.pop(bullets.index(B))
                            explode.play()
                            score += asteroidsReward
                            if A.getRadius() > lastSize:
                                if lowlag:
                                    for i in range(asteroid_split):
                                        asteroids.append(Asteroid(A.getRadius()-sizeReduction, (A.getPosX()+10, A.getPosY()+10), (asteroidSpeedRatio*randint(-40,40), asteroidSpeedRatio*randint(-40,40)), surface))
                                else:
                                    for i in range(asteroid_split):
                                        asteroids.append(Asteroid(A.getRadius()-sizeReduction, (A.getPosX()+10, A.getPosY()+10), (asteroidSpeedRatio*randint(-40,40), asteroidSpeedRatio*randint(-40,40)), surface).setPolygon(sides))
        for Aa in toPop:
            asteroids.pop(asteroids.index(Aa))
                                   
        for B in bullets:
            if not B.draw(screen):
                bullets.pop(bullets.index(B))
            if paused:
                B.freeze()
            else:
                B.unFreeze()
    pygame.display.flip()
    currentFrame += 1