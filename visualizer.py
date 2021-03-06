import re
import time
import tkinter

import requests
from PIL import Image, ImageTk, UnidentifiedImageError


class Visualizer:
    __sequence_number = 0

    def __init__(self, url=None):
        self.__url = url

    def run(self):

        while True:
            self.__sequence_number = 0
            self.__download_all(self.__url)
            for index in range(0, self.__sequence_number):
                image_name = str(index) + ".jpg"
                im = None
                try:
                    im = Image.open(image_name)

                    self.__display(im)
                    time.sleep(5)
                    im.close()
                except UnidentifiedImageError as e:
                    print(e)
                    if im is not None:
                        im.close()


    @staticmethod
    def __display(image):
        root = tkinter.Toplevel()
        w, h = root.winfo_screenwidth(), root.winfo_screenheight()
        root.overrideredirect(1)
        root.geometry("%dx%d+0+0" % (w, h))
        root.focus_set()
        root.bind("<Escape>", lambda e: (e.widget.withdraw(), e.widget.quit()))
        canvas = tkinter.Canvas(root, width=w, height=h)
        canvas.pack()
        canvas.configure(background='black')
        img_width, img_height = image.size
        if img_width > w or img_height > h:
            ratio = min(w / img_width, h / img_height)
            img_width = int(img_width * ratio)
            img_height = int(img_height * ratio)
            image = image.resize((img_width, img_height), Image.ANTIALIAS)

        image = ImageTk.PhotoImage(image)
        canvas.create_image(w / 2, h / 2, image=image)
        root.update()

    @staticmethod
    def __download(url, image_name):
        try:
            r = requests.get(url)
            if r.status_code == requests.codes.ok:
                f = open(image_name, 'wb+')
                for chunk in r.iter_content(1024):
                    f.write(chunk)
                f.close()
            print('Image downloaded from url: {} and saved to: {}.'.format(url, image_name))
        except requests.exceptions.RequestException as e:  # This is the correct syntax
            print(e)

    def __download_all(self, url):

        try:
            response = requests.get(self.__url)

            urls = re.findall(r'<media:content\surl=\"(.*?)\".*\/>', response.text)
            for url in urls:
                image_name = str(self.__sequence_number) + '.jpg'
                self.__download(url, image_name)
                self.__sequence_number += 1
        except requests.exceptions.RequestException as e:  # This is the correct syntax
            print(e)
