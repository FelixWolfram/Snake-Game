class Snakehead:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction
        self.just_turned = False 


class Snakesegments:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction


class Turncells:
    def __init__(self, cell, direction, round_corner):
        self.cell = cell
        self.direction = direction
        self.segments_passed = 0
        self.round_corner = round_corner    # stores, at which corner the snake should be round -> only for the animation