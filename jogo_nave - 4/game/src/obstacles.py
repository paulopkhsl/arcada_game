import pygame
import random

class Meteor(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        # Definir as propriedades do meteoro (posição, imagem, etc.)
        self.image = pygame.transform.scale(pygame.image.load('game/assests/imagens/meteor.png'), (50, 50))  # Amarelo para projéteis
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = random.randint(2, 6)  # Velocidade de queda

    def update(self, dt):
        """Atualiza a posição do meteoro (queda)"""
        self.rect.y += self.speed

        # Remove o meteoro quando ele sai da tela
        if self.rect.y > 600:  # Considerando que a altura da tela é 600px
            self.kill()
