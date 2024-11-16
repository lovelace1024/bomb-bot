from tkinter import *
root = Tk()
root.title("Skull mat")
root.geometry("800x600")
bg = PhotoImage(file = "skull/rastamat1.png")
w = 600
h = 400
x = w/2
y = h/2
my_canvas = Canvas(root,width=w, height=h)
my_canvas.pack(fill = "both", expand = True)
my_canvas.create_image( 0, 0, image = bg, anchor = "nw")
root.mainloop()
