import os
import shutil
import time
import sys

if sys.version_info[0] == 3:
    # for Python3
    from tkinter import *  # notice lowercase 't' in tkinter here
else:
    # for Python2
    from Tkinter import *  # notice capitalized T in Tkinter

from PIL import Image, ImageDraw, ImageTk

from cube_stuff.cube_base import CubeBase


def ensure_directory_exists_and_is_empty(folder):
    if os.path.exists(folder):
        shutil.rmtree(folder, True)
    if not os.path.exists(folder):
        os.makedirs(folder)


class CubeVisualizer(CubeBase):
    def __init__(self, n):
        self.n = n
        self._buffer = [[[(0, 0, 0) for _ in range(n)] for _ in range(n)] for _ in range(n)]
        self.z_offset = (8, 8)
        self.pixel = 8
        self.margin = 100
        bg = (0, 0, 0)
        image_size = (800, 800)
        self.img = Image.new('RGB', image_size, bg)
        self.draw = ImageDraw.Draw(self.img)

        # Tkinter
        self.label = None
        self.root = None
        self.photo = None

        # dir
        self.image_number = 0
        self.paths = []
        self.folder = "tmp" + os.sep
        ensure_directory_exists_and_is_empty(self.folder)

    def set_rgb(self, xyz, rgb):
        x, y, z = xyz
        self._buffer[x][y][z] = rgb

    def rectangle(self, origin, size):
        return origin + tuple(map(sum, zip(origin, size)))

    def show(self):
        for pixel_x in range(self.n):
            for pixel_y in range(self.n):
                for pixel_z in range(self.n):
                    rgb = self._buffer[pixel_x][pixel_y][pixel_z]
                    x = self.margin + pixel_x * (self.pixel + self.margin) + pixel_z * self.z_offset[0]
                    y = self.margin + pixel_y * (self.pixel + self.margin) + pixel_z * self.z_offset[1]

                    rect = self.rectangle((x, y), (self.pixel, self.pixel))
                    self.draw.ellipse(rect, rgb, rgb)
        path = self.folder + "image{}.BMP".format(self.image_number)
        self.img.save(path, "BMP")

        self.paths.append(path)
        self.image_number += 1

    def sleep(self, secs):
        pass

    def finished(self):
        self._show_me_what_you_got()

    def _show_me_what_you_got(self):
        self.root = Tk()
        self.label = Label(self.root)
        self.label.pack()
        self.label.place(x=0, y=0)
        self.root.after(100, self.callback)
        self.root.mainloop()

    def callback(self):
        run = True
        while run:
            try:
                for path in self.paths:
                    print(path)
                    self.change_image(path)
                    time.sleep(0.05)
            except KeyboardInterrupt:
                run = False
        ensure_directory_exists_and_is_empty(self.folder)

    def change_image(self, path):
        image = Image.open(path)
        photo = ImageTk.PhotoImage(image)
        self.label.config(image=photo)
        self.label.image = photo  # keep a reference!
        self.label.pack()
        self.root.update()
