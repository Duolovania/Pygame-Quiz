import pygame
from abc import ABC, abstractclassmethod

# Class handles the storage of x and y coordinated.
class Vector2:
    def __init__(self, x: float = 0, y: float = 0):
        self.x: float = x
        self.y: float = y 

# Class handles the storage of positional, rotational and local scale values.
class Transform:
    def __init__(self, position: Vector2 = Vector2(), rotation: Vector2 = Vector2(), localScale: Vector2 = Vector2(1, 1)):
        self.position = position
        self.rotation = rotation

        # If localScale argument is 50. localScale will equal to (50, 50)
        if type(localScale) == float or type(localScale) == int:
            self.localScale = Vector2(localScale, localScale)
        else:
            self.localScale = localScale

# Class stores the application's size and label.
class Application:
    def __init__(self, iconPath: str, w: int, h: int, flags: int, title: str, showCursor: bool = True):
        pygame.mixer.pre_init(44100, 16, 2, 4096)
        pygame.init()

        self.w: int = w
        self.h: int = h
        self.flags: int = flags
        self.title: str = title
        self.iconSurface = pygame.image.load("Assets/Images/" + iconPath) 
        self.display: pygame.Surface = pygame.display.set_mode((w, h), flags)

        pygame.display.set_icon(self.iconSurface)
        pygame.mouse.set_visible(showCursor)
        pygame.display.set_caption(title)
    
    # Refreshes the window. Use this to change screen dimensions or fullscreen.
    def Refresh(self):
        self.display = pygame.display.set_mode((self.w, self.h), self.flags)

# Blueprint abstract class for visual objects (objects on screen).
class GameObject(ABC):
    # Abstract method. Must be implemented in child.
    @abstractclassmethod
    def ResetRect(self):
        pass

    # Outputs the object onto the screen.
    def Draw(self, screen: pygame.Surface):
        self.ResetRect()
        screen.blit(self.surface, self.rect)

# Class handles all image properties. Inherits GameObject Draw().
class Texture(GameObject):
    def __init__(self, path: str, scale: Vector2 = 1):
        self.path: str = "Assets/Images/" + path
        self.transform: Transform = Transform(localScale = scale)

        self.ResetRect()
    
    # Resets the rect. This updates any values in __init__() before image is drawn on screen.
    def ResetRect(self):
        if ".png" in self.path:
            self.surface = pygame.transform.scale(pygame.image.load(self.path).convert_alpha(), (pygame.image.load(self.path).convert_alpha().get_width() * self.transform.localScale.x, pygame.image.load(self.path).convert_alpha().get_height() * self.transform.localScale.y))
        else:
            self.surface = pygame.transform.scale(pygame.image.load(self.path).convert(), (pygame.image.load(self.path).convert().get_width() * self.transform.localScale.x, pygame.image.load(self.path).convert().get_height() * self.transform.localScale.y))

        self.rect = self.surface.get_rect()
        self.rect.x = self.transform.position.x
        self.rect.y = self.transform.position.y

# Class handles all text properties. Inherits GameObject Draw().
class Text(GameObject):
    black: tuple = (0, 0, 0)
    white: tuple = (255, 255, 255)

    def __init__(self, textValue: any, path: str, scale: float = 1, antiAlias: bool = False, fillColor: tuple = black, borderColor: tuple = None):
        self.fontPath: str = path
        self.antiAlias: bool = antiAlias

        self.fillColor: tuple = fillColor
        self.borderColor: tuple = borderColor

        self.transform: Transform = Transform(localScale = scale)
        self.text: any = textValue

        self.ResetRect()

    # Resets the rect. This updates any values in __init__() before text is drawn on screen.
    def ResetRect(self):
        self.fontObj: pygame.font = pygame.font.Font("Assets/Fonts/" + self.fontPath, 64)
        width = self.fontObj.render(str(self.text), self.antiAlias, self.fillColor, self.borderColor).get_width()
        height = self.fontObj.render(str(self.text), self.antiAlias, self.fillColor, self.borderColor).get_height()

        self.surface = pygame.transform.scale(self.fontObj.render(str(self.text), self.antiAlias, self.fillColor, self.borderColor), (width * self.transform.localScale.x, height * self.transform.localScale.y))
        
        self.rect = self.surface.get_rect()
        self.rect.x = self.transform.position.x
        self.rect.y = self.transform.position.y
             

# Class handles all sound properties.
class SFX:
    def __init__(self, path: str):
        self.path: str = "Assets/SFX/" + path
        self.sound: pygame.mixer.Sound = pygame.mixer.Sound(self.path)
    
    # Plays background music (plays music forever by default)
    def LoadMusic(self, loopCount: int = -1):
        pygame.mixer.music.load(self.path)
        pygame.mixer.music.play(loopCount)

    # Plays sound effect through default channel
    def Play(self, loopCount: int = 0, volume: float = 1):
        self.sound.set_volume(volume)
        pygame.mixer.Sound.play(self.sound, loopCount)
    
    # Plays sound effect through specific channel
    def PlayThroughChannel(self, channel, loopCount: int = 0, volume: float = 1):
        self.sound.set_volume(volume)
        channel.play(self.sound, loopCount)
    
    # Sets the music volume.
    def SetMusicVolume(self, volume: float):
        pygame.mixer.music.set_volume(volume)