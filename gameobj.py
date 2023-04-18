import engine
class GameObject:
    def __init__(self, x, y, width, height, texture_filename, objectname):
        self.name = objectname
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.texture_filename = texture_filename
        self.destroyed = False

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