"""
python -m pip install pygame pymunk
python3 -m pip install pygame pymunk
"""
import pygame
import pymunk
import pymunk.pygame_util

WIDTH, HEIGHT = 1000, 400
FPS = 120

N = 5 # 0 ~ 5
MASS_SMALL = 1
MASS_LARGE = 100 ** N

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    draw_options = pymunk.pygame_util.DrawOptions(screen)

    space = pymunk.Space()
    space.gravity = (0, 0)
    space.iterations = 30

    wall_body = space.static_body
    wall = pymunk.Segment(wall_body, (50, 0), (50, HEIGHT), 5)
    wall.elasticity = 1.0
    wall.friction = 0.0
    wall.collision_type = 3
    wall.color = (200, 200, 200, 255)
    space.add(wall)

    def create_block(x, size, mass, vel, color, collision_type):
        moment = float('inf')
        body = pymunk.Body(mass, moment)
        body.position = (x, HEIGHT - size/2 - 20)

        shape = pymunk.Poly.create_box(body, (size, size))
        shape.elasticity = 1.0
        shape.friction = 0.0
        shape.color = color
        shape.collision_type = collision_type

        body.velocity = (vel, 0)

        space.add(body, shape)
        return body

    create_block(250, 40, MASS_SMALL, 0, (255, 80, 80, 255), 1)
    create_block(600, 100, MASS_LARGE, -50, (80, 160, 255, 255), 2)

    collision_count = [0]

    def count_collision(arbiter, space_, data):
        collision_count[0] += 1
        return True

    space.on_collision(1, 2, begin=count_collision)
    space.on_collision(1, 3, begin=count_collision)

    font = pygame.font.SysFont("Arial", 40, bold=True)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        dt = 1.0 / FPS
        substeps = 10000
        for _ in range(substeps):
            space.step(dt / substeps)

        screen.fill((20, 20, 25))
        space.debug_draw(draw_options)

        txt = font.render(f"Collisions: {collision_count[0]}", True, (240, 240, 240))
        screen.blit(txt, (70, 10))

        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()
if __name__ == "__main__":main()
