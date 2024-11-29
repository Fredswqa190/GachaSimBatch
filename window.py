from tkinter import *
from PIL import Image, ImageTk

class MyApp(object):
    def __init__(self, parent):
        self.width = root.winfo_screenwidth()
        self.height = root.winfo_screenheight()

        self.parent = parent
        self.main_frame = Frame(parent)
        self.main_frame.pack()
        self.canvas_frame = Frame(self.main_frame)
        self.canvas_frame.pack(side=TOP)
        self.canvas = Canvas(self.main_frame, \
                             width=self.width, height=self.height)
        self.canvas.pack()

        self.pause = 1

        self.stop_animation = False
        self.max_rolls = 0
        self.count_rolls = 0

        self.wishes = 90
        self.characters = {1:0} # {1:0, 2:0, 3:0}

        self.increment = int(self.width/7)
        self.button_height = self.height-100

        self.roll1button = Button(text="1 Pull", \
                                 width=20, height=2, command = self.roll_one)

        self.roll10button = Button(text="10 Pull", \
                                 width=20, height=2, command = self.roll_ten)

        self.displayChars = Button(text="Characters", \
                                 width=20, height=2, command = self.display_characters)

        self.displayHist = Button(text="History", \
                                 width=20, height=2, command = self.display_history)

        self.rulesbutton = Button(text="Rules", \
                                 width=20, height=2, command = self.rules)

        self.quitbutton = Button(text="Quit", \
                                 width=20, height=2, command = self.quit)

        self.mainmenu = Button(text="Main Menu", \
                                 width=20, height=2, command = self.main_menu)
        self.next = Button(text="Next", \
                                 width=20, height=2, command = self.intro)
        self.back = Button(text="Back", \
                                 width=20, height=2, command = self.display_characters)
        
        self.main_menu()
        
    def quit(self):
        self.parent.destroy()
    
    def rand_num(self):
        return 1
    
    def hide_buttons(self):
        self.roll1button.place_forget()
        self.roll10button.place_forget()
        self.quitbutton.place_forget()
        self.mainmenu.place_forget()
        self.next.place_forget()
        self.displayChars.place_forget()
        self.displayHist.place_forget()
        self.back.place_forget()
        self.rulesbutton.place_forget()

    def show_buttons(self):
        self.roll1button.place(x=self.increment, y=self.button_height, anchor="center")
        self.roll10button.place(x=2*self.increment, y=self.button_height, anchor="center")
        self.displayChars.place(x=3*self.increment, y=self.button_height, anchor="center")
        self.displayHist.place(x=4*self.increment, y=self.button_height, anchor="center")
        self.rulesbutton.place(x=5*self.increment, y=self.button_height, anchor="center")
        self.quitbutton.place(x=6*self.increment, y=self.button_height, anchor="center")

    def update_gif(self, frame, img, canvas_img, stop):
        if self.stop_animation:
            self.canvas.delete("all")
            self.stop_animation = False
            return

        img.seek(frame)  # Move to the next frame
        resize_img = img.resize((self.width, self.height))
        update = ImageTk.PhotoImage(resize_img)
        self.canvas.itemconfig(canvas_img, image=update)
        self.canvas.image = update

        if (stop and frame == img.n_frames-1):
            self.canvas.delete("all")
            self.stop_animation = False
            return
        self.parent.after(33, self.update_gif, (frame + 1) % img.n_frames, img, canvas_img, stop) # around 30 fps

    def animate(self, pathname):
        img = Image.open(pathname)
        resize_img = img.resize((self.width, self.height))
        img_tk = ImageTk.PhotoImage(resize_img)
        canvas_img = self.canvas.create_image(0, 0, anchor=NW, image=img_tk)
        self.canvas.image = img_tk

        return [canvas_img, img]
    
    def main_menu(self):
        self.stop_animation = True
        self.mainmenu.place_forget()
        if self.canvas.find_all():
            self.parent.after(self.pause, self.main_menu)
            return
        
        self.show_buttons()

        self.count_rolls = 0
        
        [canvas_img, img] = self.animate("./mainmenu.gif")
        self.canvas.create_text(0, 500, text="Remaining wishes: "+str(self.wishes), font=('Helvetica', 20), fill="blue")
        
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
        
    def intro(self):
        self.stop_animation = True
        self.hide_buttons()
        if self.canvas.find_all():
            self.parent.after(self.pause, self.intro)
            return
        
        num = self.rand_num() # determines which intro and which character
        [canvas_img, img] = self.animate("./intro1.gif")
        self.count_rolls += 1
        self.wishes -= 1
        self.characters[num] += 1

        self.stop_animation = False
        self.update_gif(0, img, canvas_img, True)

        self.character(num)

    def character(self, num):
        if self.canvas.find_all():
            self.parent.after(1, self.character, num)
            return

        # character intro animation
        [canvas_img, img] = self.animate("./character_images/"+str(num)+".gif")
        # character screen
        self.stop_animation = False
        self.update_gif(0, img, canvas_img, True)

        self.repeat(num)

    def repeat(self, num):
        if self.canvas.find_all():
            self.parent.after(self.pause, self.repeat, num)
            return
        
        if self.max_rolls == self.count_rolls:
            self.mainmenu.place(x=int(self.width/2), y=self.button_height, anchor="center")
        else:
            self.next.place(x=int(self.width/2), y=self.button_height, anchor="center")

        [canvas_img, img] = self.animate("./repeat_images/"+str(num)+"repeat.gif")
        self.stop_animation = False
        self.update_gif(0, img, canvas_img, False)

    def display_char(self, num):
        self.stop_animation = True
        self.mainmenu.place_forget()
        if self.canvas.find_all():
            self.parent.after(self.pause, self.display_char, num)
            return
        
        self.back.place(x=int(self.width/2), y=self.button_height, anchor="center")
        [canvas_img, img] = self.animate("./repeat_images/"+str(num)+"repeat.gif")
        self.stop_animation = False
        self.update_gif(0, img, canvas_img, False)

    def display_characters(self):
        self.stop_animation = True
        self.hide_buttons()
        if self.canvas.find_all():
            self.parent.after(self.pause, self.display_characters)
            return
        
        self.mainmenu.place(x=int(self.width/2), y=self.button_height, anchor="center")

        [canvas_img, img] = self.animate("./background.gif")

        text = self.canvas.create_text(200, 100, text="character 1", font=('Helvetica', 20), fill="white", anchor=CENTER)
        self.canvas.tag_bind(text, "<Button-1>", lambda event: self.display_char(1))

        self.stop_animation = False
        self.update_gif(0, img, canvas_img, False)
    
    def display_history(self):
        self.stop_animation = True
        self.hide_buttons()
        if self.canvas.find_all():
            self.parent.after(self.pause, self.display_history)
            return
        
        self.mainmenu.place(x=int(self.width/2), y=self.button_height, anchor="center")

        [canvas_img, img] = self.animate("./background.gif")

        for i in range(1):
            num = self.characters[i+1]
            self.canvas.create_text(200, (i+1)*100, text="character "+str(i+1)+": "+str(num), font=('Helvetica', 20), fill="white", anchor=CENTER)

        self.stop_animation = False
        self.update_gif(0, img, canvas_img, False)

    def rules(self):
        self.stop_animation = True
        self.hide_buttons()
        if self.canvas.find_all():
            self.parent.after(self.pause, self.rules)
            return
        
        self.mainmenu.place(x=int(self.width/2), y=self.button_height, anchor="center")

        [canvas_img, img] = self.animate("./background.gif")

        # Rules

        self.stop_animation = False
        self.update_gif(0, img, canvas_img, False)

        
        
### The main code simply creates a canvas and three buttons. 
if __name__ == "__main__":
    root = Tk()
    root.title("GachaSim")
    myapp = MyApp(root)
    root.mainloop()