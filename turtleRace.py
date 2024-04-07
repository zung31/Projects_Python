import turtle
import time
import random

#define size screen and colors
WIDTH, HEIGHT = 500, 500
COLORS = ['red', 'blue', 'green', 'orange', 'purple', 'pink', 'yellow', 'brown', 'black', 'cyan']

def get_number_of_racers():
    racers = 0;
    # check number is numeric and in range 2 - 10
    while True:
        racers = input("Enter the number of racers (2 - 10): ")
        if racers.isdigit():
            racers = int(racers)
        else:
            print("Input is not numeric... Try again!")
            continue # go back to start of loop

        if 2 <= racers <= 10:
            return racers
        else:
            print("Number not in range 2 - 10. Try again!")

def init_turtle():
    screen = turtle.Screen() # create a screen
    screen.setup(WIDTH, HEIGHT) # set screen 
    screen.title("Turtle Racing Game") # set title of the window
    
def create_turtles(colors):
    turtles =[];
    # tưởng tượng nếu để 4 rùa cách đều nhau như chia một sợi dây làm 5 phần và rùa bắt đầu từ phần index 1 (thứ 2)
    spacingx = WIDTH // (len(colors) + 1) # spacing between turtles
    for i, color in enumerate(colors):
        racer = turtle.Turtle()
        racer.color(color)
        racer.shape('turtle')
        racer.left(90)
        turtles.append(racer)

        racer.penup()
        # rùa sẽ từ giữa màn hình, quay left và đi về góc màn hình bên trái + spacingx tùy theo index
        racer.setpos(-WIDTH//2 + (i+1)*spacingx, -HEIGHT//2 +20) # set position of turtle
        racer.pendown()

    return turtles

def race(colors):
    turtles = create_turtles(colors) # create turtles and race when it ready

    while True:
        for racer in turtles:
            distance = random.randrange(1, 20) # random distance
            racer.forward(distance)

            x, y = racer.pos()
            if y >= HEIGHT // 2 - 10:
                return colors[turtles.index(racer)] # Return winner's color when reach bottom of
            # index turtle winner = index color's that turtle

# Main game function
racers = get_number_of_racers()
init_turtle()
random.shuffle(COLORS) # shuffle colors list
colors = COLORS[:racers] # array of colors for the number of racers
winner =  race(colors)
print(f"The winner is {winner} color!")
time.sleep(5) # delay 5 seconds before close window