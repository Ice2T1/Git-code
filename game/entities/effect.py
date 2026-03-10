class Effect:
    def __init__(self, x, y, effect_type):
        self.x = x
        self.y = y
        self.effect_type = effect_type
        self.lifetime = 60
        self.timer = 0
    
    def draw(self, surface, color):
        if self.timer < self.lifetime:
            if self.effect_type == "explosion":
                size = 5 + (self.timer // 10) * 5
                surface.fill(color, (int(self.x) - size//2, int(self.y) - size//2, size, size))
            elif self.effect_type == "hit":
                size = 10 - (self.timer // 6)
                surface.fill(color, (int(self.x) - size//2, int(self.y) - size//2, size, size))
    
    def update(self):
        self.timer += 1
        return self.timer < self.lifetime
