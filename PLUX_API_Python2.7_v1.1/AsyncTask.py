import tkinter as tk
import asyncio
from random import randrange as rr

class App(tk.Tk):

    def __init__(self, loop, interval=1/120):
        super().__init__()
        self.loop = loop
        self.protocol("WM_DELETE_WINDOW", self.close)
        self.tasks = []
        self.tasks.append(loop.create_task(self.rotator(1/60, 2)))
        self.tasks.append(loop.create_task(self.updater(interval)))
    
    def deg_color(deg, d_per_tick, color):
        deg += d_per_tick
        if 360 <= deg:
            deg %= 360
            color = '#%02x%02x%02x' % (rr(0, 256), rr(0, 256), rr(0, 256))
        return deg, color

    async def rotator(self, interval, d_per_tick):
        canvas = tk.Canvas(self, height=600, width=600)
        canvas.pack()
        deg = 0
        color = 'black'
        arc = canvas.create_arc(100, 100, 500, 500, style=tk.CHORD,
                                start=0, extent=deg, fill=color)
        while await asyncio.sleep(interval, True):
            deg, color = self.deg_color(deg, d_per_tick, color)
            canvas.itemconfigure(arc, extent=deg, fill=color)

    async def updater(self, interval):
        while True:
            self.update()
            await asyncio.sleep(interval)