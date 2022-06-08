"""
ATV (road rush Type) race game

author: ashraf minhaj
mail  : ashraf_minhaj@yahoo.com
"""

""" install -
$ pip install pygame
"""

""" import libraries """
import pygame            # our main game library
import glob              # for easy file searching
import random            # to get lane randomly


""" initialize """
pygame.init()                                   # initialize
window = pygame.display.set_mode((784, 549))    # set window as per our image size


""" load track images """
tracks = glob.glob('tracks/*jpg')  # get track images
index = 0

def next_img():
    # get next image, repeat through all images over and over
    global index
    if index == len(tracks):
        # if it reaches end of the loop
        # begin from start
        index = 0
    bg = tracks[index]
    index += 1
    return bg


""" vehicle speed or game's refresh rate """
# set up timer clock 
clock = pygame.time.Clock()
# at the beginning it's zero
# it's actually our bike's speed
fps = 0                      


""" bike """
bike_x, bike_y = 330, 200                       # default x,y pos of main bike
bike           = pygame.image.load("atv.png")   # our bike


""" define road edges """
road_edge_left   = 150
roard_edge_right = 550
vanish_point     = 170   # if a vehicle touches this, it vanishes


""" opponent vehicle's variables """
opponent_img        = pygame.image.load("atv.png")   # opponent/another bike on road
init_opponent_y     = 150                            # intial y position
opponent_xs         = [370, 400]                     # left right lane initial x positoin
init_opponent_scale = 20                             # initial size (%)
lane                = ''                             # indicates on which lane the vehicle is


""" to run for the first time """
bg             = next_img()            # for the first time we will add the first image
opponent_scale = init_opponent_scale
opponent_y     = init_opponent_y
new_opponent   = True                  # place new opponent
game_over      = False                 # game not over 


""" Speed data """
FONT             = pygame.font.Font('freesansbold.ttf', 40)
speedo_meter_pos = (350, 452)      # position pixel on dashboard                 
SPD_COLOR        = (0, 255, 0)     # text color


""" score  """
score       = 0
score_pos   = (365, 395)
SCORE_COLOR = (255, 255, 0)

# add engine sound
pygame.mixer.music.load("engine_sound.mp3")   
pygame.mixer.music.play()


while True:
    #check for events
    for event in pygame.event.get(): 

        if event.type == pygame.QUIT:  #quit button
            pygame.quit()
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:   # forward/UP key
                fps += 1

            if event.key == pygame.K_DOWN: # Brake/Down key
                if fps != 0:
                    fps -= 5
                if fps < 0:
                    fps = 0

            if event.key == pygame.K_LEFT: # turn left
                if bike_x > road_edge_left:
                    bike_x -= 10

            if event.key == pygame.K_RIGHT: # turn right
                if bike_x < roard_edge_right:
                    bike_x += 10

    """ ** if bike is moving forward """
    if fps != 0:
        # if bike is moving, change track image
        bg = next_img()
        if lane == 'left':
            opponent_x -= 1              # to keep that on lane
        
        if opponent_y >= vanish_point:   # if hits last edge
            # create new opponent
            opponent_y = init_opponent_y
            opponent_x = random.choice(opponent_xs)
            opponent_scale = init_opponent_scale
            new_opponent = True
            score += 1                   # update score

        opponent_y += 0.1
        opponent_scale += 1
        opponent = pygame.transform.scale(opponent_img, (opponent_scale, opponent_scale)) # resize car image

    """ ** place track and bike """
    track = pygame.image.load(bg)
    window.blit(track, (0, 0))        # load and place the track image

    """ ** show speed on dashboard """
    speed_text = FONT.render(str(fps), True, SPD_COLOR)
    window.blit(speed_text, speedo_meter_pos)

    """ ** score on dashboard """
    score_text = FONT.render(str(score), True, SCORE_COLOR)
    window.blit(score_text, score_pos)
    
    """ ** place opponent's bike """
    if new_opponent:
        opponent_x = random.choice(opponent_xs)
        new_opponent = False
        opponent = pygame.transform.scale(opponent_img, (opponent_scale, opponent_scale)) # resize car image
        if opponent_x == opponent_xs[0]:
            lane = 'left'
        else:
            lane = 'right'

    window.blit(opponent, (opponent_x, opponent_y)) # load opponent
    window.blit(bike, (bike_x, bike_y))             # load the bike image

    """ ** detect collision """
    if (not game_over) and (abs(opponent_x - bike_x) <= 120) and (abs(opponent_y - bike_y) <= 40):
        pygame.mixer.music.load("collision.mp3")   
        pygame.mixer.music.play()
        fps = 0
        game_over = True

    pygame.display.update()  # update the window
    clock.tick(fps)          # update the window/run loop by this speed