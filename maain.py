import tkinter
import cv2
import easygui
import matplotlib.pyplot as plt
import os
from tkinter import *


def upload():
    image_path = easygui.fileopenbox()
    make_cartoon(image_path)


def make_cartoon(image_path):
    original_image = cv2.imread(image_path)
    original_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)
    if original_image is None:
        print("Can not find any image. Choose appropriate file")
        sys.exit()
    re_sized1 = cv2.resize(original_image, (960, 540))
    gray_scale_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
    re_sized2 = cv2.resize(gray_scale_image, (960, 540))
    smooth_gray_scale = cv2.medianBlur(gray_scale_image, 5)
    re_sized3 = cv2.resize(smooth_gray_scale, (960, 540))
    get_edge = cv2.adaptiveThreshold(smooth_gray_scale, 255,
                                     cv2.ADAPTIVE_THRESH_MEAN_C,
                                     cv2.THRESH_BINARY, 9, 9)
    re_sized4 = cv2.resize(get_edge, (960, 540))
    color_image = cv2.bilateralFilter(original_image, 9, 300, 300)
    re_sized5 = cv2.resize(color_image, (960, 540))
    cartoon_image = cv2.bitwise_and(color_image, color_image, mask=get_edge)
    re_sized6 = cv2.resize(cartoon_image, (960, 540))
    images = [re_sized1, re_sized2, re_sized3, re_sized4, re_sized5, re_sized6]
    fig, axes = plt.subplots(3, 2, figsize=(8, 8), subplot_kw={'xticks': [], 'yticks': []},
                             gridspec_kw=dict(hspace=0.1, wspace=0.1))
    for i, ax in enumerate(axes.flat):
        ax.imshow(images[i], cmap='gray')
    save1 = Button(top, text="Save cartoon image", command=lambda: save(re_sized6, image_path), padx=30, pady=5)
    save1.configure(background='#364156', foreground='white', font=('italic', 10, 'bold'))
    save1.pack(side=TOP, pady=50)
    plt.show()


def save(re_sized6, image_path):
    new_name = "Cartoon_Image"
    path1 = os.path.dirname(image_path)
    extension = os.path.splitext(image_path)[1]
    path = os.path.join(path1, new_name + extension)
    cv2.imwrite(path, cv2.cvtColor(re_sized6, cv2.COLOR_RGB2BGR))
    image_message = "Image saved by name " + new_name + " at " + path
    tkinter.messagebox.showinfo(title=None, message=image_message)


top = tkinter.Tk()
top.geometry('400x400')
top.title('Cartoon Your Image !')
top.configure(background='white')
label = Label(top, background='#CDCDCD', font=('italic', 20, 'bold'))

upload = Button(top, text="Cartoon an Image", command=upload, padx=10, pady=5)
upload.configure(background='#364156', foreground='white', font=('italic', 10, 'bold'))
upload.pack(side=TOP, pady=50)

top.mainloop()
