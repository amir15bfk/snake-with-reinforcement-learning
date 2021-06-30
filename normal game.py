import pygame ,sys,random

#general setup
pygame.init()
clock = pygame.time.Clock()

# Setting up the main window
screen_width = 1000
screen_height = 1000
pixel_size = 50
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('Snake')

# snake
class Snake():
    def __init__(self):
        self.snake_color= pygame.Color(0,206,0)
        self.snake_head_color= pygame.Color(0,100,0)
        self.size=1
        self.tail=[]
        self.snake_speed=[1,0]
        self.head = pygame.Rect(1,1,pixel_size-2,pixel_size-2)
    def eat(self,food):
        if abs(food.head.x-self.head.x)<5 and abs(food.head.y-self.head.y)<5:
            self.size+=1
            print(self.size)
            food.reset(self)
            self.tail.append(pygame.Rect(-500,-500,pixel_size-2,pixel_size-2))
    def move(self):
        
        if self.size>2:
            i = self.size-2
            while i>0:
                self.tail[i].x=self.tail[i-1].x
                self.tail[i].y=self.tail[i-1].y
                i-=1
        if self.size>1:
            self.tail[0].x=self.head.x
            self.tail[0].y=self.head.y
        self.head.x +=self.snake_speed[0]*pixel_size
        self.head.y +=self.snake_speed[1]*pixel_size

        if self.head.x<0 or self.head.y<0 or self.head.x>screen_width or self.head.y>screen_height or self.on_tail(self):
            self.lose()
    def lose(self):
        self.size = 1
        self.tail = []
        self.snake_speed = [1,0]
        self.head.x = 1
        self.head.y = 1
    def draw(self):
        for i in range(self.size-1):
            x=100+(i+1)*10
            if x<256:
                pygame.draw.rect(screen,pygame.Color(0,x,0),self.tail[i])
            else:
                pygame.draw.rect(screen,pygame.Color(0,255,0),self.tail[i])
        pygame.draw.rect(screen,self.snake_head_color,self.head)
    def on_tail(self,obj):
        f= False

        for i in self.tail:
            if abs(i.x - obj.head.x)<5 and abs(i.y - obj.head.y)<5:
                f= True
        return f


    
snake = Snake()

# food
class Food():
    def __init__(self,snake):
        self.food_color= pygame.Color(206,0,0)
        self.head = pygame.Rect(0,0,pixel_size-2,pixel_size-2)
        self.reset(snake)
    
    def reset(self,snake):
        x = random.randrange(screen_width/pixel_size)
        y = random.randrange(screen_width/pixel_size)
        self.head.x = x*pixel_size
        self.head.y = y*pixel_size
        if (abs(snake.head.x - self.head.x)<5 and abs(snake.head.y - self.head.y)<5) or snake.on_tail(self):
            self.reset(snake)
food = Food(snake)
# colors
bg_color= pygame.Color(12,12,12)






while True:
    #handling input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                if snake.snake_speed[1] != -1:
                    snake.snake_speed=[0,1]
            elif event.key == pygame.K_z:
                if snake.snake_speed[1] != 1:
                    snake.snake_speed=[0,-1]
            elif event.key == pygame.K_q:
                if snake.snake_speed[0] != 1:
                    snake.snake_speed=[-1,0]
            elif event.key == pygame.K_d:
                if snake.snake_speed[0] != -1:
                    snake.snake_speed=[1,0]
    snake.move()
    
    snake.eat(food)
    # Draw
    screen.fill(bg_color)
    snake.draw()
    
    pygame.draw.ellipse(screen,food.food_color,food.head)
    # Updating the window
    pygame.display.flip()
    clock.tick(4)