from tkinter import *
from PIL import Image, ImageTk
import time

class MyApp(object):
    def __init__(self, parent):
        self.width = 600
        self.height = 600
        self.parent = parent
        self.main_frame = Frame(parent)
        self.main_frame.pack()
        self.canvas_frame = Frame(self.main_frame)
        self.canvas_frame.pack(side=TOP)
        self.canvas = Canvas(self.main_frame, \
                             width=self.width, height=self.height)
        self.canvas.pack()

        self.stop_animation = False
        self.max_rolls = 0
        self.count_rolls = 0
        
        self.button_frame = Frame(self.main_frame)
        self.button_frame.pack(side=BOTTOM)
        self.drawbutton = Button(self.button_frame, text="1 Pull", \
                                 command = self.roll_one)
        self.drawbutton.pack(side=LEFT)
        self.drawbutton = Button(self.button_frame, text="10 Pull", \
                                 command = self.roll_ten)
        self.drawbutton.pack(side=LEFT)
        self.quitbutton = Button(self.button_frame, text="Main Menu", \
                                 command = self.main_menu)
        self.quitbutton.pack(side=RIGHT)
        self.quitbutton = Button(self.button_frame, text="Quit", \
                                 command = self.quit)
        self.quitbutton.pack(side=RIGHT)

    def quit(self):
        self.parent.destroy()
    
    def rand_num(self):
        return 1

    def update_gif(self, frame, img, canvas_img, stop):
        if self.stop_animation:
            self.canvas.delete("all")
            self.stop_animation = False
            return

        img.seek(frame)  # Move to the next frame
        update = ImageTk.PhotoImage(img)
        self.canvas.itemconfig(canvas_img, image=update)
        self.canvas.image = update

        if (stop and frame == img.n_frames-1):
            self.canvas.delete("all")
            self.stop_animation = False
            return
        self.parent.after(10, self.update_gif, (frame + 1) % img.n_frames, img, canvas_img, stop)

    def animate(self, pathname):
        img = Image.open(pathname)
        img_tk = ImageTk.PhotoImage(img)
        canvas_img = self.canvas.create_image(0, 0, anchor=NW, image=img_tk)
        self.canvas.image = img_tk

        return [canvas_img, img]
    
    def main_menu(self):
        self.stop_animation = True
        if self.canvas.find_all():
            self.parent.after(2, self.main_menu)
            return
        
        [canvas_img, img] = self.animate("./mainmenu.gif")
        self.stop_animation = False
        self.update_gif(0, img, canvas_img, False)
        
    def roll_one(self):
        self.stop_animation = True
        self.max_rolls = 1
        self.intro()

    def roll_ten(self):
        self.stop_animation = True
        self.max_rolls = 10
        self.intro()
        
    # buttons shouldn't be visible
    def intro(self):
        if self.canvas.find_all():
            self.parent.after(2, self.intro)
            return
        
        num = self.rand_num() # determines which intro and which character
        [canvas_img, img] = self.animate("./intro1.gif")
        self.count_rolls += 1

        self.stop_animation = False
        self.update_gif(0, img, canvas_img, True)

        self.character(num)

    def character(self, num):
        if self.canvas.find_all():
            self.parent.after(1, self.character, num)
            return

        # character intro animation
        [canvas_img, img] = self.animate("./"+str(num)+".gif")
        # character screen
        self.stop_animation = False
        self.update_gif(0, img, canvas_img, True)

        self.repeat(num)

    def repeat(self, num):
        if self.canvas.find_all():
            self.parent.after(2, self.repeat, num)
            return

        # on-click event -> main menu or next character intro
        # if max_rolls == count_rolls -> main menu
        [canvas_img, img] = self.animate("./"+str(num)+"repeat.gif")
        self.stop_animation = False
        self.update_gif(0, img, canvas_img, False)

        
        
### The main code simply creates a canvas and three buttons. 
if __name__ == "__main__":
    root = Tk()
    root.title("GachaSim")
    myapp = MyApp(root)
    root.mainloop()