import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import cv2

image_path = "my_chessboards/11.jpeg"

fig = plt.figure(figsize=(20,30))
img=cv2.imread(image_path)

def onclick(event):
    ix, iy = event.xdata, event.ydata
    print("Coordinate clicked pixel (row,column): [{},{}]".format(int(round(ix)), int(round(iy))))

cid = fig.canvas.mpl_connect('button_press_event', onclick)

imgplot = plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
plt.show()
