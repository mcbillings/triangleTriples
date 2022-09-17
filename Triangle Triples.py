from tkinter import *
from tkinter import simpledialog ##Imported seperately because simpledialog not recognized otherwise
import math
import turtle

e1 = 0
e2 = 0
e3 = 0 ##Defined outside of the class to avoid having the variables undefined at the module level

counter = 0

class Window(Frame): ##Things we use on windows
    def __init__(self, master = None): 
        """Define initializing window"""
        Frame.__init__(self, master)
        self.master = master ##Main window, Master widgit
        self.init_window() ##Function created below
        
    def init_window(self):
        """Initilize Window inside of the frame"""
        self.master.title("Triangle Triples") ##Changes title of window
        self.pack(fill=BOTH, expand=1) ##Fills entire window when expanded
        
        menu = Menu(self.master) ##Menu of the main window
        self.master.config(menu=menu) ##Init menu
        
        file = Menu(menu)##Init file objext
        file.add_command(label = "Exit", command = self.client_exit) ##Assign Exit
        menu.add_cascade(label="File", menu=file)
        
        greeting = Label(self, text = "Hi! Welcome to Triangle Triples! \nPlease enter the side lenths of your triangle below.", height = 5, width = 100, font = 100)
        greeting.pack()##Displayes our Greeting on the window


        lengths_button = Button(self, text = "Enter Side Lengths...", command=self.check_button)
        lengths_button.pack() ##Displays our button on the window
        
    def client_exit(self):
        """Provides a function for the exit in our file menu"""
        exit()
        
    def check_button(self):
        """Clears the window if the button if pressed twice"""
        global counter ##Global so the class can overwrite the variable outside of the class
        counter += 1
        if counter >= 2:
            area_display.pack_forget() ##Removes the packed items in area_display
            canvas.pack_forget() ##Removes the packed items in canvas
        self.enter_lengths() ##Continues to the next function in the sequence
    
    def enter_lengths(self):
        """Creates a child window for the user to enter their side lengths in"""
        global e1 
        global e2 
        global e3 ##Lets the function write over the variables defined outside of the class
        e1 = simpledialog.askfloat("Input Side Length", "Side 1")
        e2 = simpledialog.askfloat("Input Side Length", "Side 2")
        e3 = simpledialog.askfloat("Input Side Length", "Side 3")##Asks the user for the side lengths
        self.check_if_triangle(e1, e2, e3)
        
    def check_if_triangle(self, e1, e2, e3):    
        if e1 + e2 > e3 and e1 + e3 > e2 and e2 + e3 > e1: ##Makes sure the triangle is valid
            self.calculate_area(e1, e2, e3) ##Moves to calculate the area of the valid triangle
        else:
            is_triangle = Label(self, text = "This is not a triangle.")
            is_triangle.pack() ##Informs the user their triangle is not valid and does not move forward in the process
        root.update()
    
    def calculate_area(self, e1, e2, e3):
        """Calculates the area of a valid triangle using Herons Formula"""
        p = (e1 + e2 + e3)/2 ##Half the perimeter
        area = math.sqrt(p*(p-e1)*(p-e2)*(p-e3)) ##Heron's Formula
        global area_display ##Global because it is used in button_checking, not passed because command= in buttons doesn't handle parameters well
        area_display = Label(self, text = "The area is " + str(area) + " units.", height = 5, width = 100, font = 100)
        area_display.pack()
        self.calculate_angles(e1, e2, e3)

    def calculate_angles(self, e1, e2, e3):
        """Calculates the areas of the triangle"""
        angle_e2 = round(math.degrees(math.acos((e2**2 + e3**2 - e1**2)/(2*e2*e3))))
        angle_e3 = round(math.degrees(math.acos((e3**2 + e1**2 - e2**2)/(2*e3*e1))))
        angle_e1 = round(math.degrees(math.acos((e1**2 + e2**2 - e3**2)/(2*e1*e2))))
        self.draw_triangle(angle_e1, angle_e2, angle_e3)
    
    def draw_triangle(self, angle_e1, angle_e2, angle_e3):
        """Draws Triangle on the canvas"""
        global canvas ##Global because it is used in button_checking, not passed because command= in buttons doesn't handle parameters well
        canvas = Canvas(width = 500, height = 500)
        canvas.pack()
        canvas.create_rectangle(200, 200, 400, 400) ##Creates a canvas for Turtle   
        
        t = turtle.RawTurtle(canvas)
        
        lengths = [e1, e2, e3]
        if max(lengths)<10:
            side_1 = e1*50
            side_2 = e2*50
            side_3 = e3*50
        elif max(lengths)<50:
            side_1 = e1*10
            side_2 = e2*10
            side_3 = e3*10
        elif max(lengths)<100:
            side_1 = e1*5
            side_2 = e2*5
            side_3 = e3*5
        elif max(lengths)<150:
            side_1 = e1*2
            side_2 = e2*2
            side_3 = e3*2
        else:
            side_1 = e1
            side_2 = e2
            side_3 = e3
            
        x_pos = 0 - side_1/2 ##Centers triangle on x axis
        y_pos = 0 - side_2/2 ##About Centers triangle on y axis
        
        t.up()
        t.goto(x_pos, y_pos)
        t.down()
        t.forward(side_1)
        t.lt(180-angle_e1)
        t.forward(side_2)
        t.lt(180-angle_e2)
        hx, hy = t.pos()
        t.forward(side_3) ##Draws the triangle
        
        canvas.create_text(0,-y_pos + 10, text = str(e1) + " units")
        canvas.create_text(x_pos, -y_pos/4, text = str(e2) + " units")
        canvas.create_text(-x_pos + 10, -y_pos/4, text = str(e3) + " units")
        canvas.create_text(-x_pos - 20 , -y_pos - 10, text = str(angle_e1) + "°")
        canvas.create_text(x_pos + 20, -y_pos - 10, text = str(angle_e2) + "°")
        canvas.create_text(hx, -hy + 15, text = str(angle_e3) + "°")
        

## CREATES WINDOW WITH ATTRIBUTES SPECIFIED IN WINDOW CLASS
## --------------------------------------------------------
root = Tk() ##Root window
root.state('zoomed') ##Starts window maxumized
root.configure(background="white")
app = Window(root) ##Referencing out window class, making root window
root.mainloop() ##Calls our window