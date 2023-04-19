import tkinter as tk
from PIL import ImageGrab


class PixelArtApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("PixelWave")
        self.geometry("500x500")

        self.canvas = tk.Canvas(self, bg="white", width=500, height=50)
        self.canvas.pack(padx=10, pady=10)

        self.canvas.bind("<B1-Motion>", self.draw_pixel)
        self.canvas.bind("<B3-Motion>", self.delete_pixel)

        self.save_button = tk.Button(self, text="Save", command=self.save_image)
        self.save_button.pack(pady=10)

        self.undo_button = tk.Button(self, text="Undo", command=self.undo)
        self.undo_button.pack(side="left", padx=10)

        self.redo_button = tk.Button(self, text="Redo", command=self.redo)
        self.redo_button.pack(side="right", padx=10)

        self.history = []
        self.redo_history = []


    def draw_pixel(self, event):
        x = event.x // 10 * 10
        y = event.y // 10 * 10
        rect_id = self.canvas.create_rectangle(x, y, x + 10, y + 10, fill="black", outline="")
        self.history.append(('draw', rect_id))
        self.redo_history = []


    def delete_pixel(self, event):
        x = event.x // 10 * 10
        y = event.y // 10 * 10
        rect_id = self.canvas.create_rectangle(x, y, x + 10, y + 10, fill="white", outline="")
        self.history.append(('delete', rect_id))
        self.redo_history = []


    def save_image(self):
        x0 = self.canvas.winfo_rootx()
        y0 = self.canvas.winfo_rooty()
        x1 = x0 + self.canvas.winfo_width()
        y1 = y0 + self.canvas.winfo_height()
        ImageGrab.grab().crop((x0, y0, x1, y1)).save("image1.png")

    def undo(self):
        if not self.history:
            return
        action, rect_id = self.history.pop()
        coords = self.canvas.coords(rect_id)
        self.redo_history.append((action, rect_id, coords))
        self.canvas.delete(rect_id)

    def redo(self):
        if not self.redo_history:
            return
        action, rect_id, coords = self.redo_history.pop()
        x1, y1, x2, y2 = coords
        fill_color = "black" if action == 'draw' else "white"
        new_rect_id = self.canvas.create_rectangle(x1, y1, x2, y2, fill=fill_color, outline="")
        self.history.append((action, new_rect_id))

if __name__ == "__main__":
    app = PixelArtApp()
    app.mainloop()