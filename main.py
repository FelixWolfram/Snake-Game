import pygame
from snake import Snake
from apple import Apple

class Game:
    # TODO:
    # 1. game_end = True when the snake hits one of its segments (the (x, y) of the head cannot be less than 40 pixels around a segment)
            # probably have to do the same as with checking for the wall -> simulate first, then if valid do the action
    # 2. maybe add a better GUI -> Score, Highscore, Restart Button, Sounds, better Images, ...
    # 3. optimize the code. -> some parts are redundant or could be written shorter
    # 4. add, that the snake does not start to move instantly when the game is started (for the first time)#
    # 5. apple still spawns on the snake

    def __init__(self):
        self.win_width = 800
        self.win_height = 800
        self.win = pygame.display.set_mode((self.win_width, self.win_height))
        self.fps = 100
        self.font = pygame.font.SysFont("comicsans", 100, True)

        self.field_size = 20
        self.cell_size = self.win_width / self.field_size
        self.end = False

        self.field_coords = [(i * self.win_width / self.field_size, j * self.win_height / self.field_size)
                              for i in range(self.field_size) for j in range(self.field_size)]
        self.next_turns = []
        self.max_next_turns = 3
        self.start_length = 3
        self.snake = Snake(200, 200, self.cell_size, self.fps, self.field_coords)
        for _ in range(self.start_length - 1):
            self.snake.add_segment()
        self.apple = Apple(self.snake.head, self.snake.segments, self.field_coords, self.cell_size, self.field_size)
        self.apple.generate_apple()
    
    
    def mainloop(self):
        while True:
            pygame.time.Clock().tick(self.fps)
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    global close_win
                    close_win = True
                    return
                elif event.type == pygame.KEYDOWN and self.end:
                    return
                
            if not self.end:
                for event in events:
                    if event.type == pygame.KEYDOWN and len(self.next_turns) < self.max_next_turns:   # store max 3 next turns
                        if event.key == pygame.K_LEFT and self.snake.head.direction != "right":
                            self.next_turns.append("left")
                        elif event.key == pygame.K_RIGHT and self.snake.head.direction != "left":
                            self.next_turns.append("right")
                        elif event.key == pygame.K_UP and self.snake.head.direction != "down":
                            self.next_turns.append("up")
                        elif event.key == pygame.K_DOWN and self.snake.head.direction != "up":
                            self.next_turns.append("down")

                if (self.snake.head.x, self.snake.head.y) == self.field_coords[self.apple.pos]:
                    self.snake.add_segment()
                    self.apple.generate_apple()

                self.end = self.snake.turn(self.next_turns) # turn returns TRUE if the snake hit itself and therefore the game should end
                if self.end:
                    continue

                # check whether it would be valid for the snake to move and move the snake if it is
                cur_direction = self.snake.head.direction
                add_direction = self.snake.speed if (cur_direction == "right" or cur_direction == "down") else (-self.snake.speed) # check whether you have to add or subtract pixels
                if not (0 <= self.snake.head.x + (add_direction if (cur_direction == "right" or cur_direction == "left") else 0) <= self.win_width - self.cell_size) or\
                   not (0 <= self.snake.head.y + (add_direction if (cur_direction == "up" or cur_direction == "down") else 0) <= self.win_height - self.cell_size):
                                                                        # simulate next movement of the snake -> if it hits the wall then game over
                    self.end = True # stops the movement and the control of the snake
                    continue

                self.snake.move()   # move snake if it didn't hit the wall

            self.redraw_window()


    def redraw_window(self):
        self.draw_background()
        
        self.apple.draw(self.win)
        self.snake.draw(self.win)

        if self.end:
            end_text = self.font.render("You lost!", True, (215, 30, 30))
            self.win.blit(end_text, (self.win_width / 2 - end_text.get_width() / 2, self.win_height / 2 - end_text.get_height() / 2))

        pygame.display.update()

    
    def draw_background(self):
        for i in range(len(self.field_coords)):
            if (i + i//self.field_size) % 2 == 0:
                pygame.draw.rect(self.win, (116, 196, 118), (self.field_coords[i][0], self.field_coords[i][1],
                                                             self.win_width / self.field_size, self.win_height / self.field_size))
            else:
                pygame.draw.rect(self.win, (65, 171, 93), (self.field_coords[i][0], self.field_coords[i][1],
                                                           self.win_width / self.field_size, self.win_height / self.field_size))


def main():
    pygame.display.set_caption("Snake Game")

    while not close_win:
        game = Game()
        game.mainloop()
    pygame.quit() # only closes the program, does not end the loop -> thats why we also need the return statement


pygame.init()
close_win = False
main()