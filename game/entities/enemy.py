class Enemy:
    def __init__(self, x, y, enemy_type, color):
        self.x = x
        self.y = y
        self.enemy_type = enemy_type
        self.color = color
        
        # 根据敌人类型设置属性
        if enemy_type == "basic":
            self.width = 20
            self.height = 20
            self.speed = 2
            self.health = 20
            self.damage = 5
        elif enemy_type == "fast":
            self.width = 15
            self.height = 15
            self.speed = 4
            self.health = 10
            self.damage = 3
        elif enemy_type == "tank":
            self.width = 30
            self.height = 30
            self.speed = 1
            self.health = 50
            self.damage = 10
    
    def draw(self, surface):
        surface.fill(self.color, (self.x - self.width//2, self.y - self.height//2, self.width, self.height))
    
    def move(self, player):
        # 简单的追踪AI
        dx = player.x - self.x
        dy = player.y - self.y
        distance = (dx**2 + dy**2)**0.5
        if distance > 0:
            self.x += (dx / distance) * self.speed
            self.y += (dy / distance) * self.speed
