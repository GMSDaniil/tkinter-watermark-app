from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk, ImageDraw, ImageFont
import matplotlib.pyplot as plt
import os
from sys import platform


class MainWindow():
    def __init__(self, main) -> None:
        self.main = main

        ###IMG
        self.canvas = Canvas(main, width=200, height=180)
        self.curr_img = PhotoImage(file='logo.png')
        
        self.image_container = self.canvas.create_image(0,0, anchor='nw', image=self.curr_img)
        self.canvas.grid(column=1, row=0)

        ###WATERMARK
        self.curr_img_downl = None
        self.watermark = "GMS"

        ###Upload btn
        self.upload_btn = Button(main, text='Upload', command=self.imageUploader)
        self.upload_btn.grid(column=1, row=1, pady=5)

        ###Download btn
        self.download_btn = Button(main, text='Download', command=self.downloadImage)
        self.download_btn.grid(column=1, row=2, pady=5)

        ###Change Watermark
        self.download_btn = Button(main, text='Change Watermark', command=self.open_popup)
        self.download_btn.grid(column=1, row=3, pady=5)

        ###FileTypes
        if platform == "win32":
            self.fileTypes = [("Image files", "*.png;*.jpg;*.jpeg")]
        else:
            self.fileTypes = [("Image files", ".png .jpg .jpeg")]
    
    def imageUploader(self):
        
        path = filedialog.askopenfilename(filetypes=self.fileTypes)

        ##if file selected
        if len(path):
            curr_img = Image.open(path).convert("RGBA")
            width, height = curr_img.size
            curr_img = curr_img.rotate(45, expand=True)
            img_w, img_h = curr_img.size
            
            txt = Image.new('RGBA', (img_w, img_h), (0,0,0,0))
            font = ImageFont.truetype("impact.ttf", 25)
            draw = ImageDraw.Draw(txt)

            w , h =self.get_text_dimensions(self.watermark, font)
            curr_w = 0
            curr_h = 0
            while curr_h < img_w:
                while curr_w < img_h:
                    draw.text((curr_w,curr_h), self.watermark, fill=(0,0,0,50), font=font)
                    curr_w += w+10
                curr_w = 0
                curr_h += h+10
            
            
            combined = Image.alpha_composite(curr_img, txt).convert('RGBA')
            combined = combined.rotate(-45, expand=True)
            img_w , img_h = combined.size
            left = (img_w - width)/2
            top = (img_h - height)/2
            right = (img_w + width)/2
            bottom = (img_h + height)/2

            combined = combined.crop((left, top, right, bottom))
            

            show = combined.resize((int(combined.width*200/combined.height), 200))
            self.curr_img = ImageTk.PhotoImage(show)
            self.curr_img_downl = ImageTk.PhotoImage(combined)
            self.canvas.config(width=self.curr_img.width(), height=self.curr_img.height())
            


            self.canvas.itemconfig(self.image_container, image=self.curr_img)
            self.main.eval('tk::PlaceWindow . center')
        else:
            print("No file is Choosen !! Please choose a file.")


    def get_text_dimensions(self, text_string, font):
        ascent, descent = font.getmetrics()

        text_width = font.getmask(text_string).getbbox()[2]
        text_height = font.getmask(text_string).getbbox()[3] + descent

        return (text_width, text_height)

   
    
    def open_popup(self):
        top = Toplevel(self.main)
        top.title = 'New Watermart'
        Label(top, text='Type new watermark name:').grid(column=1, row=0)
        watermark_input = Entry(top)
        watermark_input.grid(column=1,row=1)

        def change_watermark():
            self.watermark = watermark_input.get()
            top.destroy()
            top.update()
        submit = Button(top, text='Change', command=change_watermark)
        submit.grid(column=1, row=2)

    def downloadImage(self):
        if not os.path.isdir("watermarks"):
            os.mkdir("watermarks")

        if self.curr_img_downl:
            i = 1
            while True:
                filename = 'watermarks/watermarked_image{}.png'.format(i)
                if os.path.isfile(filename):
                    i += 1
                else:
                    img = ImageTk.getimage( self.curr_img_downl).convert('RGBA')
                    img.save(filename, "PNG")
                    break
        
            
        

root = Tk()
root.title("Watermark")
root.eval('tk::PlaceWindow . center')
root.resizable(False,False)
MainWindow(root)
root.mainloop()
