# This is a version of the popular game Snake that we programmed using pygame
# This game runs on pygame - if you are having difficulty loading it, try entering " pip3 install pygame " in your command prompt
# If you are experiencing issues consider the README.md file


# First, import the necessary modules.
import pygame
from enum import Enum
import random
import time
import sys


# Create a class that includes the directions in which the snake will later move
class Direction(Enum):
    UP = 1
    DOWN = 2
    RIGHT = 3
    LEFT = 4


# We define variables for the window in which the game will be played
window_width = 750
window_height = 750


# We load the background image for the main menu and create the rectangle for the background
bg_image_title = pygame.image.load("Assets/background.png")
bg_rect = bg_image_title.get_rect()


# We run pygame and create a window with the name "Snakegame" using the .set_caption and display.set_mode commands
pygame.init()
pygame.display.set_caption("Snakegame")
window = pygame.display.set_mode((window_width, window_height))


# We create an object to control the fps of our game using .time.Clock()
refresh_controller = pygame.time.Clock()


# We create a class that enables us to easily use different (global) variables inside multiple functions
class gl():
    # The variable rand_food will enable us to change the visuals of the food randomly
    rand_food = 0
    game_paused = False


# We create variables which we will use often in the code, including several fonts and colors for the ui
scale = 20
primary_font = pygame.font.SysFont("Arial", scale * 2, bold=True)
secondary_font = pygame.font.SysFont("Arial", scale)
title_font = pygame.font.SysFont("Arial", scale * 4, bold=True)
title_white = pygame.Color("#ffffff")
title_gray = pygame.Color("#BDBDBD")
title_yellow = pygame.Color("#B68F40")


def reset():
    """Sets the game to its initial values"""
    # We define the initial position of our snake's head and body. These will be stored in a list
    gl.snake_position = [250, 250]
    gl.snake_body = [[250, 250],[240, 250], [230, 250]]
    # We define the first position that the food spawns in
    gl.food_position = [100, 100]
    # We start with the score 0 and get the saved highscore
    gl.score = 0
    get_highscore()
    # We create a random number which will decide which theme that the game has
    gl.rand_theme = random.randint(0, 2)
    choose_theme()


def choose_theme():
    """Changes the games theme according to the variable gl.rand_theme"""
    if gl.rand_theme == 0:
        gl.food_a = pygame.image.load("Assets/food_1.png")
        gl.food_b = pygame.image.load("Assets/food_2.png")
        gl.food_c = pygame.image.load("Assets/food_3.png")
        gl.bg_image = pygame.image.load("Assets/background.png")
        gl.snake_color = pygame.Color("#0AC80A")
    if gl.rand_theme == 1:
        gl.food_a = pygame.image.load("Assets/food_4.png")
        gl.food_b = pygame.image.load("Assets/food_5.png")
        gl.food_c = pygame.image.load("Assets/food_6.png")
        gl.bg_image = pygame.image.load("Assets/background_2.png")
        gl.snake_color = pygame.Color("#B68F40")
    # The first two themes are dark. Therefore the text colors need to be white
    if gl.rand_theme <= 1:
        gl.primary_color = pygame.Color("#ffffff")
        gl.secondary_color = pygame.Color("#E1E4E6")
    if gl.rand_theme == 2:
        gl.food_a = pygame.image.load("Assets/food_7.png")
        gl.food_b = pygame.image.load("Assets/food_8.png")
        gl.food_c = pygame.image.load("Assets/food_9.png")
        gl.bg_image = pygame.image.load("Assets/background_3.png")
        gl.snake_color = pygame.Color("#822926")
        # This theme has a white background. Thus it needs black as the text color
        gl.primary_color = pygame.Color("#000000")
        gl.secondary_color = pygame.Color("#696969")


def get_highscore():
    """Gets the saved highscore"""
    # We try to open the txt file, that stores the highscore
    # The highscore variable will be set to the value saved in the text file
    try:
        file = open("highscore.txt", "r")
        gl.highscore = file.read()
        # If somehow the file has not stored a nummeric value as highscore, we will change the highscore to 0 as string
        if not gl.highscore.isnumeric():
            gl.highscore = "0"
        file.close()
    # We use except for the case if no file was found and create a new highscore file
    # We start with an initial highscore 0 saved as a string
    except:
        file = open("highscore.txt", "x")
        gl.highscore = "0"
        file.close()


