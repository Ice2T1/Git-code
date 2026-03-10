from game.items.weapon import weapons

class Player:
    def __init__(self):
        self.x = 400  # SCREEN_WIDTH // 2
        self.y = 300  # SCREEN_HEIGHT // 2
        self.width = 30
        self.height = 30
        self.speed = 5
        self.health = 100
        self.max_health = 100
        self.attack_speed = 1.0
        self.range = 100
        self.gold = 0
        # 初始武器
        self.weapon = weapons["Pistol"]
    
    def draw(self, surface, color):
        surface.fill(color, (self.x - self.width//2, self.y - self.height//2, self.width, self.height))
    
    def move(self, keys, screen_width, screen_height):
        if keys[0]:  # W
            self.y -= self.speed
        if keys[1]:  # S
            self.y += self.speed
        if keys[2]:  # A
            self.x -= self.speed
        if keys[3]:  # D
            self.x += self.speed
        
        # 边界检查
        if self.x < self.width//2:
            self.x = self.width//2
        if self.x > screen_width - self.width//2:
            self.x = screen_width - self.width//2
        if self.y < self.height//2:
            self.y = self.height//2
        if self.y > screen_height - self.height//2:
            self.y = screen_height - self.height//2
