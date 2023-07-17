import pygame
import random
import math

# Inicializar pygame
pygame.init()

# Crear pantalla de juego
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("darth-vader.png")
pygame.display.set_icon(icon)
background = pygame.image.load("pexels-francesco-ungaro-998641.jpg")

# Variables del jugador
img_player = pygame.image.load("scienceandfiction-smuggle_99256.png")
player_x = 368  # 400 (mitad) - 32
player_y = 536
player_x_change = 0

# Bullet variables
img_bullet = pygame.image.load("sable-laser.png")
bullet_x = 0
bullet_y = 536
bullet_x_change = 0
bullet_y_change = 1
bullet_visible = False

# Variables de los enemigos (ovnis)
img_enemy = []
enemy_x = []
enemy_y = []
enemy_x_change = []
enemy_y_change = []
enemy_speed = 0.25  # Velocidad inicial de los enemigos
number_of_enemies = 5

for i in range(number_of_enemies):
    img_enemy.append(pygame.image.load("Tie_Fighter_-_03_35417.png"))
    enemy_x.append(random.randint(0, 736))
    enemy_y.append(random.randint(30, 200))
    enemy_x_change.append(enemy_speed)
    enemy_y_change.append(35)

# Variables de los meteoritos
img_meteorite = []
meteorite_x = []
meteorite_y = []
meteorite_y_change = []
meteorite_x_change = []
meteorite_speed = 0.3  # Velocidad inicial de los meteoritos
number_of_meteorite = 5
meteorite_visible = False

for i in range(number_of_meteorite):
    img_meteorite.append(pygame.image.load("Death_Star_-_1st_35438.png"))
    meteorite_x.append(random.randint(0, 736))
    meteorite_x_change.append(meteorite_speed)
    meteorite_y.append(random.randint(30, 200))
    meteorite_y_change.append(35)

# Variables de puntuación
score = 0
score_font = pygame.font.Font("freesansbold.ttf", 32)
score_text_x = 10
score_text_y = 10

# Variables de fin de juego
end_font = pygame.font.Font("freesansbold.ttf", 64)

# Variables de pantalla de inicio
menu_font = pygame.font.Font("freesansbold.ttf", 48)
option_font = pygame.font.Font("freesansbold.ttf", 32)
selected_option = 0  # Opción seleccionada en el menú de inicio

# Cargar nombres y puntajes de los jugadores desde el archivo de texto
players = []
with open("scores.txt", "r") as file:
    for line in file:
        parts = line.split(", ")
        if len(parts) == 2:
            player_name = parts[0].replace("Player: ", "")
            player_score = int(parts[1].replace("Score: ", ""))
            players.append((player_name, player_score))

# Creadores del juego
credits = ["Game created by:",
           "Abraham",
           "Benjamín",
           "Nicolas"]


# Mensaje de fin de juego
def final_message():
    final_text = end_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(final_text, (200, 200))


# Mostrar puntuación
def show_score(x, y):
    text = score_font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(text, (x, y))


# Mostrar jugador en pantalla
def player(x, y):
    screen.blit(img_player, (x, y))


# Mostrar enemigo (ovni)
def enemy(x, y, enemy_index):
    screen.blit(img_enemy[enemy_index], (x, y))


# Mostrar meteorito
def meteorite(x, y, meteorite_index):
    screen.blit(img_meteorite[meteorite_index], (x, y))


# Disparar bala
def shoot_bullet(x, y):
    global bullet_x, bullet_y, bullet_visible
    bullet_x = x
    bullet_y = y
    bullet_visible = True


# Detectar colisión entre dos objetos
def detect_collision(x_1, y_1, x_2, y_2):
    x_sub = x_2 - x_1
    y_sub = y_2 - y_1
    distance = math.sqrt(math.pow(x_sub, 2) + math.pow(y_sub, 2))
    if distance < 27:
        return True
    else:
        return False


