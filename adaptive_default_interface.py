import tkinter as tk

class Window:
    def __init__(self, master):
        self.master = master
        f = tk.Frame(self.master)

        b = tk.Button(f, text="Close Window", command=self.quit)
        b.pack(pady=30)
        
        f.pack()

    def exit_on_error(error_string):
        """
            Provide a useful error message to the user and gracefully exit.
        """
    
    def quit(self):
        self.master.destroy()


root = tk.Tk()
root.geometry('200x150')
window = Window(root)
root.mainloop()

### WHAT IS OUR WORKFLOW GOING TO LOOK LIKE?

# what data do we want to collect?