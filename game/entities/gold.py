class Gold:
    def __init__(self, x, y, amount):
        self.x = x
        self.y = y
        self.amount = amount
        self.size = 10
        self.collected = False
    
    def draw(self, surface, color):
        if not self.collected:
            surface.fill(color, (int(self.x) - self.size//2, int(self.y) - self.size//2, self.size, self.size))
    
    def collect(self, player):
        dx = self.x - player.x
        dy = self.y - player.y
        distance = (dx**2 + dy**2)**0.5
        if distance < (player.width // 2 + self.size):
            player.gold += self.amount
            self.collected = True
            return True
        return False
