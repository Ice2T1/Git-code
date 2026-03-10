# 武器类
class Weapon:
    def __init__(self, name, damage, attack_speed, range, bullet_count):
        self.name = name
        self.damage = damage
        self.attack_speed = attack_speed
        self.range = range
        self.bullet_count = bullet_count

# 武器列表
weapons = {
    "Pistol": Weapon("Pistol", 10, 1.0, 300, 1),
    "Shotgun": Weapon("Shotgun", 15, 0.7, 250, 3),
    "Machine Gun": Weapon("Machine Gun", 8, 1.5, 350, 1)
}
