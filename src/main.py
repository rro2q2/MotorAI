import search as sr
#import nms
import time
import math
import pygame
from car_model import Car

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
DARKGREEN = (0, 100, 0)
RED = (255, 0, 0)
DARKRED = (139, 0, 0)
BLUE = (0, 0, 255)
BROWN = (101, 67, 33)
GREY = (211, 211, 211)
YELLOW = (255, 255, 0)

# This sets the WIDTH and HEIGHT of each grid location
WIDTH = 100
HEIGHT = 75

# This sets the margin between each cell
MARGIN = 1

# Set the HEIGHT and WIDTH of the screen
WINDOW_SIZE = [1400, 760]
screen = pygame.display.set_mode(WINDOW_SIZE)

# Set title of screen
pygame.display.set_caption("Self-Driving Car Simulator")

# Goal coordinates
goal_coord = {
    "Bob": (4, 8),   # Blue
    "Joe": (5, 1),   # Red
    "Kris": (1, 1),  # Green
    "Mason": (1, 7)  # Orange
}

# Building coordinates
bldg_coord = [(1, 2), (1, 3), (1, 5), (1, 6), (1, 8), (2, 1), (2, 8), (3, 1), (3, 2), (3, 3), (3, 5), (3, 6), (3, 7),
              (3, 8), (4, 1), (5, 2), (5, 3), (5, 5), (5, 6), (5, 7), (5, 8), (7, 1), (7, 2), (7, 3), (7, 5), (7, 6),
              (7, 7), (7, 8), (9, 1), (9, 2), (9, 3), (9, 6), (9, 7), (9, 8)]

# Stop coordinates
stop_coord = [(0, 2), (0, 5), (2, 9), (3, 0), (4, 3), (4, 6), (5, 4), (6, 3), (8, 1), (8, 5), (8, 8), (9, 4)]


# Initializes each element on the grid as an empty node
# Returns a 2d list of empty nodes
def initGrid(node, image_list, dim: tuple):
    k = [[' ' for i in range(dim[0])] for j in range(dim[1])]
    length = 0
    for i in range(dim[0]):
        for j in range(dim[1]):
            color = GREY
            if (i, j) == node.pos:
                k[i][j] = node.value
            if (i, j) in bldg_coord:
                k[i][j] = 'X'
                rect = pygame.draw.rect(screen, color, [(WIDTH) * j,
                                                        (HEIGHT) * i, WIDTH, HEIGHT])
                displayImage(rect, '../assets/' + image_list[0])
            elif (i, j) in stop_coord:
                k[i][j] = 'S'
                rect = pygame.draw.rect(screen, color, [(WIDTH) * j,
                                                        (HEIGHT) * i, WIDTH, HEIGHT])
                displayImage(rect, '../assets/' + image_list[1])
            elif (i, j) == goal_coord["Bob"]:
                #k[i][j] = 'G'
                rect = pygame.draw.rect(screen, color, [(WIDTH) * j,
                                                        (HEIGHT) * i, WIDTH, HEIGHT])
                displayImage(rect, '../assets/' + image_list[2])
            elif (i, j) == goal_coord["Joe"]:
                #k[i][j] = 'G'
                rect = pygame.draw.rect(screen, color, [(WIDTH) * j,
                                                        (HEIGHT) * i, WIDTH, HEIGHT])
                displayImage(rect, '../assets/' + image_list[3])
            elif (i, j) == goal_coord["Kris"]:
                #k[i][j] = 'G'
                rect = pygame.draw.rect(screen, color, [(WIDTH) * j,
                                                        (HEIGHT) * i, WIDTH, HEIGHT])
                displayImage(rect, '../assets/' + image_list[4])
            elif (i, j) == goal_coord["Mason"]:
                k[i][j] = 'G'
                rect = pygame.draw.rect(screen, color, [(WIDTH) * j,
                                                        (HEIGHT) * i, WIDTH, HEIGHT])
                displayImage(rect, '../assets/' + image_list[5])
            else:
                rect = pygame.draw.rect(screen, color, [(WIDTH) * j,
                                                        (HEIGHT) * i, WIDTH, HEIGHT])
        length += (rect.width)
    return k, (length)

# Loads an image and displays it on the grid
# Shows the images displayed on different grid coordinates
def displayImage(rect, file_name):
    image = pygame.image.load(file_name).convert()  # or .convert_alpha()
    # Create a rect with the size of the image.
    im_rect = image.get_rect(center=(rect.center))
    screen.blit(image, im_rect)

# Initialized the menu display of pedestrian
# Diplays the pedestrian image as well as clock time
def initPedDisplay(length, file_name):
    color = GREY
    pygame.draw.rect(screen, color, [length+MARGIN, MARGIN-1, WINDOW_SIZE[0] - length-1, ((WINDOW_SIZE[1] / 2) - 1)])
    # Display ped menu of friends houses
    displayPed(length, file_name)

