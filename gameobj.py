import engine
class GameObject:

    instances = [] 

    def __init__(self, x, y, width, height, texture_filename, objectname, mass=1):
        self.name = objectname
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.texture_filename = texture_filename
        self.destroyed = False
        self.mass = mass
        self.vx = 0
        self.vy = 0
        self.ax = 0
        self.ay = -9.8  # Gravity
        GameObject.instances.append(self)

    def aabb(self):
        return self.x, self.y, self.x + self.width, self.y + self.height

    def collides_with(self, other):
        x1, y1, x2, y2 = self.aabb()
        ox1, oy1, ox2, oy2 = other.aabb()

        return not (x2 <= ox1 or x1 >= ox2 or y2 <= oy1 or y1 >= oy2)

    def draw(self):
        engine.draw_sprite(self.texture_filename, self.x, self.y, self.width, self.height)

    def destroy(self):
        self.destroyed = True

    def apply_physics(self, dt):
        self.vx += self.ax * dt
        self.vy += self.ay * dt
        self.x += self.vx * dt
        self.y += self.vy * dt

    def check_collisions(self):
        for other in GameObject.instances:
            if self != other and self.collides_with(other):
                self.resolve_collision(other)
                return True
            return False

    def resolve_collision(self, other):
        if self.collides_with(other):
            overlap_x = min(self.x + self.width, other.x + other.width) - max(self.x, other.x)
            overlap_y = min(self.y + self.height, other.y + other.height) - max(self.y, other.y)

            if overlap_x < overlap_y:
                if self.x < other.x:
                    self.x -= overlap_x
                else:
                    self.x += overlap_x
                self.vx = 0
            else:
                if self.y < other.y:
                    self.y -= overlap_y
                else:
                    self.y += overlap_y
                self.vy = 0