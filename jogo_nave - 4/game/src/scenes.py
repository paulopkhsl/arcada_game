import pygame
from config import WIDTH, HEIGHT, BLACK, WHITE, RED
from player import Player
from enemy import Enemy
from obstacles import Meteor
import random



import pygame
from config import WIDTH, HEIGHT, BLACK, WHITE, RED
from player import Player
from enemy import Enemy
from obstacles import Meteor
import random
import os


class TitleScene:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 74)
        self.options_font = pygame.font.Font(None, 50)
        self.options = ["Iniciar Jogo", "Ranking"]
        self.selected_option = 0

        # Iniciar a música tema
        pygame.mixer.music.load("game/assests/music/theme_music.mp3")  # Caminho para a música
        pygame.mixer.music.play(-1, 0.0)  # -1 para loop infinito

    def update(self, dt):
        self.screen.fill(BLACK)
        
        # Renderizar título
        title = self.font.render("Jogo de Nave Arcade", True, WHITE)
        self.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 3))

        # Renderizar opções do menu
        for i, option in enumerate(self.options):
            color = RED if i == self.selected_option else WHITE
            option_text = self.options_font.render(option, True, color)
            self.screen.blit(option_text, (WIDTH // 2 - option_text.get_width() // 2, HEIGHT // 2 + i * 60))

        # Controle de seleção
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.selected_option = (self.selected_option - 1) % len(self.options)
        elif keys[pygame.K_DOWN]:
            self.selected_option = (self.selected_option + 1) % len(self.options)

        # Iniciar jogo ou abrir ranking
        if keys[pygame.K_RETURN]:
            if self.selected_option == 0:  # Iniciar Jogo
                pygame.mixer.music.stop()  # Parar música ao começar o jogo
                return GameScene(self.screen)  # A cena do jogo agora recebe o jogador
            elif self.selected_option == 1:  # Ranking
                return RankingScene(self.screen)
        return self





WIDTH, HEIGHT = 800, 600
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

from powerup import PowerUp
import pygame
from config import WIDTH, HEIGHT, BLACK, WHITE, RED
from player import Player
from enemy import Enemy, AdvancedEnemy
from obstacles import Meteor
from powerup import PowerUp
import random
import os


class GameScene:
    def __init__(self, screen, phase=1, score=0, lives=3):
        self.screen = screen
        self.phase = phase
        self.score = score
        self.lives = lives
        self.all_sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.meteors = pygame.sprite.Group()
        self.player_projectiles = pygame.sprite.Group()
        self.enemy_projectiles = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()

        self.load_music()

        # Carregar quadros do GIF de fundo
        self.bg_frames = self.load_background_frames("game/assests/imagens/background_frames")
        self.current_frame = 0
        self.frame_timer = 0

        # Carregar imagem de coração
        self.heart_image = pygame.image.load("game/assests/imagens/heart.png")
        self.heart_image = pygame.transform.scale(self.heart_image, (30, 30))

        # Carregar imagem do escudo
        self.shield_icon = pygame.image.load("game/assests/imagens/shield.png")
        self.shield_icon = pygame.transform.scale(self.shield_icon, (30, 30))

        # Criar o jogador
        self.player = Player(WIDTH // 2, HEIGHT - 70)
        self.all_sprites.add(self.player)

        self.spawn_timer = 0
        self.phase_timer = 0
        self.powerup_timer = 0
        self.phase_duration = 5

        self.font = pygame.font.Font(None, 36)
    

    def spawn_powerup(self):
        x = random.randint(40, WIDTH - 40)
        powerup_type = random.choice(["shield", "extra_life"])
        powerup = PowerUp(x, -30, powerup_type)
        self.powerups.add(powerup)
        self.all_sprites.add(powerup)



    def spawn_meteor(self):
        x = random.randint(50, WIDTH - 50)
        meteor = Meteor(x, -50)
        self.meteors.add(meteor)
        self.all_sprites.add(meteor)

    def load_background_frames(self, path):
        """Carrega quadros de uma animação de fundo."""
        frames = []
        for filename in sorted(os.listdir(path)):
            if filename.endswith(".png"):  # Certifique-se de usar apenas imagens
                frame = pygame.image.load(os.path.join(path, filename)).convert()
                frame = pygame.transform.scale(frame, (WIDTH, HEIGHT))
                frames.append(frame)
        return frames

    def render_background(self, dt):
        """Renderiza o fundo animado."""
        if len(self.bg_frames) == 0:
            return  # Caso não tenha quadros de fundo, não renderize nada

        self.frame_timer += dt
        if self.frame_timer > 0.1:  # Alterar quadro a cada 0.1s
            self.current_frame = (self.current_frame + 1) % len(self.bg_frames)
            self.frame_timer = 0  # Reset o timer após cada quadro

        self.screen.blit(self.bg_frames[self.current_frame], (0, 0))
        
    
    def render_hud(self):
        """Desenha o HUD na tela."""
        score_text = self.font.render(f"Pontuação: {self.score}", True, WHITE)
        phase_text = self.font.render(f"Fase: {self.phase}", True, WHITE)

        self.screen.blit(score_text, (10, 10))
        self.screen.blit(phase_text, (10, 50))

        # Renderizar as vidas como corações
        for i in range(self.lives):
            self.screen.blit(self.heart_image, (WIDTH - 40 - i * 35, 10))

        # Renderizar o ícone de escudo, se o escudo estiver ativo
        if self.player.shield_active:
            self.screen.blit(self.shield_icon, (WIDTH - 40, HEIGHT - 40))


    def load_music(self):
        """Carrega e inicia a música tema com base na fase."""
        pygame.mixer.music.stop()  # Para qualquer música anterior
        if self.phase == 1:
            pygame.mixer.music.load("game/assests/music/theme_music1.mp3")
        elif self.phase == 2:
            pygame.mixer.music.load("game/assests/music/theme_music1.mp3")
        elif self.phase == 3:
            pygame.mixer.music.load("game/assests/music/theme_music1.mp3")
        pygame.mixer.music.set_volume(0.5)  # Define o volume da música
        pygame.mixer.music.play(-1)  # Reproduz a música em loop


    def spawn_enemy(self):
        x = random.randint(40, WIDTH - 40)
        speed = random.randint(100, 200)
        shoot_interval = random.uniform(1.5, 2.5)

        # Inimigos avançados ou normais com base na fase
        if self.phase in [2, 3]:
            if random.random() < 0.5:  # 50% de chance de AdvancedEnemy
                enemy = AdvancedEnemy(x, -40, speed, shoot_interval)
            else:  # Caso contrário, cria um inimigo normal
                enemy = Enemy(x, -40, speed, shoot_interval)
        else:  # Fase 1: Apenas inimigos normais
            enemy = Enemy(x, -40, speed, shoot_interval)

        self.enemies.add(enemy)
        self.all_sprites.add(enemy)
        

    def update(self, dt):
        self.render_background(dt)  # Renderiza o fundo animado
        self.phase_timer += dt

        if self.phase_timer > self.phase_duration:
            if self.phase < 3:
                return GameScene(self.screen, phase=self.phase + 1, score=self.score, lives=self.lives)
            else:
                return BossScene(self.screen, score=self.score, lives=self.lives)

        keys = pygame.key.get_pressed()
        for sprite in self.all_sprites:
            if isinstance(sprite, Player):
                sprite.update(keys, dt, self.player_projectiles, self.all_sprites)
            elif isinstance(sprite, Enemy):
                sprite.update(dt, self.enemy_projectiles, self.all_sprites)
            elif isinstance(sprite, Meteor):
                sprite.update(dt)
            elif isinstance(sprite, PowerUp):
                sprite.update(dt)
            elif isinstance(sprite, AdvancedEnemy):
                sprite.update(dt, self.enemy_projectiles, self.all_sprites)
            else:
                sprite.update(dt)

        self.spawn_timer += dt
        if self.spawn_timer > (1.5 if self.phase == 1 else 1.0):
            self.spawn_enemy()
            self.spawn_meteor()
            self.spawn_timer = 0

        self.powerup_timer += dt
        if self.powerup_timer > 5:
            self.spawn_powerup()
            self.powerup_timer = 0

        hits = pygame.sprite.groupcollide(self.player_projectiles, self.enemies, True, True)
        self.score += len(hits) * 10

        pygame.sprite.groupcollide(self.player_projectiles, self.meteors, True, False)

        if pygame.sprite.spritecollide(self.player, self.enemy_projectiles, True):
            if not self.player.shield_active:
                self.lives -= 1
            else:
                self.player.deactivate_shield()
            if self.lives <= 0:
                print("Game Over")
                return TitleScene(self.screen)

        collected_powerups = pygame.sprite.spritecollide(self.player, self.powerups, True)
        for powerup in collected_powerups:
            if powerup.type == "shield":
                self.player.activate_shield()
            elif powerup.type == "extra_life":
                self.lives += 1

        if pygame.sprite.spritecollide(self.player, self.enemies, True) and not self.player.shield_active:
            self.lives -= 1
            if self.lives <= 0:
                print("Game Over")
                return TitleScene(self.screen)

        if pygame.sprite.spritecollide(self.player, self.meteors, False) and not self.player.shield_active:
            self.lives -= 1
            if self.lives <= 0:
                print("Game Over")
                return TitleScene(self.screen)

        self.render_hud()
        self.all_sprites.draw(self.screen)

        return self




from boss import Boss
from powerup import PowerUp
import random

class BossScene:
    def __init__(self, screen, score, lives):
        self.screen = screen
        self.score = score
        self.lives = lives

     # Gerenciamento de música
        pygame.mixer.music.stop()  # Para qualquer música anterior
        pygame.mixer.music.load("game/assests/music/theme_music_boss.mp3")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1) 

        self.all_sprites = pygame.sprite.Group()
        self.enemy_projectiles = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.player_projectiles = pygame.sprite.Group()
        self.meteors = pygame.sprite.Group()  # Grupo de meteoros
        self.powerups = pygame.sprite.Group()  # Novo grupo para power-ups

        # Jogador
        self.player = Player(WIDTH // 2, HEIGHT - 70)
        self.all_sprites.add(self.player)

        # Boss
        self.boss = Boss(WIDTH // 2, 100)
        self.all_sprites.add(self.boss)

        self.spawn_timer = 0
        self.meteor_spawn_timer = 0  # Timer para spawnar meteoros
        self.powerup_timer = 0  # Timer para spawn de power-ups
        self.font = pygame.font.Font(None, 36)

        # Tempos para spawn
        self.spawn_timer = 0
        self.meteor_spawn_timer = 0  # Timer para spawnar meteoros
        self.powerup_timer = 0  # Timer para spawn de power-ups
        self.advanced_enemy_spawn_timer = 0  # Timer para spawn de inimigos avançados
        self.font = pygame.font.Font(None, 36)


        # Carregar imagem de coração
        self.heart_image = pygame.image.load("game/assests/imagens/heart.png")  # Caminho para a imagem de coração
        self.heart_image = pygame.transform.scale(self.heart_image, (30, 30))  # Redimensiona o ícone

        # Carregar imagens para o escudo
        self.shield_image = pygame.image.load("game/assests/imagens/shield.png")  # Caminho para a imagem do escudo
        self.shield_image = pygame.transform.scale(self.shield_image, (30, 30))  # Redimensiona a imagem do escudo

        # Carregar quadros do GIF de fundo
        self.bg_frames = self.load_background_frames("game/assests/imagens/background_boss_frames")
        self.current_frame = 0
        self.frame_timer = 0  # Timer para controlar a troca de quadros

    def load_background_frames(self, path):
        """Carrega quadros de uma animação de fundo."""
        frames = []
        for filename in sorted(os.listdir(path)):
            if filename.endswith(".png"):  # Certifique-se de usar apenas imagens
                frame = pygame.image.load(os.path.join(path, filename)).convert()
                frame = pygame.transform.scale(frame, (WIDTH, HEIGHT))
                frames.append(frame)
        return frames

    def render_background(self, dt):
        """Renderiza o fundo animado."""
        if len(self.bg_frames) == 0:
            return  # Caso não tenha quadros de fundo, não renderize nada

        self.frame_timer += dt
        if self.frame_timer > 0.1:  # Alterar quadro a cada 0.1s
            self.current_frame = (self.current_frame + 1) % len(self.bg_frames)
            self.frame_timer = 0  # Reset o timer após cada quadro

        self.screen.blit(self.bg_frames[self.current_frame], (0, 0))

    def spawn_meteor(self):
        """Cria e adiciona meteoros."""
        x = random.randint(50, WIDTH - 50)
        meteor = Meteor(x, -50)
        self.meteors.add(meteor)
        self.all_sprites.add(meteor)

    def spawn_powerup(self):
        """Cria e adiciona power-ups aleatórios na fase do boss."""
        x = random.randint(40, WIDTH - 40)
        powerup_type = random.choice(["shield", "extra_life"])  # Power-ups disponíveis
        powerup = PowerUp(x, -30, powerup_type)
        self.powerups.add(powerup)
        self.all_sprites.add(powerup)

    def render_hearts(self):
        """Desenha os corações representando as vidas no HUD."""
        for i in range(self.lives):
            self.screen.blit(self.heart_image, (WIDTH - 40 - i * 35, 10))

    def render_shields(self):
        """Desenha o escudo no HUD se estiver ativo."""
        if self.player.shield_active:
            self.screen.blit(self.shield_image, (WIDTH - 40, HEIGHT - 40))

    def spawn_advanced_enemy(self):
        """Cria e adiciona um inimigo avançado."""
        x = random.randint(50, WIDTH - 50)
        advanced_enemy = AdvancedEnemy(x, -50, speed=150, shoot_interval=2)
        self.enemies.add(advanced_enemy)
        self.all_sprites.add(advanced_enemy)

    def update(self, dt):
        """Atualiza lógica da luta contra o boss."""
        self.render_background(dt)

        # Atualizar todos os sprites
        keys = pygame.key.get_pressed()
        for sprite in self.all_sprites:
            if isinstance(sprite, Player):
                sprite.update(keys, dt, self.player_projectiles, self.all_sprites)
            elif isinstance(sprite, Boss):
                sprite.update(dt, self.enemy_projectiles, self.enemies, self.all_sprites)
            elif isinstance(sprite, Enemy):
                sprite.update(dt, self.enemy_projectiles, self.all_sprites)  # Passa os grupos necessários
            elif isinstance(sprite, Meteor):
                sprite.update(dt)
            elif isinstance(sprite, PowerUp):  # Atualiza power-ups
                sprite.update(dt)
            elif isinstance(sprite, AdvancedEnemy):
                sprite.update(dt, self.enemy_projectiles, self.all_sprites)
            else:
                sprite.update(dt)


        # Spawnar meteoros e power-ups periodicamente
        self.meteor_spawn_timer += dt
        self.powerup_timer += dt
        self.advanced_enemy_spawn_timer += dt
        
        if self.meteor_spawn_timer > 1.5:  # Meteoros a cada 1.5 segundos
            self.spawn_meteor()
            self.meteor_spawn_timer = 0

        if self.powerup_timer > 5:  # Power-ups a cada 5 segundos
            self.spawn_powerup()
            self.powerup_timer = 0

        # Spawn de inimigos avançados a cada 4 segundos
        if self.advanced_enemy_spawn_timer > 4:
            self.spawn_advanced_enemy()
            self.advanced_enemy_spawn_timer = 0


        # Colisão de projéteis do jogador com o boss
        boss_hits = pygame.sprite.spritecollide(self.boss, self.player_projectiles, True)
        for _ in boss_hits:
            self.boss.take_damage(1)
            self.score += 20

        # Colisão de projéteis do jogador com inimigos
        pygame.sprite.groupcollide(self.player_projectiles, self.enemies, True, True)

        # Colisão de projéteis inimigos com o jogador
        if pygame.sprite.spritecollide(self.player, self.enemy_projectiles, True):
            if not self.player.shield_active:  # Se o escudo não estiver ativo
                self.lives -= 1
            else:
                self.player.deactivate_shield()  # Desativa o escudo após a colisão
            if self.lives <= 0:
                print("Game Over")
                return TitleScene(self.screen)

        # Colisão de inimigos e meteoros com o jogador
        if pygame.sprite.spritecollide(self.player, self.enemies, True) and not self.player.shield_active:
            self.lives -= 1
            if self.lives <= 0:
                print("Game Over")
                return TitleScene(self.screen)
        if pygame.sprite.spritecollide(self.player, self.meteors, False) and not self.player.shield_active:
            self.lives -= 1
            if self.lives <= 0:
                print("Game Over")
                return TitleScene(self.screen)

        # Colisão de power-ups com o jogador
        collected_powerups = pygame.sprite.spritecollide(self.player, self.powerups, True)
        for powerup in collected_powerups:
            if powerup.type == "shield":
                self.player.activate_shield()  # Ativa o escudo
            elif powerup.type == "extra_life":
                self.lives += 1  # Adiciona vida

        # Verificar se o boss foi derrotado
        if not self.boss.alive():
            print("Você derrotou o boss!")
            return TitleScene(self.screen)  # Retorna ao menu principal

        # Renderizar HUD
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        boss_health_text = self.font.render(f"Boss HP: {self.boss.health}", True, RED)
        shield_status_text = self.font.render(f"Escudo: {'Ativo' if self.player.shield_active else 'Inativo'}", True, WHITE)

        self.render_hearts()  # Renderiza os corações
        self.render_shields()  # Renderiza o escudo
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(boss_health_text, (10, 50))
        self.screen.blit(shield_status_text, (10, 90))

        # Desenhar todos os sprites
        self.all_sprites.draw(self.screen)

        return self





class RankingScene:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 50)
        self.ranking = ["1. 10000", "2. 8000", "3. 6000", "4. 4000", "5. 2000"]

    def update(self, dt):
        self.screen.fill(BLACK)
        
        # Renderizar título do ranking
        title = self.font.render("Ranking", True, WHITE)
        self.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 6))

        # Renderizar as pontuações
        for i, score in enumerate(self.ranking):
            score_text = self.font.render(score, True, WHITE)
            self.screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 3 + i * 40))

        # Voltar para o menu
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            return TitleScene(self.screen)
        return self


