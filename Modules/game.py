from Modules.application import *
from Modules.gameobject import *
from Modules.sound import *
from enum import Enum
import math

userName: any = input("Please enter your username: ")
mahogany: tuple = (196, 73, 0)
richBlack: tuple = (4, 21, 31)
celeste: tuple = (185, 250, 248)
wisteria: tuple = (178, 152, 220)
amethyst: tuple = (166, 99, 204)

score: int = 0 # Game score.
questionNum: int = 0
optionSize: float = 0.5

window: Application = Application("warning.png", 800, 600, 0, "12DDT", False) # Creates new window.
gameRunning: bool = True # Status of game loop.
mouseChannel: pygame.mixer.Channel = pygame.mixer.Channel(0) # New audio channel for mouse SFX.

mouseCursor: Texture = Texture("mouse cursor.png", scale = 1.2)
background: Texture = Texture("Backgrounds/MainMenu.png", scale = 3)
background.transform.position = Vector2(-10, 0)

music: SFX = SFX("Kubbi - Up In My Jam  NO COPYRIGHT 8-bit Music.mp3") # Background music.

music.set_music_volume(0.25)
music.load_music()

bitFont: str = "nokia_cellphone/nokiafc22.ttf"
scoreText: Text = Text(score, bitFont, scale = 1, fillColor = celeste)
scoreText.transform.position = Vector2(20, 20)

fpsText: Text = Text(score, bitFont, scale = 0.4, fillColor = wisteria)
fpsText.transform.position = Vector2(680, 20)

endText:Text = Text("ggs, " + userName, bitFont, scale = 1, fillColor = celeste)
endText.transform.position = Vector2(20, 20)

refreshAll: bool = False
clock = pygame.time.Clock()

creator: Texture = Texture("DLogo.png", 0.15)
creator.transform.position = Vector2(10, 10)

title: Texture = Texture("ehs.png", 0.1)
title.transform.position = Vector2(220, 150)

playGame: Text = Text("Play Game", bitFont)
playGame.transform.position = Vector2(40, 490)

player:Texture = Texture("char.png", 1)
player.transform.position = Vector2(0, 0)

inputVector:Vector2 = Vector2()

class GameState(Enum):
    MainMenu = 0
    GameScreen = 1
    EndScreen = 2

gameState: GameState = GameState(GameState.MainMenu)

# Class handles game events.
class Game:
    # Function controls game loop and closes window after game loop is terminated.
    def run():
        while gameRunning:
            Game.forever()
        pygame.quit()
        quit()

    # Game loop.
    def forever():
        window.display.fill((0, 0, 0))
        pygame.time.delay(10)

        fpsText.text = "FPS: " + str(int(clock.get_fps()))
        clock.tick(60)
        background.path = "Assets/Images/Backgrounds/" + str(gameState.name) + ".png"
        background.reset_rect()
        background.draw(window.display)
        
        if gameState == GameState.GameScreen:
            scoreText.text = score

            player.draw(window.display)
            player.transform.position += inputVector * 1

            if refreshAll:
                Game.refresh_all()

            scoreText.draw(window.display)
        elif gameState == GameState.MainMenu:
            playGame.transform.position = Vector2(math.cos((pygame.time.get_ticks() / 3 % 1000) / 100) * 10 + 50, playGame.transform.position.y)

            title.draw(window.display)
            playGame.draw(window.display)
            creator.draw(window.display)
        else:
            playGame.transform.position = Vector2(math.cos((pygame.time.get_ticks() / 3 % 1000) / 100) * 10 + 50, playGame.transform.position.y)

            playGame.draw(window.display)
            endText.draw(window.display)
            
        mousepos = pygame.mouse.get_pos()
        mouseCursor.transform.position = Vector2(mousepos[0], mousepos[1])

        fpsText.reset_rect()
        fpsText.draw(window.display)
        mouseCursor.draw(window.display)
        
        Game.handle_events()
        pygame.display.update()

    # Refreshes all GameObjects.
    def refresh_all():
        scoreText.reset_rect()

        global refreshAll
        refreshAll = False
    
    # Handles user's keyboard and mouse events.
    def handle_events():
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    global gameRunning
                    gameRunning = False
                case pygame.KEYDOWN:
                    Game.key_events(event)
                case pygame.MOUSEBUTTONDOWN:
                    mousepos = pygame.mouse.get_pos()
                    if playGame.rect.collidepoint(mousepos):
                        global gameState
                        global score
                        global questionNum

                        gameState = GameState.GameScreen
                        score = 0 
                        questionNum = 0
                        pygame.time.wait(50)

    # Defines what each key press does.
    def key_events(gameEvent: pygame.event):
        match gameEvent.key:
            case pygame.K_UP:
                inputVector.y = -1
            case pygame.K_DOWN:
                inputVector.y = 1
            case pygame.K_RIGHT:
                inputVector.x = 1
            case pygame.K_LEFT:
                inputVector.x = -1
            case pygame.K_ESCAPE:
                if window.flags != 0:
                    window.flags = 0
                    window.refresh()
                else:
                    global gameRunning
                    gameRunning = False
            case pygame.K_f:
                window.flags = pygame.FULLSCREEN
                window.refresh()