# Displays the labels/titles of the pedestrian container
# Shows the image of the pedestrian at crosswalk
def displayPed(length, file_name):
    ped_offset = 20
    # Title
    font = pygame.font.Font('freesansbold.ttf', 32)
    text = font.render('Pedestrian Display', True, BLACK)
    temp_length = length + ((WINDOW_SIZE[0] - length) / 2)
    text_rect = text.get_rect(center=(temp_length, ped_offset))
    screen.blit(text, text_rect)

# Initialized the menu display of friends' houses
# Displays the menu container, and keys of goal nodes (houses)
def initMenu(length, file_name):
    color = GREY
    pygame.draw.rect(screen, color, [length+MARGIN, (WINDOW_SIZE[1] / 2) , WINDOW_SIZE[0] - length,
                                     ((WINDOW_SIZE[1] / 2) - 10)])
    # Display menu key of friends houses
    displayMenu(length, file_name)

# Loads a set of images within the menu container
# Displays the menu items of friends' houses
def displayMenu(length, file_name):
    menuLb_list = ["- Bob's House", "- Joe's House", "- Kris's House", "- Mason's House"]
    offset = 0
    menu_offset = 400
    font = pygame.font.Font('freesansbold.ttf', 32)
    text = font.render('Menu Display', True, BLACK)
    temp_length = length + ((WINDOW_SIZE[0] - length) / 2)
    text_rect = text.get_rect(center=(temp_length, menu_offset))
    screen.blit(text, text_rect)
    for i in range(4):
        offset += 80
        image = pygame.image.load('../assets/'+file_name[i+2]).convert()  # or .convert_alpha()
        # Create a rect with the size of the image.
        im_rect = image.get_rect(center=(length+75, (WINDOW_SIZE[1] / 2) + offset))
        screen.blit(image, im_rect)
        # Add text to houses
        font = pygame.font.Font('freesansbold.ttf', 28 )
        text = font.render(menuLb_list[i], True, BLACK)
        temp_length = length + ((WINDOW_SIZE[0] - length) / 2)
        text_rect = text.get_rect(center=(temp_length + 40, menu_offset + (offset - 15)))
        screen.blit(text, text_rect)



def gamePlay(car, index, path, action, done):
    column = car.pos[0] // (WIDTH)
    row = car.pos[1] // (HEIGHT)
    temp = None
    stop = None
    if len(path) > 0:
        if (row, column) == path[0].pos:
            if (row, column) == goal_coord["Mason"]:
                done = True
                print("Success!")
                return done
            car.speed = 0
            if path[0].value == 'S':
                stop = path[0].value
            # implement turns
            if len(action) > 0:
                temp = action[0]
                action.pop(0)
            path.pop(0)
            index += 1
    return temp, stop


def main():
    start_pos = (9, 5)
    grid_size = (10, 10)
    node = sr.Node(start_pos, 0, 0, 0, 'C', None, None)
    # Image List
    image_list = ['grey_house.jpeg', 'stop_sign.png', 'blue_house.png', 'red_house.png', 'green_house.png',
                  'orange_house.png']

    # Initialize pygame
    pygame.init()
    # Loop until the user clicks the close button.
    done = False
    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()
    # Set the screen background
    screen.fill(BLACK)
    # Initialize game displays
    grid, grid_length = initGrid(node, image_list, grid_size)
    #grid[4][8] = 'G'
    initPedDisplay(grid_length, image_list)
    initMenu(grid_length, image_list)

    # Pos indices are switched because x is read going down
    start_x = (start_pos[0] * HEIGHT) + 37
    start_y = (start_pos[1] * WIDTH) + 50

    car = Car(screen, start_y, start_x, 0)
    #print('This is car pos', car.pos)
    car.constant_speed = True

    # where the car will start
    #pygame.draw.rect(screen, RED, (400, 300, car.length, car.width))

    # Run Algorithm first
    startTime = time.time()
    res = sr.aStarSearch(node, grid)
    # Path to Goal function
    path = sr.pathToGoal(res)
    actions_list = []
    endTime = time.time()

    #print("TIME:", endTime - startTime)
    for states in path:
        print(states.pos, states.action)
        if states.value == 'S':
            #time.sleep(3)
            print("STOP")

    for i in range(1, len(path)):
        actions_list.append(path[i].action)
    print(actions_list)
    index = 0

    # -------- Main Program Loop -----------
    while not done:
        for event in pygame.event.get():  # User did something
            if event.type == pygame.QUIT:  # If user clicked close
                done = True  # Flag that we are done so we exit this loop

        action, stop = gamePlay(car, index, path, actions_list, done)

        # Update grid every time car moves
        initGrid(node, image_list, grid_size)

        rate = 10
        car.update(1 / rate, action, stop)

        # Limit to 60 frames per second
        clock.tick(60)
        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

    # Be IDLE friendly. If you forget this line, the program will 'hang'
    # on exit.
    pygame.quit()
    return

if __name__ == '__main__':
    main()
