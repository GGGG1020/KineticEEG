"""Training Data Getter"""
import tkinter
import tkinter.ttk as tk

class TrainerApp(tkinter.Tk):
    def __init__(self, parent):
        tkinter.Tk.__init__(self, parent)
        self.parent=parent
        self.minsize(width=666, height=666)
        self.initialize()
    def initialize(self):
        self.grid()
        self.closebtn=tk.Button(self, text="close")
        self.closebtn.grid(column=10, row=3, )
if __name__=='__main__':
    app=TrainerApp(None)
    app.title("Trainer")
