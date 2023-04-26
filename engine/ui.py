from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

def draw_text(x, y, text):
    glDisable(GL_TEXTURE_2D)
    glColor3f(1, 1, 1)
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(GLUT_BITMAP_9_BY_15, ord(ch))
    glEnable(GL_TEXTURE_2D)