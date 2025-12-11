import pygame

class SpriteSheet():
    def __init__(self, image):
        self.sheet = image

    def get_image(self, frame, width, height, scale, colour):
        image = pygame.Surface((width, height)).convert_alpha()
        image.blit(self.sheet, (0, 0), ((frame * width), 0, width, height))
        image = pygame.transform.scale(image, (width * scale, height * scale))
        image.set_colorkey(colour)
        return image
    
class Platform():
    def __init__(self, x, y, sizeX, sizeY, ImagePath):
        self.rect = pygame.Rect((x, y, sizeX, sizeY))
        self.image = pygame.image.load(ImagePath)

    def Draw(self, surface, image):
        pygame.draw.rect(surface, (255, 0, 0), self.rect)
        pygame.image.load(self.image)
    