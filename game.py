#TestingGame
#Engine
import engine 
import utilities 
import gameobj
import ui

#Grpahics
from OpenGL.GL import *
from OpenGL.GLUT import *   
from OpenGL.GLU import *
import time
import random

#Variables
locx = 0
locy = 0
game_object1 = gameobj.GameObject(locy, locx, 0.5, 0.5, "player_texture.png", "player")
game_object2 = gameobj.GameObject(0.8, 0.8, 0.5, 0.5, "player_texture.png", "object1")

#walls

wall1 = gameobj.GameObject(0.0, -1, 2, 0.5, "wall.png", "wall1")

previous_time = time.time()

all_game_objects = [game_object1, game_object2, wall1] 

def start_local():
    engine.init("Game") 
    engine.update()
  

def update_overwrite():
    global game_object1
    global locx
    global locy

    new_x = locx
    new_y = locy
    

    if engine.keydown == "w":
        locx = locx + 0.05
    if engine.keydown == "s":
        locx = locx - 0.05
    #side movement
    if engine.keydown == "d":
        locy = locy + 0.05
    if engine.keydown == "a":
        locy = locy - 0.05

    

    for obj1 in all_game_objects:
        for obj2 in all_game_objects:
            if obj1 != obj2 and obj1.collides_with(obj2):
                obj1.resolve_collision(obj2)

    
    
    
def draw_overwrite():
    global locx
    global locy
    engine.set_2d_projection()

    global previous_time
    utilities.ShowFrame()

    current_time = time.time()
    dt = current_time - previous_time
    previous_time = current_time

    game_object2.apply_physics(dt)
    game_object1.apply_physics(dt)
    

    game_object1.x = locy
    game_object1.y = locx
   
    if game_object1.collides_with(game_object2):
        game_object1.destroy()
        ui.draw_text(0, 0, "Collision detected!")
        
        print("Collision detected!")
    else:
            ui.draw_text(0, 0, "Not detected!")
            print("No collision")
            
    game_object1.draw()
    game_object2.draw()
    wall1.draw()
    
    
    
engine.draw = draw_overwrite
engine.update = update_overwrite
start_local()