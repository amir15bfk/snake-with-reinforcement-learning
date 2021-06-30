import pygame ,sys,random,math

#general setup


# snake
class Snake():
    def __init__(self,pixel_size):
        self.snake_color= pygame.Color(0,206,0)
        self.snake_head_color= pygame.Color(0,100,0)
        self.size=1
        self.tail=[]
        self.history= []
        self.state =  [0,0,0,1]
        self.frame_itiration=0
        self.head = pygame.Rect(1,1,pixel_size-2,pixel_size-2)
    def eat(self,food,pixel_size,screen_width):
        if abs(food.head.x-self.head.x)<5 and abs(food.head.y-self.head.y)<5:
            self.size+=1
            self.history=[]
            food.reset(self,pixel_size,screen_width)
            self.frame_itiration=0
            self.tail.append(pygame.Rect(-500,-500,pixel_size-2,pixel_size-2))
            return 10
        else:
            return 0
    def move(self,action,pixel_size,screen_width,screen_height,food):

        
        if self.size>2:
            i = self.size-2
            while i>0:
                self.tail[i].x=self.tail[i-1].x
                self.tail[i].y=self.tail[i-1].y
                i-=1
        if self.size>1:
            self.tail[0].x=self.head.x
            self.tail[0].y=self.head.y
        if self.state==action:
            reward = 0
        else:
            reward = -0.1
        #test action
        if (action[0] and not (self.state[1])) or (action[1] and not (self.state[0]))or (action[2] and not (self.state[3]))or (action[3] and not (self.state[3])):
            self.state= action

        #move
        if self.state[0]:
            #upp
            self.head.y +=-1*pixel_size
        elif self.state[1]:
            #down
            self.head.y +=1*pixel_size
        elif self.state[2]:
            #left
            self.head.x +=-1*pixel_size
        elif self.state[3]:
            #right
            self.head.x +=1*pixel_size
        
        
        
        
         
        game_over = False
        score = self.size
        if  self.is_lose(screen_width,screen_height):
            self.lose()
            reward = -10
            game_over = True
        self.history.append([self.head.x,self.head.y])
        reward += self.eat(food,pixel_size,screen_width)
        return reward , game_over , score
    def is_lose(self,screen_width,screen_height):
        return self.head.x<0 or self.head.y<0 or self.head.x>screen_width or self.head.y>screen_height or self.on_tail(self) or ([self.head.x,self.head.y] in self.history)or self.frame_itiration>100*self.size
    def lose(self):
        self.history=[]
        self.size = 1
        self.tail = []
        self.state =  [0,0,0,1]
        self.head.x = 1
        self.head.y = 1
        self.frame_itiration=0
    def draw(self,screen):
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


    


# food
class Food:
    def __init__(self,snake,pixel_size,screen_width):
        self.food_color= pygame.Color(206,0,0)
        self.head = pygame.Rect(0,0,pixel_size-2,pixel_size-2)
        self.reset(snake,pixel_size,screen_width)
    
    def reset(self,snake,pixel_size,screen_width):
        x = random.randint(0, (screen_width-pixel_size )//pixel_size )
        y = random.randint(0, (screen_width-pixel_size )//pixel_size )
        self.head.x = x*pixel_size
        self.head.y = y*pixel_size
        if (abs(snake.head.x - self.head.x)<5 and abs(snake.head.y - self.head.y)<5) or snake.on_tail(self):
            self.reset(snake,pixel_size,screen_width)
# colors

class Game:
    def __init__(self):  
        pygame.init()
        self.clock = pygame.time.Clock()

        self.fast = True

        # Setting up the main window
        self.screen_width = 1000
        self.screen_height = 1000
        self.pixel_size = 50

        self.screen = pygame.display.set_mode((self.screen_width,self.screen_height))
        pygame.display.set_caption('Snake')
        self.snake = Snake(self.pixel_size)
        self.food = Food(self.snake,self.pixel_size,self.screen_width)
        self.bg_color= pygame.Color(12,12,12)
    def play_round(self,action,number_of_games):
        #handling input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    self.fast = not self.fast
        self.snake.frame_itiration+=1
        reward ,game_over , score =  self.snake.move(action,self.pixel_size,self.screen_width,self.screen_height,self.food)

        # Draw
        self.screen.fill(self.bg_color)
        self.snake.draw(self.screen)

        pygame.draw.ellipse(self.screen,self.food.food_color,self.food.head)
        # Updating the window
        pygame.display.flip()
        if self.fast:
            self.clock.tick(10000)
        else:
            self.clock.tick(30)
        return reward,game_over , score-1

    
    
# game_1 =Game()   

# while True:
#     action =[0,0,1,0]
    
#     if game_1.snake.frame_itiration>10:
#         action =[0,1,0,0]
#     reward ,game_over , score = game_1.play_round(action)

    