# Pantalla de inicio
def show_menu():
    screen.blit(background, (0, 0))
    title_text = menu_font.render("Space Invaders", True, (255, 255, 255))
    screen.blit(title_text, (screen_width // 2 - 180, 150))

    # Opciones del menú
    option_start = option_font.render("Start Game", True, (255, 255, 255))
    option_scores = option_font.render("View Scores", True, (255, 255, 255))
    option_credits = option_font.render("Credits", True, (255, 255, 255))

    screen.blit(option_start, (screen_width // 2 - 110, 300))
    screen.blit(option_scores, (screen_width // 2 - 110, 350))
    screen.blit(option_credits, (screen_width // 2 - 110, 400))


# Mostrar puntajes
def show_scores():
    screen.blit(background, (0, 0))
    title_text = menu_font.render("Scores", True, (255, 255, 255))
    screen.blit(title_text, (screen_width // 2 - 80, 50))

    # Mostrar jugadores y puntajes
    scores_y = 150
    for player_info in players:
        player_name = player_info[0]
        player_score = player_info[1]
        player_text = option_font.render(f"{player_name}: {player_score}", True, (255, 255, 255))
        screen.blit(player_text, (screen_width // 2 - 80, scores_y))
        scores_y += 50


# Mostrar créditos
def show_credits():
    screen.blit(background, (0, 0))
    title_text = menu_font.render("Credits", True, (255, 255, 255))
    screen.blit(title_text, (screen_width // 2 - 80, 50))

    # Mostrar nombres de los creadores
    credits_y = 150
    for credit in credits:
        credit_text = option_font.render(credit, True, (255, 255, 255))
        screen.blit(credit_text, (screen_width // 2 - 110, credits_y))
        credits_y += 50


def game_loop():
    # Variables needed for the game loop
    global player_x, player_x_change, bullet_x, bullet_y, bullet_visible, is_name_saved
    global meteorite_visible, score, enemy_x, enemy_y, enemy_x_change, enemy_y_change, enemy_speed

    # Game loop
    while True:
        screen.blit(background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player_x_change -= 0.3
                if event.key == pygame.K_RIGHT:
                    player_x_change += 0.3
                if event.key == pygame.K_SPACE:
                    if not bullet_visible:
                        shoot_bullet(player_x, player_y)
                if event.key == pygame.K_ESCAPE:
                    return True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    player_x_change = 0

        player_x += player_x_change

        if player_x <= 0:
            player_x = 0
        elif player_x >= 736:
            player_x = 736

        for i in range(number_of_enemies):
            if enemy_y[i] > 450:
                for j in range(number_of_enemies):
                    enemy_y[j] = 1000
                    if meteorite_visible == True:
                        for j in range(number_of_meteorite):
                           meteorite_y[j] = 1001
                final_message()
                # Solicitar nombre del jugador y registrar puntuación una sola vez
                if not is_name_saved:
                    player_name = input("Enter your name: ")
                    with open("scores.txt", "a") as file:
                        file.write(f"Player: {player_name}, Score: {score} \n")
                    is_name_saved = True
                break

            enemy_x[i] += enemy_x_change[i]

            if enemy_x[i] <= 0:
                enemy_x_change[i] = enemy_speed
                enemy_y[i] += enemy_y_change[i]
            elif enemy_x[i] >= 736:
                enemy_x_change[i] = -enemy_speed
                enemy_y[i] += enemy_y_change[i]

            collision = detect_collision(enemy_x[i], enemy_y[i], bullet_x, bullet_y)

            if collision:
                enemy_x[i] = random.randint(0, 736)
                enemy_y[i] = random.randint(30, 200)
                bullet_visible = False
                score += 1
                bullet_y = 500

            enemy(enemy_x[i], enemy_y[i], i)

        if 10 <= score < 20:
            enemy_speed = 0.3
        elif score >= 20:
            enemy_speed = 0.4

        if bullet_y <= -64:
            bullet_y = 500
            bullet_visible = False

        if bullet_visible:
            pygame.draw.rect(screen, (255, 0, 0), (bullet_x + 16, bullet_y + 10, 8, 24))
            bullet_y -= 1

        player(player_x, player_y)
        show_score(score_text_x, score_text_y)


        # Generar meteoritos cuando el puntaje alcance 30
        if score >= 30:
            for i in range(number_of_meteorite):
                collision_pm = detect_collision(player_x, player_y, meteorite_x[i], meteorite_y[i])
                if 582 <= meteorite_y[i] <= 1000:
                    meteorite_x[i] = random.randint(0, 736)
                    meteorite_y[i] = random.randint(30, 200)
                if collision_pm:
                    for j in range(number_of_meteorite):
                        meteorite_y[j] = 1001
                    for t in range(number_of_meteorite):
                        enemy_y[t] = 1000
                    final_message()
                    # Solicitar nombre del jugador y registrar puntuación una sola vez
                    if not is_name_saved:
                        player_name = input("Enter your name: ")
                        with open("scores.txt", "a") as file:
                            file.write(f"Player: {player_name}, Score: {score} \n")
                            is_name_saved = True
                    break

            collision_bm = detect_collision(meteorite_x[i], meteorite_y[i], bullet_x, bullet_y)

            if collision_bm:
                meteorite_x[i] = random.randint(0, 736)
                meteorite_y[i] = random.randint(30, 200)
                bullet_visible = False
                bullet_y = 500

            meteorite_y[i] += meteorite_x_change[i]
            meteorite(meteorite_x[i], meteorite_y[i], i)
        pygame.display.update()

def main_menu():
    # Variables del menú
    global selected_option
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % 3
                if event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % 3
                if event.key == pygame.K_RETURN:
                    if selected_option == 0:
                        return True
                    elif selected_option == 1:
                        show_scores()
                        pygame.display.update()
                        pygame.time.wait(3000)  # Espera 3 segundos antes de volver al menú
                    elif selected_option == 2:
                        show_credits()
                        pygame.display.update()
                        pygame.time.wait(3000)  # Espera 3 segundos antes de volver al menú
        show_menu()
        pygame.draw.rect(screen, (255, 255, 255),
                         (screen_width // 2 - 140, 300 + selected_option * 50, 280, 40), 3)
        pygame.display.update()


# Initialize game variables
bullet_x = 0
bullet_y = 0
bullet_visible = False
is_name_saved = False  # Flag to indicate if the player's name has already been saved

# Bucle principal del juego
while True:
    if not main_menu():
        break
    if not game_loop():
        break