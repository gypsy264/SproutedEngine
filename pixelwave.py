import tkinter as tk
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from PIL import Image, ImageTk
import engine
import game
import io

class PreviewApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Game Preview")
        self.canvas = tk.Canvas(self, width=640, height=480, bg="white")
        self.canvas.pack()
        
        self.update_button = tk.Button(self, text="Update Preview", command=self.update_preview)
        self.update_button.pack()

        glutInit()
 
    def update_preview(self):
        # Draw the game frame
        frame_image = game.draw_overwrite(640, 480)

        # Convert the image to a PhotoImage object
        photo_image = ImageTk.PhotoImage(frame_image)

        # Clear the canvas
        self.canvas.delete("all")

        # Add the image to the canvas
        self.canvas.create_image(0, 0, anchor=tk.NW, image=photo_image)

        # Store the image object to prevent garbage collection
        self.canvas.image = photo_image


if __name__ == "__main__":
    app = PreviewApp()
    app.mainloop()
