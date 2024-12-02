import pygame
import random
from config import WIDTH, HEIGHT

import pygame
import random
from config import WIDTH, HEIGHT

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, x, y, type_):
        super().__init__()
        self.type = type_  # Tipo: "shield" ou "extra_life"
        
        # Se for power-up de vida extra, carrega a imagem de coração
        if self.type == "shield":
            self.image = pygame.image.load("game/assests/imagens/shield.png") 
            self.image = pygame.transform.scale(self.image, (50, 50)) # Azul para escudo
        elif self.type == "extra_life":
            # Carregar a imagem de coração
            self.image = pygame.image.load("game/assests/imagens/heart.png")  # Caminho para a imagem de coração
            self.image = pygame.transform.scale(self.image, (30, 30))  # Redimensiona a imagem para o tamanho adequado

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 150  # Velocidade de descida

    def update(self, dt):
        """Atualiza posição do power-up."""
        self.rect.y += self.speed * dt
        if self.rect.top > HEIGHT:  # Remove se sair da tela
            self.kill()
