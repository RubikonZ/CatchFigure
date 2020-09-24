""" file contains everything about creation of shapes"""
from abc import ABC, abstractmethod
from random import randint as rnd, choice
from canvas import *

colors = ['red', 'orange', 'yellow', 'green', 'blue']
random_directions = [-2, +2]

canv, root = create_canvas(WIDTH, HEIGHT)


class Shape(ABC):
    shape_id = None

    def __init__(self):
        self.canv = canv
        self.root = root
        # For movement:
        self.dx = choice(random_directions)
        self.dy = choice(random_directions)

    @abstractmethod
    def type_shape(self):
        pass

    @abstractmethod
    def new_shape(self):
        pass

    @abstractmethod
    def hit_shape(self, event):
        pass

    @abstractmethod
    def move_shape(self):
        pass


class Circle(Shape):
    def __init__(self):
        Shape.__init__(self)
        self.r = rnd(20, 50)
        self.x = rnd(self.r, WIDTH - self.r)
        self.y = rnd(self.r, HEIGHT - self.r)

    def type_shape(self):
        return 'CIRCLE'

    def new_shape(self):
        """ Generates CIRCLE """
        self.shape_id = self.canv.create_oval(self.x - self.r, self.y - self.r, self.x + self.r, self.y + self.r,
                                              fill=choice(colors), width=2)

    def hit_shape(self, event):
        """ Hit check for CIRCLE"""
        return ((self.x - event.x) ** 2 + (self.y - event.y) ** 2) ** 0.5 <= self.r

    def move_shape(self):
        """ Movement and bounce off wall logic for CIRCLE"""
        if self.x + self.r >= WIDTH or self.x - self.r <= 0:
            self.dx = -self.dx
        if self.y + self.r >= HEIGHT or self.y - self.r <= 0:
            self.dy = -self.dy


class Square(Shape):
    def __init__(self):
        Shape.__init__(self)
        self.r = rnd(20, 50)
        self.x = rnd(self.r, WIDTH - self.r)
        self.y = rnd(self.r, HEIGHT - self.r)

    def type_shape(self):
        return 'SQUARE'

    def new_shape(self):
        """ Generates SQUARE with given parameters """
        self.shape_id = self.canv.create_rectangle(self.x - self.r / 2, self.y - self.r / 2, self.x + self.r / 2,
                                                   self.y + self.r / 2,
                                                   fill=choice(colors), width=2)

    def hit_shape(self, event):
        """ Hit check for SQUARE"""
        return ((self.x - self.r / 2) <= event.x <= (self.x + self.r / 2)) and \
               ((self.y - self.r / 2) <= event.y <= (self.y + self.r / 2))

    def move_shape(self):
        """ Movement and bounce off wall logic for SQUARE"""
        if self.x + self.r / 2 >= WIDTH or self.x - self.r / 2 <= 0:
            self.dx = -self.dx
        if self.y + self.r / 2 >= HEIGHT or self.y - self.r / 2 <= 0:
            self.dy = -self.dy


class Rectangle(Shape):
    def __init__(self):
        Shape.__init__(self)
        self.width = rnd(40, 60)
        self.height = rnd(40, 60)
        self.x = rnd(self.width // 2, WIDTH - self.width // 2)
        self.y = rnd(self.height // 2, HEIGHT - self.height // 2)

    def type_shape(self):
        return 'RECTANGLE'

    def new_shape(self):
        """ Generates RECTANGLE with given parameters """
        self.shape_id = self.canv.create_rectangle(self.x - self.width / 2, self.y - self.height / 2,
                                                   self.x + self.width / 2,
                                                   self.y + self.height / 2,
                                                   fill=choice(colors), width=2)

    def hit_shape(self, event):
        """ Hit check for RECTANGLE"""
        return ((self.x - self.width / 2) <= event.x <= (self.x + self.width / 2)) and \
               ((self.y - self.height / 2) <= event.y <= (self.y + self.height / 2))

    def move_shape(self):
        """ Movement and bounce off wall logic for SQUARE"""
        if self.x + self.width / 2 >= WIDTH or self.x - self.width / 2 <= 0:
            self.dx = -self.dx
        if self.y + self.height / 2 >= HEIGHT or self.y - self.height / 2 <= 0:
            self.dy = -self.dy


class Storage:
    """ Collection of class 'Shape'"""
    def __init__(self):
        self.canv = canv
        self.root = root
        self.count = 0
        self.canv.bind('<Button-1>', self.hit_shapes)
        self.holding_shapes = []
        self.shape_counter = 0  # Number of ALL shapes
        self.ignored_shapes = 0  # IGNORED shapes counter
        self.shapes_hit = 0  # Shape HIT counter
        self.shapes_miss = 0  # Shape MISS counter

    def create_and_hold_shapes(self):
        """ Creates and holds up to 3 shapes """
        if len(self.holding_shapes) >= 3:
            self.ignored_shapes += 1  # Counter for ignored shapes
            print(f'Ignored shape №{self.ignored_shapes}, deleting oldest one')
            self.canv.delete(self.holding_shapes[0].shape_id)  # Deletes ignored shape from canvas
            del self.holding_shapes[0]  # Deletes ignored shape from 3-shape pool
        shape = Circle()
        # TODO: Понять как одновременно создавать шейпы разных классов И чтобы они получали разные координаты
        shape.new_shape()
        self.shape_counter += 1
        print(f'Generated {shape.type_shape()} shape №{self.shape_counter}, x: {shape.x} y: {shape.y}')
        self.holding_shapes.append(shape)

    def generate_shapes(self):  # Figure out how to get new coordinates
        """ Chooses which shape to generate """
        return choice(random_shapes)

    def hit_shapes(self, event):
        """ Compares button press coordinates to existing shapes """
        for shape in self.holding_shapes:
            if shape.hit_shape(event):
                self.shapes_hit += 1
                print(f'you hit the shape {self.shapes_hit} times(s), deleting the shape')
                self.canv.delete(shape.shape_id)
                del self.holding_shapes[self.holding_shapes.index(shape)]
                return
        else:
            self.shapes_miss += 1
            print(f'you missed {self.shapes_miss} time(s)')

    def tick(self):
        """ Loops program """
        self.create_and_hold_shapes()  # Usual work
        self.tick_move()
        self.root.after(1500, self.tick)
        # TODO: Добавить одновременный мувмент (скорее всего созданием отдельного Tick'a под движение

    def tick_move(self):
        """ Loop for movement """
        for shape in self.holding_shapes:
            shape.move_shape()
            canv.move(shape.shape_id, shape.dx, shape.dy)
            shape.x += shape.dx
            shape.y += shape.dy
        # self.move_accel()
        self.root.after(25, self.tick_move)


random_shapes = [Square(), Circle(), Rectangle()]

if __name__ == '__main__':
    print('Figure.py check check')
