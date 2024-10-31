from pygame import draw
from segment_info import Snakehead, Turncells, Snakesegments
from math import sqrt

class Snake:
    def __init__(self, x ,y, cell_size, fps, field_coords, win, snake_head_img):
        self.win = win
        self.segment_size = cell_size
        self.field_size = sqrt(len(field_coords))
        self.speed = (round(500 / fps) + (self.segment_size % round(500 / fps)))  # ensure speed is an integer multiple of segment size and stays similar with every fps-num
        self.head = Snakehead(x, y, "right")
        self.body = {}
        self.segments = []
        self.turn_cells = [] # stores the cells where the snake turns, direction of the turn and how many segements passed this cell
        self.field_coords = field_coords
        self.segment_color = (70, 180, 230)
        self.head_img = snake_head_img

    def move(self):
        all_segments = [self.head] + self.segments
        for segment in all_segments:
            if segment.direction == "right":
                segment.x += self.speed
            elif segment.direction == "left":
                segment.x -= self.speed
            elif segment.direction == "up":
                segment.y -= self.speed
            elif segment.direction == "down":
                segment.y += self.speed


    def turn(self, next_turns):
        # change direction of the snake if it aligns on a cell and store the new direction for the cell
        if (self.head.x, self.head.y) in self.field_coords:
            if next_turns: # if the head of the snake is on a cell
                direction = next_turns.pop(0)
                while self.head.direction == "right" and direction == "left" or\
                        self.head.direction == "left" and direction == "right" or\
                        self.head.direction == "up" and direction == "down" or\
                        self.head.direction == "down" and direction == "up" or\
                        self.head.direction == direction:     # if the new direction is valid -> no direction opposite to the current direction
                    if next_turns:
                        direction = next_turns.pop(0)   # pop new turns until a turn is valid
                    else:
                        direction = None    # if all the turns in the queue were invalid
                if direction is not None:       # all the directions in the queue were invalid
                    if len(self.segments) > 0:  # if the snake already has segments
                        self.turn_cells.append(Turncells((self.head.x, self.head.y), direction, self.get_round_corner(direction))) # store the direction of the turn and the direction of the segment
                    self.head.direction = direction
            
        # check for every segment whether it aligns with a "turn_cell" turn the segment if it does
        if self.segments is not None and self.turn_cells is not None:
            for segment in self.segments:
                for turn_cell in self.turn_cells:
                    if (segment.x, segment.y) == turn_cell.cell:     # if a snake segment reaches the cell where it should turn
                        segment.direction = turn_cell.direction # change the direction of the segment
                        turn_cell.segments_passed += 1      # mark how many cell turned for that cell
                        if turn_cell.segments_passed == len(self.segments):  # if all of the segments turned at that cells
                            self.turn_cells.remove(turn_cell)         # remove the turn_cell out of the list
                            turn_cell = None
                            return
        return self.check_for_collision() # at the end, check whether the snake hit itself


    def get_round_corner(self, direction):
        if self.head.direction == "up" and direction == "right" or self.head.direction == "left" and direction == "down":
            return "top left"
        elif self.head.direction == "right" and direction == "down" or self.head.direction == "up" and direction == "left":
            return "top right"
        elif self.head.direction == "down" and direction == "left"  or self.head.direction == "right" and direction == "up":
            return "bottom right"
        else: 
            return "bottom left"
        

    def check_for_collision(self):
        # check wheter the snake hit itself -> calculate the distance and not just look at the x and y-coordinates itself -> otherwise wrong output when snake turns
        if len(self.segments) > 3: # before the snake can't hit itself
            for segment in self.segments: # check which direction the snake goes and check whether the snake would hit a segment if it continues moving
                if (self.head.direction == "left" and 0 <= self.head.x - segment.x <= self.segment_size and abs(self.head.y - segment.y) == 0) or\
                    (self.head.direction == "right" and 0 <= segment.x - self.head.x <= self.segment_size and abs(self.head.y - segment.y) == 0) or\
                    (self.head.direction == "up" and 0 <= self.head.y - segment.y <= self.segment_size and abs(self.head.x - segment.x) == 0) or\
                    (self.head.direction == "down" and 0 <= segment.y - self.head.y <= self.segment_size and abs(self.head.x - segment.x) == 0):
                    return True
        return False


    # the turn_cell drawings can be written shorter for sure
    def draw(self, win):
        for segment in self.segments:
            pass
            draw.rect(win, self.segment_color, ((segment.x, segment.y), (self.segment_size, self.segment_size)))
        for turn_cell in self.turn_cells:
                # draw over the segments which are on the turn_cell and draw the backgroudn on there
            field_index = self.field_coords.index(turn_cell.cell)
            draw.rect(self.win, (116, 196, 118) if (field_index + (field_index // self.field_size)) % 2 == 0 else (65, 171, 93), # draw the background of the field
                      (self.field_coords[field_index][0], self.field_coords[field_index][1], self.segment_size, self.segment_size))
            self.draw_corner(win, turn_cell)
        draw.rect(win, (13, 146, 244), ((self.head.x, self.head.y),(self.segment_size, self.segment_size))) # draw the head of the snake

    
    def draw_corner(self, win, turn_cell):
        if turn_cell.round_corner == "top left":
            draw.rect(win, self.segment_color, ((turn_cell.cell[0], turn_cell.cell[1]+self.segment_size/2), (self.segment_size, self.segment_size/2)))
            draw.rect(win, self.segment_color, ((turn_cell.cell[0]+self.segment_size/2, turn_cell.cell[1]), (self.segment_size/2, self.segment_size)))
        elif turn_cell.round_corner == "top right":
            draw.rect(win, self.segment_color, ((turn_cell.cell[0], turn_cell.cell[1]+self.segment_size/2), (self.segment_size, self.segment_size/2)))
            draw.rect(win, self.segment_color, ((turn_cell.cell[0], turn_cell.cell[1]), (self.segment_size/2, self.segment_size)))
        elif turn_cell.round_corner == "bottom right":
            draw.rect(win, self.segment_color, ((turn_cell.cell[0], turn_cell.cell[1]), (self.segment_size/2, self.segment_size)))
            draw.rect(win, self.segment_color, ((turn_cell.cell[0], turn_cell.cell[1]), (self.segment_size, self.segment_size/2)))
        elif turn_cell.round_corner == "bottom left":
            draw.rect(win, self.segment_color, ((turn_cell.cell[0], turn_cell.cell[1]), (self.segment_size, self.segment_size/2)))
            draw.rect(win, self.segment_color, ((turn_cell.cell[0]+self.segment_size/2, turn_cell.cell[1]), (self.segment_size/2, self.segment_size)))
        draw.circle(win, self.segment_color, (turn_cell.cell[0] + self.segment_size/2, turn_cell.cell[1] + self.segment_size/2), self.segment_size/2)
    

    def add_segment(self):
        last_element = (self.segments[-1] if self.segments else self.head)
        if last_element.direction == "right" or last_element.direction == "left":
             self.segments.append(Snakesegments(last_element.x - self.segment_size if last_element.direction == "right" 
                                                else last_element.x + self.segment_size, last_element.y, last_element.direction))
        else:
             self.segments.append(Snakesegments(last_element.x, last_element.y - self.segment_size if last_element.direction == "down" 
                                                else last_element.y + self.segment_size, last_element.direction))
             