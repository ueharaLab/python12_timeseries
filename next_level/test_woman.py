import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageOps
from IPython.display import display


fig, ax = plt.subplots()
ln, = ax.plot([],[],'bo')

def fill(event):
    
    x = int(event.xdata)
    y = int(event.ydata)
    if im.getpixel((x,y))[3] != 0:
        im.putpixel((x,y), (255,200,200))
    
        ax.imshow(im)
        plt.draw()
        
        

im = Image.open('woman.png')
fig.canvas.mpl_connect('motion_notify_event',fill)
ax.imshow(im)
plt.show()



