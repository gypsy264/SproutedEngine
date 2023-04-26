#Make by Gypsy264 with love
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from PIL import Image
import time
import random




try:
    
    keydown = None
    keys_down = set()
    loaded_textures = {}

    def get_frame_as_image(width, height):
        glReadBuffer(GL_FRONT)
        pixels = glReadPixels(0, 0, width, height, GL_RGB, GL_UNSIGNED_BYTE)
        image = Image.frombytes("RGB", (width, height), pixels)
        image = image.transpose(Image.FLIP_TOP_BOTTOM)
        return image



    def draw_screen():
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # Clear the screen
        set_2d_projection()
        draw()
        glutSwapBuffers()
        glFlush()  # Force execution of GL commands


    def draw():
        
        pass 

    def load_texture(filename):

        global loaded_textures

        # If the texture is already loaded, return it
        if filename in loaded_textures:
            return loaded_textures[filename]

        # load image using PIL
        image = Image.open("./sprites/" + filename)
        # convert image to RGBA format to include alpha channel
        image = image.convert("RGBA")
        # get image data as a byte string
        image_data = image.tobytes("raw", "RGBA")
        # get image size
        width, height = image.size

        # generate a new texture object
        texture_id = glGenTextures(1)
        # bind the texture object
        glBindTexture(GL_TEXTURE_2D, texture_id)
        # set texture parameters
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        # set texture data
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, image_data)

        # Save the loaded texture in the dictionary
        loaded_textures[filename] = texture_id

        return texture_id


    def set_2d_projection():
        #glClearColor(0.0, 0.0, 0.0, 1.0)  # set clear color to black
        glClearColor(0.4, 0.6, 0.8, 1.0)  # Set clear color to light blue
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(-1, 1, -1, 1, -1, 1)
        glMatrixMode(GL_MODELVIEW)

    def draw_sprite(texture_filename, x, y, width, height):
        # load the sprite texture
        sprite_texture = load_texture(texture_filename)

        # enable 2D texturing
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, sprite_texture)

        # update the modelview matrix with the new position and scale
        glLoadIdentity()
        glTranslatef(x, y, 0)
        glScalef(width, height, 1)

        # render the sprite quad
        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 0.0)
        glVertex3f(-0.5, -0.5, 0.0)
        glTexCoord2f(1.0, 0.0)
        glVertex3f(0.5, -0.5, 0.0)
        glTexCoord2f(1.0, 1.0)
        glVertex3f(0.5, 0.5, 0.0)
        glTexCoord2f(0.0, 1.0)
        glVertex3f(-0.5, 0.5, 0.0)
        glEnd()

        # disable 2D texturing
        glDisable(GL_TEXTURE_2D)

        

    def update_tick(value):
        update()
        glutPostRedisplay() 
        glutTimerFunc(1000 // 60, update_tick, 0)
        
        
        #print("Updating Every Second")

    def update():
        pass


    def keyboard(key, x, y):
        global keydown
        key_name = key.decode()[0].lower()
        keydown = key_name
        keys_down.add(key_name)

    def keyboard_up(key, x, y):
        global keydown
        key_name = key.decode()[0].lower()
        keys_down.remove(key_name)
        keydown = None
        
    def reshape(width, height):
        if height == 0:
            height = 1

        aspect_ratio = float(width) / float(height)

        glViewport(0, 0, width, height)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        gluPerspective(45, aspect_ratio, 0.1, 100.0)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        
    def init(ScreenName):
        if ScreenName == None:
            print("Warning: ScreenName has no value")
            ScreenName = "Game"
        glutInit()
        glutInitDisplayMode(GLUT_RGBA|GLUT_DOUBLE|GLUT_DEPTH)
        glutInitWindowSize(640, 480)
        glutCreateWindow(ScreenName)
        glutKeyboardFunc(keyboard)
        glutKeyboardUpFunc(keyboard_up)
        glutReshapeFunc(reshape)
        glutDisplayFunc(draw_screen)
        glutTimerFunc(1000 // 60, update_tick, 0)
        glutMainLoop()

except Exception:
    print("Error")
