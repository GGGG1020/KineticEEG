"""Training Data Getter"""
import tkinter
import tkinter.ttk as tk
class TrainingCore:
    SENSORS_OF_INTEREST=["FC5","F3","F4","FC6"]
    def __init__(self):
        pass
class TrainerApp(tkinter.Tk):
    def __init__(self, parent, TrainingCore):
        tkinter.Tk.__init__(self, parent)
        self.parent=parent
        self.minsize(width=400, height=400)
        self.maxsize(width=400, height=400)
        self.initialize()
    def initialize(self):
        self.closebtn=tk.Button(self, text="close")
        self.closebtn.place(x=325,y=0)
        self.train_kickbtn=tk.Button(self, text="Train Kick")
        self.train_kickbtn.place(x=120, y=100)
        self.train_armbtn=tk.Button(self, text="Train Arm")
        self.train_armbtn.place(x=200, y=100)
        self.train_nuetralbtn=tk.Button(self, text="Train Nuetral")
        self.train_nuetralbtn.place(x=160, y=130)  
if __name__=='__main__':
    core=TrainingCore()
    app=TrainerApp(None,core)
    app.title("Trainer")
    app.mainloop()
