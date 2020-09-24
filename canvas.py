import tkinter as tk

WIDTH = 600
HEIGHT = 400


def create_canvas(width, height):
    """ Create canvas """
    root = tk.Tk()
    root.geometry(f'{str(width)}x{str(height)}')
    canvas = tk.Canvas(root, bg='white')
    canvas.pack(fill=tk.BOTH, expand=1)
    return canvas, root


