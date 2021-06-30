import random
from typing import final
import torch
import numpy as np
from game import Game
from collections import deque
from model import Linear_QNet ,QTrainer
from ploter import plot
MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.0005

class Agent:

    def __init__(self) :
        self.number_of_games = 0
        self.epsilon = 0 # randomness ??
        self.gamma = 0.9 # discount rate ??
        self.memory = deque(maxlen=MAX_MEMORY) # popleft() if is full
        self.model = Linear_QNet(12,256,4) 
        self.trainer = QTrainer(self.model,LR,self.gamma) 

    def get_state(self,game):
        #self.head.x<0 or self.head.y<0 or self.head.x>screen_width or self.head.y>screen_height or self.on_tail(self)
        # left
        game.snake.head.x+=-1*game.pixel_size
        if game.snake.is_lose(game.screen_width,game.screen_height):
            l_danger=True
        else:
            l_danger=False
        game.snake.head.x+=game.pixel_size
        
        # right
        game.snake.head.x+=game.pixel_size
        if game.snake.is_lose(game.screen_width,game.screen_height):
            r_danger=True
        else:
            r_danger=False
        game.snake.head.x+=-1*game.pixel_size

        # up
        game.snake.head.y+=-1*game.pixel_size
        if game.snake.is_lose(game.screen_width,game.screen_height):
            u_danger=True
        else:
            u_danger=False
        game.snake.head.y+=game.pixel_size
        
        # down
        game.snake.head.y+=game.pixel_size
        if game.snake.is_lose(game.screen_width,game.screen_height):
            d_danger=True
        else:
            d_danger=False
        game.snake.head.y+=-1*game.pixel_size

        state =[
            l_danger,
            r_danger,
            u_danger,
            d_danger,
            game.snake.state[0],
            game.snake.state[1],
            game.snake.state[2],
            game.snake.state[3],
            game.food.head.x<game.snake.head.x,
            game.food.head.x>game.snake.head.x,
            game.food.head.y<game.snake.head.y,
            game.food.head.y>game.snake.head.y
        ]
        return np.array(state,dtype=int)

    def remember(self,state,action,reward,next_state,game_over):
        self.memory.append((state,action,reward,next_state,game_over))

    def train_long_memory(self):
        if len(self.memory)>BATCH_SIZE:
            mini_sample = random.sample(self.memory,BATCH_SIZE)
        else:
            mini_sample = self.memory
        
        states,actions,rewards,next_states,game_overs = zip(*mini_sample)
        self.trainer.train_step(states,actions,rewards,next_states,game_overs)
    
    def train_short_memory(self,state,action,reward,next_state,game_over):
        self.trainer.train_step(state,action,reward,next_state,game_over)

    def get_move(self,state):
        # do a random move
        self.epsilon = 80 - self.number_of_games
        final_move = [0,0,0,0]

        if random.randint(0,200) < self.epsilon:
            move = random.randint(0,3)
            final_move[move]=1
        else:
            state0 = torch.tensor(state,dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move]=1
        return final_move
def train():
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    agent = Agent()
    game = Game()
    while True:
        # get corr state
        state = agent.get_state(game)

        # get the move
        action = agent.get_move(state)
        
        # play the move
        reward , game_over , score = game.play_round(action,agent.number_of_games)

        # get the new state
        new_state = agent.get_state(game)

        # train short memory
        agent.train_short_memory(state,action,reward,new_state,game_over)

        # remember
        agent.remember(state,action,reward,new_state,game_over)

        if game_over:
            agent.number_of_games += 1
            # train long memory
            agent.train_long_memory()

            if score > record :
                record = score
                agent.model.save('model_v9.pth')
            # TODO : plot
            plot_scores.append(score)
            total_score+= score
            mean_score = total_score/ agent.number_of_games

            print('Game:',agent.number_of_games,'Score:',score,'Record:',record,'Mean:',mean_score)
            
            # plot_mean_scores.append(mean_score)
            # plot(plot_scores,plot_mean_scores)





if __name__=='__main__' :
    train()