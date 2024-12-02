import pygame
import random
from projectile import Projectile
from enemy import Enemy
from PIL import Image
import os

class Boss(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.frames = self.load_frames()  # Carregar os quadros da animação
        self.current_frame = 0  # Índice do quadro atual
        self.image = self.frames[self.current_frame]  # Definir o quadro inicial
        self.rect = self.image.get_rect(center=(x, y))
        self.health = 80
        self.speed_x = 200
        self.shoot_timer = 0
        self.spawn_timer = 0
        self.frame_timer = 0  # Temporizador para controlar a troca de quadros
        self.frame_delay = 0.1  # Tempo entre cada troca de quadro (ajuste conforme necessário)

    def load_frames(self):
        gif_folder = "game/assests/imagens/boss_frames"
        frames = []
        for filename in sorted(os.listdir(gif_folder)):
            if filename.endswith(".png"):  # Certifique-se de que está carregando imagens
                image = pygame.image.load(os.path.join(gif_folder, filename))
                frames.append(image)
        return frames

    def update(self, dt, enemy_projectiles, enemies, all_sprites):
        # Atualiza a animação do boss
        self.frame_timer += dt
        if self.frame_timer >= self.frame_delay:  # Controla a velocidade da animação
            self.frame_timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.frames)  # Loop através dos quadros
            self.image = self.frames[self.current_frame]  # Atualiza a imagem com o novo quadro

        # Movimento horizontal do boss
        self.rect.x += self.speed_x * dt
        if self.rect.right >= 800 or self.rect.left <= 0:  # Limites da tela
            self.speed_x = -self.speed_x

        # Atirar projéteis
        self.shoot_timer += dt
        if self.shoot_timer > 1:
            self.shoot_timer = 0
            # Projétil central
            central_projectile = Projectile(self.rect.centerx, self.rect.bottom, speed=400, direction="down")
            # Projétil esquerdo
            left_projectile = Projectile(self.rect.centerx - 20, self.rect.bottom, speed=400, direction="down-left")
            # Projétil direito
            right_projectile = Projectile(self.rect.centerx + 20, self.rect.bottom, speed=400, direction="down-right")
            # Adicionar projéteis ao grupo
            enemy_projectiles.add(central_projectile, left_projectile, right_projectile)
            all_sprites.add(central_projectile, left_projectile, right_projectile)

        # Spawnar inimigos menores
        self.spawn_timer += dt
        if self.spawn_timer > 2:
            self.spawn_timer = 0
            x = random.randint(100, 700)
            enemy = Enemy(x, -40, speed=random.randint(150, 200), shoot_interval=random.uniform(2, 4))
            enemies.add(enemy)
            all_sprites.add(enemy)

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.kill()
