from random import randint
from pygame import draw

class Apple:
    def __init__(self, head, segments, field_coords, cell_size, field_size):
        self.head = head
        self.segments = segments
        self.cell_size = cell_size
        self.field_size = field_size
        self.pos = None # position of the apple (index in field_coords)
        self.color = (255, 0, 0) 
        self.field_coords = field_coords
        

    def generate_apple(self):
        valid_pos = False
        while not valid_pos:
            self.pos = randint(0, int((self.field_size ** 2) - 1))

            # check if the apple is not on the snake
            if self.field_coords[self.pos] == (self.head.x, self.head.y): # if the apple is on the head of the snake
               continue
            else:
                valid_pos = True
                for segment in self.segments:
                    if self.field_coords[self.pos] == (segment.x, segment.y):
                        valid_pos = False


    def draw(self, win):
        draw.rect(win, self.color, (self.field_coords[self.pos], (self.cell_size, self.cell_size)))