from tkinter import * 
import random 

GAME_WIDTH = 1000
GAME_HEIGHT = 700
SPEED = 50
SPACE_SIZE = 50
BODY_PARTS = 3 
SNAKE_COLOR = "#00FF00"
FOOD_COLOR = "#FF0000"
BACKGROUND_COLOR = "#000000"

class Snake: # create snake
    def __init__(self): 
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for _ in range(0, BODY_PARTS):
            self.coordinates.append([0,0]) # start top left 
        
        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill = SNAKE_COLOR, tag="snake")
            self.squares.append(square)

class Food:
    def __init__(self):
        x =random.randint(0,(GAME_WIDTH // SPACE_SIZE) - 1) * SPACE_SIZE # random number between 0,14
        y = random.randint(0,(GAME_HEIGHT // SPACE_SIZE) - 1) * SPACE_SIZE # random number between 0,14

        self.coordinates = [x,y]

        canvas.create_oval(x,y,x + SPACE_SIZE, y + SPACE_SIZE, fill= FOOD_COLOR, tag="food")


def next_turn(snake, food):
    x,y = snake.coordinates[0] #head of the snake
    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    snake.coordinates.insert(0, (x,y))
    square = canvas.create_rectangle(x,y,x + SPACE_SIZE, y + SPACE_SIZE, fill = SNAKE_COLOR)
    snake.squares.insert(0, square)
    
    if x == food.coordinates[0] and y == food.coordinates[1]: #overlap
        global score
        score += 1
        label.config(text="Score:{}".format(score))

        #Delete and create food 
        canvas.delete("food")
        food = Food()
    else:#increase length only if food object is eaten 
        # delete tail end 
        del snake.coordinates[-1] 
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]
    #control collisions
    if check_collisions(snake):
        game_over()
    else:
        window.after(SPEED, next_turn, snake, food)


def change_direction(new_direction):
    global direction #old direction
    if new_direction == 'left':
        if direction != 'right': # new direction
            direction = new_direction
    if new_direction == 'right':
        if direction != 'left': # new direction
            direction = new_direction
    if new_direction == 'up':
        if direction != 'down': # new direction
            direction = new_direction
    if new_direction == 'down':
        if direction != 'up': # new direction
            direction = new_direction


def check_collisions(snake): # create borders(T or F) to stop game
    x,y = snake.coordinates[0]
    if x < 0 or x >= GAME_WIDTH:
        return True 
    elif y < 0 or y >= GAME_HEIGHT:
        return True 
    
    #check body collisions
    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True 
    return False 

def game_over():
    canvas.delete(ALL) 
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2,font=('consolas', 70), text="GAME OVER", fill="red", tag="GAMEOVER")


window = Tk()
window.title("Snake Game")
window.resizable(False, False)


score = 0
direction = 'down'

label = Label(window, text = "score:{}".format(score), font = ('consolas', 40))
label.pack()

canvas = Canvas(window, bg= BACKGROUND_COLOR, height = GAME_HEIGHT, width = GAME_WIDTH)
canvas.pack()

window.update()

window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width/2) - (window_width/2))
y = int((screen_height/2) - (window_height/2))

window.geometry(f"{window_width}x{window_height}+{x}+{y}")

#control snake movements 
window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))
#call
snake = Snake()
food = Food()
next_turn(snake, food)
window.mainloop()