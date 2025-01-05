from tkinter import *
from PIL import Image, ImageTk
import random

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
        self.started = True

        self.error = "Can't wish anymore."
        self.errorID = None
        self.stop_animation = False
        self.max_rolls = 0
        self.count_rolls = 0

        self.wishes = 90
        self.characters = {1:0, # 1 5-star 
                            2:0, 3:0, # 2 4-star characters
                            4:0, 5:0, 6:0, 7:0, # 4 3-star weapons
                            8:0, 9:0, 10:0, 11:0} # 4 2-star weapons

        self.char_names = {1:"Sienna Ines", # 1 5-star 
                            2:"Raziel Sera", 3:"Styx Ferryman", # 2 4-star characters
                            4:"weapon1", 5:"weapon2", 6:"weapon3", 7:"weapon4", # 4 3-star weapons
                            8:"weapon5", 9:"weapon6", 10:"weapon7", 11:"weapon8"} # 4 2-star weapons

        self.increment = int(self.width/6)
        self.button_height = self.height-100
        self.button_background = "#A9E6E0"
        self.button_text_color = "#DD3B0F"
        self.button_text_font = "Comic Sans MS"

        self.buttonW = int(self.width/100)
        self.buttonH = int(self.height/500)

        self.roll1button = Button(text="1 Pull", \
                                 width=self.buttonW, height=self.buttonH, command = self.roll_one,
                                 bg=self.button_background, fg=self.button_text_color, font=(self.button_text_font, 14, "bold"))

        self.roll10button = Button(text="10 Pull", \
                                 width=self.buttonW, height=self.buttonH, command = self.roll_ten,
                                 bg=self.button_background, fg=self.button_text_color, font=(self.button_text_font, 14, "bold"))

        self.displayHist = Button(text="History", \
                                 width=self.buttonW, height=self.buttonH, command = self.display_history,
                                 bg=self.button_background, fg=self.button_text_color, font=(self.button_text_font, 14, "bold"))

        self.rulesbutton = Button(text="Rules", \
                                 width=self.buttonW, height=self.buttonH, command = self.rules,
                                 bg=self.button_background, fg=self.button_text_color, font=(self.button_text_font, 14, "bold"))

        self.quitbutton = Button(text="Quit", \
                                 width=self.buttonW, height=self.buttonH, command = self.quit,
                                 bg=self.button_background, fg=self.button_text_color, font=(self.button_text_font, 14, "bold"))

        self.mainmenu = Button(text="Main Menu", \
                                 width=self.buttonW, height=self.buttonH, command = self.main_menu,
                                 bg=self.button_background, fg=self.button_text_color, font=(self.button_text_font, 14, "bold"))
        self.next = Button(text="Next", \
                                 width=self.buttonW, height=self.buttonH, command = self.intro,
                                 bg=self.button_background, fg=self.button_text_color, font=(self.button_text_font, 14, "bold"))
        
        self.main_menu()
        
    def quit(self):
        self.parent.destroy()
    
    def rand_num(self):
        star = random.randint(1, 100)
        if (star >= 1 and star <= 6):
            return 1
        elif (star >= 7 and star <= 26):
            return random.randint(1, 2)
        elif (star >= 27 and star <= 56):
            return 3 + random.randint(1, 4)
        return 7 + random.randint(1, 4)
    
    def hide_buttons(self):
        self.roll1button.place_forget()
        self.roll10button.place_forget()
        self.quitbutton.place_forget()
        self.mainmenu.place_forget()
        self.next.place_forget()
        self.displayHist.place_forget()
        self.rulesbutton.place_forget()

    def show_buttons(self):
        self.roll1button.place(x=self.increment, y=self.button_height, anchor="center")
        self.roll10button.place(x=2*self.increment, y=self.button_height, anchor="center")
        self.displayHist.place(x=3*self.increment, y=self.button_height, anchor="center")
        self.rulesbutton.place(x=4*self.increment, y=self.button_height, anchor="center")
        self.quitbutton.place(x=5*self.increment, y=self.button_height, anchor="center")

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
    
    def start(self):
        self.show_buttons()
        self.count_rolls = 0
        self.canvas.create_text(int(self.width/2), int(self.height/4), text="Remaining wishes: "+str(self.wishes), font=(self.button_text_font, 40), fill="white")

    def main_menu(self):
        self.stop_animation = True
        self.mainmenu.place_forget()
        if self.canvas.find_all():
            self.parent.after(self.pause, self.main_menu)
            return
        
        [canvas_img, img] = self.animate("./mainmenu.gif")
        
        self.stop_animation = False
        self.update_gif(0, img, canvas_img, False)

        if (self.started):
            self.start()
        #else:
            # start message and button
        
    def remove(self):
        self.canvas.delete(self.errorID)
        self.errorID = None

    def roll_one(self):
        if self.wishes == 0: # and timer ran out
            self.errorID = self.canvas.create_text(int(self.width/2), 100, text=self.error, font=(self.button_text_font, 50, "bold"), fill="red")
            self.parent.after(3000, self.remove)
            return
        self.stop_animation = True
        self.max_rolls = 1
        self.intro()

    def roll_ten(self):
        if self.wishes == 0:
            self.errorID = self.canvas.create_text(int(self.width/2), 100, text=self.error, font=(self.button_text_font, 50, "bold"), fill="red")
            self.parent.after(3000, self.remove)
            return
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
        star_num = num
        if (num == 2 or num == 3):
            star_num = 2
        elif (num >= 4 and num <= 7):
            star_num = 3
        elif (num >= 8 and num <= 11):
            star_num = 4

        [canvas_img, img] = self.animate("./intros/"+str(star_num)+".gif")
        self.count_rolls += 1
        self.wishes -= 1
        self.characters[num] += 1

        self.stop_animation = False
        self.update_gif(0, img, canvas_img, True)

        if (num <= 3):
            self.character(num)
        else:
            self.repeat(num) # no intros for weapons

    def character(self, num):
        if self.canvas.find_all():
            self.parent.after(1, self.character, num)
            return

        # character intro animation info
        [canvas_img, img] = self.animate("./character_images/"+str(num)+".gif")
        # character intro
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

        [canvas_img, img] = self.animate("./repeat_images/"+str(num)+".gif")
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

        self.canvas.create_text(int(self.width/3), int(self.height/11), text="Characters", font=(self.button_text_font, 40, "bold"), fill="black", anchor=CENTER)
        self.canvas.create_text(2*int(self.width/3), int(self.height/11), text="Weapons", font=(self.button_text_font, 40, "bold"), fill="black", anchor=CENTER)
        for i in range(3):
            num = self.characters[i+1]
            self.canvas.create_text(int(self.width/3), (i+2)*(int(self.height/11)), text=self.char_names[i+1]+": "+str(num), font=(self.button_text_font, 20), fill="white", anchor=CENTER)
        for i in range(3,11):
            num = self.characters[i+1]
            self.canvas.create_text(2*int(self.width/3), (i-1)*(int(self.height/11)), text=self.char_names[i+1]+": "+str(num), font=(self.button_text_font, 20), fill="white", anchor=CENTER)

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