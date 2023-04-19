import engine 
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GLUT import GLUT_BITMAP_9_BY_15

def draw_text(x, y, text):
    glDisable(GL_TEXTURE_2D)  # Disable textures before drawing text
    glColor3f(1, 1, 1)  # Set text color
    glRasterPos2f(x, y)  # Set text position
    for ch in text:
        glutBitmapCharacter(GLUT_BITMAP_9_BY_15, ord(ch))
    glEnable(GL_TEXTURE_2D)