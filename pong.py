import pygame, sys, random
 
pygame.init()
 
WIDTH, HEIGHT = 1280, 720
 
FONT = pygame.font.SysFont("Consolas", int(WIDTH/20))
 
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong!")
CLOCK = pygame.time.Clock()

# Paddles
player = pygame.Rect(WIDTH-110, HEIGHT/2-50, 10, 100)
opponent = pygame.Rect(110, HEIGHT/2-50, 10, 100)

# Score
player_score, opponent_score = 0, 0

# Ball
ball = pygame.Rect(WIDTH/2-10, HEIGHT/2-10, 20, 20)
x_speed, y_speed = 1,1

# SFX
ball_sfx = pygame.mixer.Sound("Ping pong ball hit - Sound Effect (HD).mp3")
score_sfx = pygame.mixer.Sound("score.mp3")
 
 # Main Game Loop
while True:
    Keys_pressed = pygame.key.get_pressed()

    # Key input
    if Keys_pressed[pygame.K_UP]:
        if player.top > 0:
            player.top -= 2
    if Keys_pressed[pygame.K_DOWN]:
        if player.bottom < HEIGHT:
            player.bottom += 2
            
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Ball logic
    if ball.bottom >= HEIGHT:
        y_speed = -1
    if ball.y <= 0:
        y_speed = 1
    if ball.x >= WIDTH:
        opponent_score += 1
        ball.center = (WIDTH/2, HEIGHT/2)
        x_speed, y_speed = random.choice([1, -1]), random.choice([1, -1])
        score_sfx.play()
    if ball.x <= 0:
        player_score += 1
        ball.center = (WIDTH/2, HEIGHT/2)
        x_speed, y_speed = random.choice([1, -1]), random.choice([1, -1])
        score_sfx.play()

    # Ball collision with paddles    
    if ball.colliderect(player):
        x_speed = -1
        ball_sfx.play()
    if ball.colliderect(opponent):
        x_speed = 1
        ball_sfx.play()

    ball.x += x_speed * 2
    ball.y += y_speed * 2

    # Opponent AI
    if opponent.centery < ball.y and opponent.bottom < HEIGHT:
        opponent.y += 1
    elif opponent.centery > ball.y and opponent.top > 0:
        opponent.y -= 1

    # Score
    player_score_text = FONT.render(f"{str(player_score//10)}{str(player_score%10)}", True, "white")
    opponent_score_text = FONT.render(f"{str(opponent_score//10)}{str(opponent_score%10)}", True, "white")


    SCREEN.fill("BLACK")

    # Draws middle line
    for index, i in enumerate(range(18, HEIGHT, HEIGHT // 20)):
        if index % 2 == 0:
            pygame.draw.rect(SCREEN, "white", (WIDTH // 2 - 3, i, 6, HEIGHT // 20))


    # Draws player and AI paddle
    pygame.draw.rect(SCREEN, "white", player)
    pygame.draw.rect(SCREEN, "white", opponent)
    pygame.draw.circle(SCREEN, "white", ball.center, 10)

    # Draws score
    SCREEN.blit(player_score_text, (WIDTH/2 + 300, 50))
    SCREEN.blit(opponent_score_text, (WIDTH/2 - 350, 50))
 
    pygame.display.update()
    CLOCK.tick(300)