def handle_keys(direction):
    """Takes the players keyboardinput and returns a new direction the sneak should head in"""
    new_direction = direction
    # We do this using the .KEYDOWN command, which detects if a button on the keyboard of the player is pressed down
    for event in [e for e in pygame.event.get() if e.type == pygame.KEYDOWN]:
        # The snake changes its direction if the key for the corresponding direction is pressed down and the snake won't do a 180 degree turn
        if event.key == pygame.K_UP and direction != Direction.DOWN:
            new_direction = Direction.UP
        if event.key == pygame.K_DOWN and direction != Direction.UP:
            new_direction = Direction.DOWN
        if event.key == pygame.K_RIGHT and direction != Direction.LEFT:
            new_direction = Direction.RIGHT
        if event.key == pygame.K_LEFT and direction != Direction.RIGHT:
            new_direction = Direction.LEFT
        # If the user presses the escape button the variable gl.game_paused will be set to True in order to pause the game
        if event.key == pygame.K_ESCAPE:
            gl.game_paused = True
    return new_direction


def move_snake(direction):
    """Takes the direction as input and updates the snake's X and Y coordinate accordingly"""
    if direction == Direction.UP:
        gl.snake_position[1] -= scale
    if direction == Direction.DOWN:
        gl.snake_position[1] += scale
    if direction == Direction.LEFT:
        gl.snake_position[0] -= scale
    if direction == Direction.RIGHT:
        gl.snake_position[0] += scale
    # We also have to let the snake grow - we do this by adding a new part at the end of the list that is snake.body
    gl.snake_body.insert(0, (list(gl.snake_position)))


