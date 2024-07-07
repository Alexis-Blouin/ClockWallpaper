import tkinter as tk
from tkinter import filedialog, colorchooser

class Example(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        # create a prompt, an input box, an output label,
        # and a button to do the computation
        self.prompt = tk.Label(self, text="Enter a number:", anchor="w")
        self.entry = tk.Entry(self)
        self.prompt = tk.Label(self, text="Select a repo:", anchor="w")
        self.prompt = tk.Label(self, text="Select a repo:", anchor="w")
        self.submit = tk.Button(self, text="Submit", command = self.calculate)
        self.button = tk.Button(self, text="Submit", command = self.select_directory)
        self.color = tk.Button(self, text="Submit", command = self.choose_color)
        self.output = tk.Label(self, text="")

        # lay the widgets out on the screen. 
        self.prompt.pack(side="top", fill="x")
        self.entry.pack(side="top", fill="x", padx=20)
        self.output.pack(side="top", fill="x", expand=True)
        self.button.pack(side="top", fill="x", expand=True)
        self.color.pack(side="top", fill="x", expand=True)
        self.submit.pack(side="right")

    def calculate(self):
        # get the value from the input widget, convert
        # it to an int, and do a calculation
        try:
            i = int(self.entry.get())
            result = "%s*2=%s" % (i, i*2)
        except ValueError:
            result = "Please enter digits only"

        # set the output widget to have our result
        self.output.configure(text=result)
        
    def select_directory(self):
        #https://pythonspot.com/tk-file-dialogs/
        #ask the user to select a directory
        directory = filedialog.askopenfilename(title="Select Folder")
        #ask the user to select a file, then we get the ful path
        directory = filedialog.askopenfilename(title="Select File")
        print(directory)
        
    def choose_color(self):
        #https://pythonspot.com/tk-color-picker/
        #ask the user to select a color
        color = colorchooser.askcolor()
        print(color)

# if this is run as a program (versus being imported),
# create a root window and an instance of our example,
# then start the event loop

if __name__ == "__main__":
    root = tk.Tk()
    Example(root).pack(fill="both", expand=True)
    root.mainloop()