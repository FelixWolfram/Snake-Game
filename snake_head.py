from pygame import image, transform


class SnakeHeadImg:
    def __init__(self):
        self.img = image.load("caleb.png")
        self.img = transform.rotate(self.img, -90)

        
    def rotate_right(self):
        self.img = transform.rotate(self.img, -90)


    def rotate_left(self):
        self.img = transform.rotate(self.img, 90)
