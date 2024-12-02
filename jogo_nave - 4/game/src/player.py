import pygame
from projectile import Projectile
from config import WIDTH, HEIGHT, GREEN, WHITE

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Carregar as imagens uma vez
        self.player_image = pygame.transform.scale(pygame.image.load('game/assests/imagens/player_ship.png'), (50, 50))
        self.player_shield_image = pygame.transform.scale(pygame.image.load('game/assests/imagens/player_ship_shield.png'), (50, 50))
        
        # Definir a imagem inicial
        self.image = self.player_image
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 450  # Velocidade de movimento do jogador
        self.shoot_delay = 0.3 # Intervalo entre os disparos
        self.last_shot = 0  # Tempo desde o último disparo

        # Propriedades para power-ups
        self.shield_active = False  # Indica se o escudo está ativo
        self.shield_timer = 0  # Tempo restante do escudo
        self.max_shield_time = 5  # Duração do escudo (em segundos)

        self.lives = 3  # Vidas do jogador

         # Carregar som do tiro
        self.shoot_sound = pygame.mixer.Sound("game/assests/sounds/player_shoot.wav")
        self.shoot_sound.set_volume(0.5)  # Ajuste o volume do som


    def update(self, keys, dt, projectiles_group, all_sprites):
        # Movimentação
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.rect.y -= self.speed * dt
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.rect.y += self.speed * dt
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.rect.x -= self.speed * dt
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.rect.x += self.speed * dt
        self.rect.clamp_ip(pygame.Rect(0, 0, 800, 600))  # Impede que o jogador saia da tela

        # Lógica de disparo
        self.last_shot += dt
        if keys[pygame.K_SPACE] and self.last_shot >= self.shoot_delay:
            self.last_shot = 0
            self.shoot(projectiles_group, all_sprites)

        # Atualiza o escudo
        if self.shield_active:
            self.shield_timer -= dt
            if self.shield_timer <= 0:
                self.deactivate_shield()  # Desativa o escudo quando o tempo acabar

        # Atualiza a imagem da nave dependendo do estado do escudo
        if self.shield_active:
            self.image = self.player_shield_image
        else:
            self.image = self.player_image

    def shoot(self, projectiles_group, all_sprites):
        """Cria um projétil atirado para cima pelo jogador."""
        projectile = Projectile(self.rect.centerx, self.rect.top, speed=400, direction="up")
        projectiles_group.add(projectile)
        all_sprites.add(projectile)

        self.shoot_sound.play()

        
    def take_damage(self):
        """Gerencia dano ao jogador, considerando o escudo."""
        if self.shield_active:
            self.shield_active = False  # O escudo absorve o dano
            return False  # O jogador não perde vida quando o escudo está ativo
        else:
            self.lives -= 1  # O jogador perde uma vida
            if self.lives <= 0:
                return True  # O jogador perde todas as vidas
            return False  # O jogador não perde todas as vidas ainda

    def draw_shield(self, surface):
        """Desenha o escudo ao redor do jogador se ele estiver ativo."""
        if self.shield_active:
            pygame.draw.circle(surface, (0, 0, 255), self.rect.center, self.rect.width // 2 + 10, 5)  # Escudo azul

    def collide_with_enemy_projectiles(self, enemy_projectiles_group):
        """Verifica se o jogador colidiu com projéteis inimigos."""
        for projectile in enemy_projectiles_group:
            if self.rect.colliderect(projectile.rect):
                if not self.shield_active:
                    self.take_damage()
                projectile.kill()  # Remove o projétil após a colisão
    
    def activate_shield(self):
        """Ativa o escudo por um período limitado."""
        self.shield_active = True
        self.shield_timer = self.max_shield_time

    def deactivate_shield(self):
        """Desativa o escudo."""
        self.shield_active = False
        self.shield_timer = 0  