def generate_new():
    """Randomly generates x and y coordinates for the food the snake consumes"""
    gl.food_position[0] = random.randint(5, ((window_width - 2) // scale) * scale)
    gl.food_position[1] = random.randint(5, ((window_height - 2) // scale) * scale)


def change_theme():
    """Changes the gl.rand_theme variable everytime the player reaches a score with a number of ten (0, 10, 20, 30...)
    According to the gl.rand_theme value, the visuals of the game will change"""
    if gl.score % 10 == 0:
        last_theme = gl.rand_theme
        # The while loop makes sure that the random generated number is not the same as it was before
        while gl.rand_theme == last_theme:
            gl.rand_theme = random.randint(0, 2)    


def get_food():
    """Defines what happens if the snake gets food or what happens if it doesen't"""
    # Using an if statement, we check if the position (X/Y coordinates) of the snake's head corresponds to the position of the food
    # within 17 pixels for accuracy
    if abs(gl.snake_position[0] - gl.food_position[0]) < 17 and abs(gl.snake_position[1] - gl.food_position[1]) < 17:
        # If the statement is true, add 1 point to the score
        gl.score += 1
        # Call the generate_new() function to generate new food in the game
        generate_new()
        # Call change_theme() and check if the game needs to change its visuals
        change_theme()
        # We also generate a new random number which we use in the repaint() function 
        gl.rand_food = random.randint(0, 2)
    # If no food was collectes, remove the last part of the snake's body using .pop - this way the snake appears to be moving without growing.
    # In essence, a new part of the snake is generated every tick at the end of the body, but will always be removed if the snake hasn't consumed a new item of food
    else:     
       gl.snake_body.pop()


def repaint():
    """Paints the game using images and color defined in the choose_theme() function"""
    # Drawing the background
    window.blit(gl.bg_image, bg_rect)
    # For the snake we draw circles
    for body in gl.snake_body:
        pygame.draw.circle(window, gl.snake_color, (body[0], body[1]), scale/2)
    # We create a rectangle with the position and size the food will be displayed
    food_rect = pygame.Rect(gl.food_position[0] - scale / 2, gl.food_position[1] - scale / 2, scale, scale)
    # Depending on the random number, that changes every time food is consumed, we change the image of the food
    if gl.rand_food == 0:
     window.blit(gl.food_a, food_rect)
    if gl.rand_food == 1:
        window.blit(gl.food_b, food_rect)
    if gl.rand_food == 2:
        window.blit(gl.food_c, food_rect)


def game_over_message():
    """Displays a message when the snake died and the game is over"""
    window.blit(gl.bg_image, bg_rect)
    # If the score is higher than the highscore, we show a positive message and overwrite the old score on the txt file
    if gl.score > int(gl.highscore):
        message = "Congratulations you beat the highscore"
        file = open("highscore.txt", "w")
        file.write(str(gl.score))
        file.close()
    # If the score is lower or equal the highscore, we show a sad message
    else:
        message = "You didn't beat the highscore :-("
    render_message = primary_font.render(message, True, gl.primary_color)
    rect_message = render_message.get_rect()
    rect_message.midtop = (window_width / 2, window_height / 3)
    render_score = secondary_font.render(f"Your score: {gl.score}", True, gl.secondary_color)
    rect_score = render_score.get_rect()
    rect_score.midtop = (window_width / 2, 1.2 * window_height / 3)
    window.blit(render_message, rect_message)
    window.blit(render_score, rect_score)
    pygame.display.flip()
    # We show this screen 3 seconds and go back to the main menu afterwards
    time.sleep(3)
    main_menu()


def game_over():
    """Defines in which cases the snake dies and the game is over.
    The snake dies when she either touches herself or the edges of the game window"""
    if gl.snake_position[0] < 0 or gl.snake_position[0] > window_width - 10:
        game_over_message()
    if gl.snake_position[1] < 0 or gl.snake_position[1] > window_height - 10:
        game_over_message()
    for blob in gl.snake_body[1:]:
        if gl.snake_position[0] == blob[0] and gl.snake_position[1] == blob[1]:
            game_over_message()


def paint_hud():
    """Displayes the score and highscore during the game"""
    render_score = primary_font.render(f"Score: {gl.score}", True, gl.primary_color)
    render_highscore = secondary_font.render(f"Highscore: {gl.highscore}", True, gl.secondary_color)
    rect = render_score.get_rect()
    window.blit(render_score, rect.move(10, 0))
    window.blit(render_highscore, rect.move(10, 40))
    pygame.display.flip()


def pause_game():
    """Displays a message when the game is paused and takes the escape button as userinput to continue the game"""
    pause_text = title_font.render("Game Paused", True, title_yellow)
    rect = pause_text.get_rect()
    rect.midtop = (window_width / 2, window_height / 7)
    continue_text = primary_font.render(f"Press 'esc' to continue the game", True, gl.primary_color)
    continue_rect = continue_text.get_rect()
    continue_rect.midtop = (window_width / 2, 2 * window_height / 7)
    window.blit (pause_text, rect)
    window.blit (continue_text, continue_rect)
    for event in [e for e in pygame.event.get() if e.type == pygame.KEYDOWN]:
        if event.key == pygame.K_ESCAPE:
            gl.game_paused = False


def main_menu():
    """This is the launch point of the game. It displayes the game title, highscore and the options to start the game or quit the application"""
    get_highscore()
    # Using a while loop to keep the main menu running
    while True:
        # Drawing the background
        window.blit (bg_image_title, bg_rect)
        # Drawing the title "Snakegame"
        menu_text = title_font.render("Snakegame", True, title_yellow)
        menu_rect = menu_text.get_rect()
        menu_rect.midtop = (window_width / 2, window_height / 7)
        window.blit (menu_text, menu_rect)
        # "Your higshcore: ..."
        highscore_text = secondary_font.render(f"Your highscore: {gl.highscore}", True, title_gray)
        highscore_rect = highscore_text.get_rect()
        highscore_rect.midtop = (window_width / 2, 2 * window_height / 7)
        window.blit (highscore_text, highscore_rect)
        # "Play"
        play_text = primary_font.render("Play", True, title_white)
        play_rect = play_text.get_rect()
        play_rect.midtop = (window_width / 3, 3.5 * window_height / 7)
        window.blit (play_text, play_rect)
        # "Quit"
        quit_text = primary_font.render("Quit", True, title_white)
        quit_rect = quit_text.get_rect()
        quit_rect.midtop = (2* window_width / 3, 3.5 * window_height / 7)
        window.blit (quit_text, quit_rect)
        # Displaying the info what the user needs to press
        p_info_text = secondary_font.render("Press 'p' or 'enter'", True, title_white)
        p_info_rect = p_info_text.get_rect()
        p_info_rect.midtop = (window_width / 3, 4 * window_height / 7)
        window.blit (p_info_text, p_info_rect)
        q_info_text = secondary_font.render("Press 'q'", True, title_white)
        q_info_rect = q_info_text.get_rect()
        q_info_rect.midtop = (2 * window_width / 3, 4 * window_height / 7)
        window.blit (q_info_text, q_info_rect)
        # Displaying the hint
        hint_text = secondary_font.render("Hint: Press 'esc' anytime to pause the game", True, title_gray)
        hint_rect = hint_text.get_rect()
        hint_rect.midtop = (window_width / 2, 6 * window_height / 7)
        window.blit (hint_text, hint_rect)
        # Defining which keys need to be pressed down in order to start the game or quit the application
        for event in [e for e in pygame.event.get() if e.type == pygame.KEYDOWN]:
            if event.key == pygame.K_p or event.key == pygame.K_RETURN:
                game_loop()
            if event.key == pygame.K_q:
                pygame.quit
                sys.exit('Game finished')
        pygame.display.update()


def game_loop():
    """This is the game function. At the beginning all variables will be set to their initial values. 
    Afterwards it goes through the predefined functions in a loop and keeps the game running"""
    direction = Direction.RIGHT
    reset()
    # Using a while loop to keep the game running
    while True:
        # When the game is not paused we keep the game running/updating
        while gl.game_paused == False:
            direction = handle_keys(direction)
            move_snake(direction)
            get_food()
            repaint()
            game_over()
            choose_theme()
            paint_hud()
            pygame.display.update()
            refresh_controller.tick()
            time.sleep(0.15)
        # When the game is paused we show the pause_game() message and don't update the game
        while gl.game_paused == True:
            pause_game()
            pygame.display.update()


# We need to make sure, that the game starts at the main menu. Therefore the main_menu() function will be called up
main_menu()
