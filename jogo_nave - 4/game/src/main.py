import pygame
from scenes import TitleScene

# Configuração inicial
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jogo de Nave Arcade 2D")
clock = pygame.time.Clock()

# Loop principal
def main():
    scene = TitleScene(screen)  # Começa na tela de título
    running = True
    while running:
        dt = clock.tick(60) / 1000  # Delta time
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        scene = scene.update(dt)  # Atualiza a cena atual
        pygame.display.flip()
    pygame.quit()

if __name__ == "__main__":
    main()

