from pygame import draw
from segment_info import Snakehead, Turncells, Snakesegments

class Snake:
    def __init__(self, x ,y, cell_size, fps, field_coords):
        self.segment_size = cell_size
        self.speed = fps / 20
        self.head = Snakehead(x, y, "right")
        self.body = {}
        self.segments = []
        self.turn_cells = [] # stores the cells where the snake turns, direction of the turn and how many segements passed this cell
        self.field_coords = field_coords
    

    def move(self):
        if self.head.direction == "right":
            self.head.x += self.speed
        elif self.head.direction == "left":
            self.head.x -= self.speed
        elif self.head.direction == "up":
            self.head.y -= self.speed
        elif self.head.direction == "down":
            self.head.y += self.speed

        for segment in self.segments:
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
            self.head.just_turned = False

            if next_turns: # if the head of the snake is on a cell
                direction = next_turns.pop(0)
                while (self.head.direction == "right" and direction == "left" or\
                        self.head.direction == "left" and direction == "right" or\
                        self.head.direction == "up" and direction == "down" or\
                        self.head.direction == "down" and direction == "up"):     # if the new direction is valid -> no direction opposite to the current direction
                    if next_turns:
                        direction = next_turns.pop(0)   # pop new turns until a turn is valid
                    else:
                        direction = None    # if all the turns in the queue were invalid
                if direction is not None:       # all the directions in the queue were invalid
                    self.head.direction = direction
                    self.head.just_turned = True
                    if len(self.segments) > 0:  # if the snake already has segments
                        self.turn_cells.append(Turncells((self.head.x, self.head.y), self.head.direction)) # store the direction of the turn and the direction of the segment
        
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


    def check_for_collision(self):
        # check wheter the snake hit itself -> calculate the distance and not just look at the x and y-coordinates itself -> otherwise wrong output when snake turns
        if len(self.segments) > 3: # before the snake can't hit itself
            for segment in self.segments: # check which direction the snake goes and check whether the snake would hit a segment if it continues moving
                if (self.head.direction == "left" and self.head.x - segment.x == self.segment_size and abs(self.head.y - segment.y) == 0) or\
                    (self.head.direction == "right" and segment.x - self.head.x == self.segment_size and abs(self.head.y - segment.y) == 0) or\
                    (self.head.direction == "up" and self.head.y - segment.y == self.segment_size and abs(self.head.x - segment.x) == 0) or\
                    (self.head.direction == "down" and segment.y - self.head.y == self.segment_size and abs(self.head.x - segment.x) == 0):
                    return True
        return False


    def draw(self, win):
        draw.rect(win, (13, 146, 244), ((self.head.x, self.head.y),(self.segment_size, self.segment_size))) # draw the head of the snake
        for segment in self.segments:
            draw.rect(win, (119, 205, 255), ((segment.x, segment.y), (self.segment_size, self.segment_size)))

    
    def add_segment(self):
        last_element = (self.segments[-1] if self.segments else self.head)
        if last_element.direction == "right" or last_element.direction == "left":
             self.segments.append(Snakesegments(last_element.x - self.segment_size if last_element.direction == "right" 
                                                else last_element.x + self.segment_size, last_element.y, last_element.direction))
        else:
             self.segments.append(Snakesegments(last_element.x, last_element.y - self.segment_size if last_element.direction == "down" 
                                                else last_element.y + self.segment_size, last_element.direction))
             