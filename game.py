#Engine
import engine 
import utilities 
import gameobj


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


def start_local():
    engine.init("Game") 
    engine.update()



    
    
def update_overwrite():
    global game_object1
    global locx
    global locy
    utilities.ShowFrame()

   


    if engine.keydown == "w":
        locx = locx + 0.05
    if engine.keydown == "s":
        locx = locx + -0.05
    #side movement
    if engine.keydown == "d":
        locy = locy + 0.05
    if engine.keydown == "a":
        locy = locy + -0.05
    
def draw_overwrite():
    global locx
    global locy
    engine.set_2d_projection()

    game_object1.x = locy
    game_object1.y = locx
   
    if game_object1.collides_with(game_object2):
        game_object1.destroy()
        print("Collision detected!")
    else:
            print("No collision")
   
    game_object1.draw()
    game_object2.draw()
    
    
    
engine.draw = draw_overwrite
engine.update = update_overwrite
start_local()