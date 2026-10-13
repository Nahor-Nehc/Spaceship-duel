from Components.settings import *


class Bullet:
    def __init__(self, x, y, direction:[-1 or 1]):
        """direction is 1 or -1 (1 is to the right and -1 is to the left)"""
        self.x = x
        self.y = y
        self.width = AMMO_BAR_WIDTH
        self.height = BULLET_HEIGHT
        self.speed = BULLET_VEL * direction
        self.update()
    
    def move(self):
        self.x += self.speed
        self.update()
        
    def update(self):
        self.rect = (self.x, self.y, self.width, self.height)
    
class Bullets:
    def __init__(self, direction):
        self.bullets = []
        self.direction = direction

    def __call__(self):
        return self.bullets
    
    def add_bullet(self, bullet_position):
        new_bullet = Bullet(bullet_position[0], bullet_position[1], self.direction)
        self.bullets.append(new_bullet)
    
    def unpack(self):
        return [(bullet.x, bullet.y) for bullet in self.bullets]
    
    def get_bullets(self):
        return self.unpack()

    def move(self):
        for bullet in self.bullets:
            bullet.move()
            if bullet.x < -50 or bullet.x > WIDTH:
                self.bullets.remove(bullet)