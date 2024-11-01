import pygame
from snake import Snake
from apple import Apple

class Game:
    def __init__(self):
        self.bar_size = 80 # bar which displays the score, highscore, ...      
        self.wall_size = 20 # size of the wall around the board

        self.board_width = 800
        self.win_width = 800 + self.wall_size * 2
        self.win_height = 800 + self.bar_size + self.wall_size * 2

        self.win = pygame.display.set_mode((self.win_width, self.win_height))
        self.fps = 100
        self.font_game_over = pygame.font.SysFont("courier new", 72, True)
        self.font_end_score = pygame.font.SysFont("courier new", 66, True)
        self.font_score = pygame.font.SysFont("courier new", 33, True)
        self.font_press_key = pygame.font.SysFont("courier new", 36, True)

        self.field_size = 20
        self.cell_size = self.board_width / self.field_size
        self.game_start = True
        self.end = False 
        self.score = 0
        self.field_coords = [(i * self.board_width / self.field_size + self.wall_size, (j * self.board_width / self.field_size) + self.bar_size + self.wall_size)
                              for i in range(self.field_size) for j in range(self.field_size)]
        self.next_turns = []
        self.max_next_turns = 3
        self.start_length = 3
        self.snake = Snake(self.win, self.cell_size * 5 + self.wall_size, self.cell_size * 9 + self.bar_size + self.wall_size, self.cell_size,
                           self.fps, self.field_coords)
        for _ in range(self.start_length - 1):
            self.snake.add_segment()
        self.apple = Apple(self.snake.head, self.snake.segments, self.field_coords, self.cell_size, self.field_size)
        self.apple.generate_apple()
        self.colors = {
            "background": (25, 140, 50),
            "field": [(116, 196, 118), (65, 171, 93)],
            "bar": (10, 120, 10),
            "end_window": (33, 150, 204),
            "hover_color": (20, 120, 200),
            "text": (200, 200, 200),
            "white": (255, 255, 255)
        }
        self.rect_width = round(self.win_width * 0.75)
        self.rect_height = round(self.win_height * 0.32)
        small_rect_height = 90
        offset_top = small_rect_height + 10
        offset_bottom = self.rect_height + 10
        self.text_press_key = self.font_press_key.render(f"Press any key to play again" , True, self.colors["text"])
        self.main_end_window = pygame.Rect((self.win_width / 2 - self.rect_width / 2, self.win_height / 2 - self.rect_height / 2, self.rect_width, self.rect_height))
        self.top_end_window = pygame.Rect((self.main_end_window.topleft[0], self.main_end_window.topleft[1] - offset_top, self.rect_width, small_rect_height))
        self.bottom_end_window = pygame.Rect((self.main_end_window.topleft[0], self.main_end_window.topleft[1] + offset_bottom, self.rect_width, small_rect_height))
        self.bottom_window_col = self.colors["end_window"]
    
    
    def mainloop(self):
         while True:
            pygame.time.Clock().tick(self.fps)
            events = pygame.event.get()
            for event in events:
                pos = pygame.mouse.get_pos()
                if event.type == pygame.QUIT:
                    global close_win
                    close_win = True
                    return
                elif event.type == pygame.KEYDOWN and self.game_start:
                    self.game_start = False
                elif (event.type == pygame.MOUSEBUTTONDOWN and self.end):
                    if self.bottom_end_window.collidepoint(pos):
                        return
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and self.end:
                        return
                if self.bottom_end_window.collidepoint(pos) and self.end:
                    self.bottom_window_col = self.colors["hover_color"]
                    pygame.mouse.set_cursor(*pygame.cursors.tri_left)   # * -> unpacks the tuple given as a parameter
                else:
                    self.bottom_window_col = self.colors["end_window"]
                    pygame.mouse.set_cursor(*pygame.cursors.arrow)
                    
                
            if not self.end and not self.game_start:
                for event in events:
                    if event.type == pygame.KEYDOWN and len(self.next_turns) < self.max_next_turns:   # store max 3 next turns
                        if (event.key == pygame.K_LEFT or event.key == pygame.K_a) and self.snake.head.direction != "right":
                            self.next_turns.append("left")
                        elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and self.snake.head.direction != "left":
                            self.next_turns.append("right")
                        elif (event.key == pygame.K_UP or event.key == pygame.K_w) and self.snake.head.direction != "down":
                            self.next_turns.append("up")
                        elif (event.key == pygame.K_DOWN or event.key == pygame.K_s) and self.snake.head.direction != "up":
                            self.next_turns.append("down")

                if (self.snake.head.x, self.snake.head.y) == self.field_coords[self.apple.pos]:
                    global highscore

                    self.snake.add_segment()
                    self.score += 1
                    if self.score > highscore:
                        highscore = self.score
                    self.apple.generate_apple()

                self.end = self.snake.turn(self.next_turns) # turn returns TRUE if the snake hit itself and therefore the game should end
                if self.end:
                    continue

                # check whether it would be valid for the snake to move and move the snake if it is
                cur_direction = self.snake.head.direction
                add_direction = self.snake.speed if (cur_direction == "right" or cur_direction == "down") else (-self.snake.speed) # check whether you have to add or subtract pixels
                if not (0 + self.wall_size <= self.snake.head.x + (add_direction if (cur_direction == "right" or cur_direction == "left") else 0) <= self.board_width + self.wall_size - self.cell_size) or\
                   not (0 + self.wall_size + self.bar_size <= self.snake.head.y + (add_direction if (cur_direction == "up" or cur_direction == "down") else 0) <= self.board_width + self.wall_size + self.bar_size - self.cell_size):
                                                                        # simulate next movement of the snake -> if it hits the wall then game over
                    self.end = True # stops the movement and the control of the snake
                    continue
                self.snake.move()   # move snake if it didn't hit the wall
            self.redraw_window()


    def redraw_window(self):
        self.win.fill(self.colors["background"])
        self.draw_field()
        self.draw_bar()
        self.draw_gui()

        self.apple.draw(self.win)
        self.snake.draw(self.win)

        if self.end:
            self.draw_end()
        pygame.display.update()


    def draw_gui(self):
        score_text = self.font_score.render("Score: " + str(self.score), False, self.colors["white"])
        highscore_text = self.font_score.render("Highscore: " + str(highscore), False, self.colors["white"])
        self.win.blit(score_text, (self.wall_size, self.bar_size / 2 - score_text.get_height() / 2))
        self.win.blit(highscore_text, (self.wall_size + score_text.get_width() + 60, self.bar_size / 2 - highscore_text.get_height() / 2))
        pass
    

    def draw_field(self):
        for i in range(len(self.field_coords)):
            if (i + i//self.field_size) % 2 == 0:
                pygame.draw.rect(self.win, self.colors["field"][0], (self.field_coords[i][0], self.field_coords[i][1], self.cell_size, self.cell_size))
            else:
                pygame.draw.rect(self.win, self.colors["field"][1], (self.field_coords[i][0], self.field_coords[i][1], self.cell_size, self.cell_size))


    def draw_bar(self):
        pygame.draw.rect(self.win, self.colors["bar"], (0, 0, self.win_width, self.bar_size))


    def draw_end(self):
        text_game_over = self.font_game_over.render(f"Game Over!", True, self.colors["text"])
        score_text_end = self.font_end_score.render(f"Score: {self.score}", True, self.colors["text"])
        highscore_text_end = self.font_end_score.render(f"Highscore: {highscore}", True, self.colors["text"])

        pygame.draw.rect(self.win, self.colors["end_window"], self.top_end_window, border_radius=40)
        pygame.draw.rect(self.win, self.colors["end_window"], self.main_end_window, border_radius=40)
        pygame.draw.rect(self.win, self.bottom_window_col, self.bottom_end_window, border_radius=40)

        game_over_rect = text_game_over.get_rect()
        game_over_rect.center = self.top_end_window.center
        self.win.blit(text_game_over, game_over_rect)
        self.win.blit(score_text_end, (self.main_end_window.topleft[0] + self.rect_width / 2 - score_text_end.get_width() / 2, self.main_end_window.topright[1] + self.rect_height / 3 - score_text_end.get_height() / 2))
        self.win.blit(highscore_text_end, (self.main_end_window.topleft[0] + self.rect_width / 2 - highscore_text_end.get_width() / 2, self.main_end_window.topright[1] + self.rect_height / 3 * 2 - highscore_text_end.get_height() / 2))
        text_press_rect = self.text_press_key.get_rect()
        text_press_rect.center = self.bottom_end_window.center
        self.win.blit(self.text_press_key, text_press_rect)


def main():
    pygame.display.set_caption("Snake Game")
    
    global highscore
    highscore = 0

    while not close_win:
        game = Game()
        game.mainloop()
    pygame.quit() # only closes the program, does not end the loop -> thats why we also need the return statement


pygame.init()
close_win = False
main()
