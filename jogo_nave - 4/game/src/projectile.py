import pygame
import math

import pygame
import math

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, direction="up"):
        super().__init__()

        # Carregar a imagem padrão para projéteis que vão para cima
        self.image_up = pygame.transform.scale(pygame.image.load('game/assests/imagens/projectile_up.png'), (20, 20))  # Imagem para projéteis para cima
        # Carregar a imagem para projéteis que vão para baixo
        self.image_down = pygame.transform.scale(pygame.image.load('game/assests/imagens/projectile_down.png'), (20, 20))  # Imagem para projéteis para baixo
        
        # Se a direção for "down", usa a imagem específica para projéteis que vão para baixo
        if direction == "down":
            self.image = self.image_down
        else:
            self.image = self.image_up
        
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = speed
        self.direction = direction

        # Determinar a direção do movimento baseado no vetor unitário
        if direction == "down-left":
            self.angle = -225  # 45 graus
        elif direction == "down-right":
            self.angle = 45  # -45 graus
        else:
            self.angle = 0  # Para "up" e "down", não é necessário ajuste de direção

    def update(self, dt):
        # Atualizar a direção do movimento baseado no ângulo
        if self.direction == "up":
            self.rect.y -= self.speed * dt
        elif self.direction == "down":
            self.rect.y += self.speed * dt
        elif self.direction in ["down-left", "down-right"]:
            # Calcular o deslocamento em X e Y para movimentos diagonais
            angle_radians = math.radians(self.angle)  # Converter o ângulo para radianos
            self.rect.x += math.cos(angle_radians) * self.speed * dt
            self.rect.y += math.sin(angle_radians) * self.speed * dt

        # Remove o projétil se sair da tela
        if self.rect.bottom < 0 or self.rect.top > 600 or self.rect.right < 0 or self.rect.left > 800:
            self.kill()

