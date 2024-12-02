import pygame
import random
from projectile import Projectile
from config import HEIGHT, WIDTH

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, shoot_interval):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load('game/assests/imagens/enemy_ship.png'), (150, 150))
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = speed  # Velocidade vertical do inimigo
        self.shoot_interval = 0.9  # Intervalo entre os disparos
        self.shoot_timer = 0  # Cronômetro para disparos

        self.speed_x = 250  # Velocidade de movimento horizontal

          # Carregar som do tiro
        self.shoot_sound = pygame.mixer.Sound("game/assests/sounds/enemy_shoot.wav")
        self.shoot_sound.set_volume(0.5)  # Ajuste o volume do som


    def update(self, dt, projectiles_group, all_sprites):

        # Movimento horizontal
        self.rect.x += self.speed_x * dt
        if self.rect.right >= 611 or self.rect.left <= 222:  # Limites da tela
            self.speed_x = -self.speed_x

        # Movimentação para baixo
        self.rect.y += self.speed * dt

        # Lógica de disparo
        self.shoot_timer += dt
        if self.shoot_timer >= self.shoot_interval:
            self.shoot_timer = 0
            self.shoot(projectiles_group, all_sprites)

        # Remover inimigo se sair da tela
        if self.rect.top > 600:
            self.kill()

    def shoot(self, projectiles_group, all_sprites):
        """Cria um projétil atirado para baixo pelo inimigo."""
        projectile = Projectile(self.rect.centerx, self.rect.bottom, speed=400, direction="down")
        projectiles_group.add(projectile)
        all_sprites.add(projectile)

        self.shoot_sound.play()

class AdvancedEnemy(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, shoot_interval):
        super().__init__()
        self.image = pygame.image.load("game/assests/imagens/advanced_enemy.png")
        self.image = pygame.transform.scale(self.image, (50, 50))  
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = speed
        self.shoot_interval = shoot_interval
        self.shoot_timer = 0
        self.direction = random.choice([-1, 1])  
        self.health = 2 
        self.shoot_sound = pygame.mixer.Sound("game/assests/sounds/enemy_shoot.wav")
        self.shoot_sound.set_volume(0.5)

    def update(self, dt, projectiles_group, all_sprites):
        self.rect.x += self.direction * self.speed * dt
        self.rect.y += self.speed * dt

        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.direction *= -1

        if self.rect.top > HEIGHT:
            self.kill()

        self.shoot_timer += dt
        if self.shoot_timer >= self.shoot_interval:
            self.shoot(projectiles_group, all_sprites)
            self.shoot_timer = 0

    def shoot(self, projectiles_group, all_sprites):
        """Cria dois projéteis disparados para baixo."""
        left_projectile = Projectile(self.rect.left + 10, self.rect.bottom, speed=400, direction="down")
        right_projectile = Projectile(self.rect.right - 10, self.rect.bottom, speed=400, direction="down")
        
        projectiles_group.add(left_projectile, right_projectile)
        all_sprites.add(left_projectile, right_projectile)
        
        # Reproduzir o som de disparo
        self.shoot_sound.play()

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.kill()
