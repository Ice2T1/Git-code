class Bullet:
    def __init__(self, x, y, dx, dy, damage, range):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.speed = 8
        self.damage = damage
        self.range = range
        self.distance = 0
    
    def draw(self, surface, color):
        surface.fill(color, (int(self.x) - 2, int(self.y) - 2, 4, 4))
    
    def update(self):
        self.x += self.dx * self.speed
        self.y += self.dy * self.speed
        self.distance += self.speed
        return self.distance < self.range
