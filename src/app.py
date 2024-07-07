import tkinter as tk
from tkinter import filedialog, colorchooser, ttk

class Example(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        # Init the options
        self.prompt_img = tk.Label(self, text="Enter a number:", anchor="w")
        self.entry_img = tk.Entry(self)
        self.button_img = tk.Button(self, text="Submit", command = self.calculate)
        
        self.prompt_font = tk.Label(self, text="Enter a number:", anchor="w")
        self.entry_font = tk.Entry(self)
        self.button_font = tk.Button(self, text="Submit", command = self.calculate)
        
        self.combo_monitor = ttk.Combobox(self, values=["Monitor 1", "Monitor 2", "Monitor 3"])
        self.combo_monitor.current(0)
        self.combo_monitor.bind("<<ComboboxSelected>>", self.monitor_selected)
        
        self.position_hours_label = tk.Label(self, text="Position hours", anchor="w")
        self.position_hours_x = tk.Entry(self)
        self.position_hours_x.insert(0, "X")
        self.position_hours_y = tk.Entry(self)
        self.position_hours_y.insert(0, "Y")
        self.position_minutes_label = tk.Label(self, text="Position minutes", anchor="w")
        self.position_minutes_x = tk.Entry(self)
        self.position_minutes_y = tk.Entry(self)
        self.position_split_label = tk.Label(self, text="Position split", anchor="w")
        self.position_split_x = tk.Entry(self)
        self.position_split_y = tk.Entry(self)
        
        self.prompt2 = tk.Label(self, text="Select a repo:", anchor="w")
        self.prompt3 = tk.Label(self, text="Select a color:", anchor="w")
        self.submit = tk.Button(self, text="Submit", command = self.calculate)
        self.button = tk.Button(self, text="Submit", command = self.select_file)
        self.color = tk.Button(self, text="Submit", command = self.choose_color)
        self.output = tk.Label(self, text="")

        # Show the options 
        self.prompt_img.pack(side="top", fill="x")
        self.entry_img.pack(side="top", fill="x", expand=True)
        self.button_img.pack(side="top", fill="x", expand=True)
        
        self.prompt_font.pack(side="top", fill="x")
        self.entry_font.pack(side="top", fill="x", expand=True)
        self.button_font.pack(side="top", fill="x", expand=True)
        
        self.combo_monitor.pack(side="top", fill="x", expand=True)
        
        self.position_hours_label.pack(side="top", fill="x")
        self.position_hours_x.pack(side="top", fill="x", expand=True)
        self.position_hours_y.pack(side="top", fill="x", expand=True)
        self.position_minutes_label.pack(side="top", fill="x")
        self.position_minutes_x.pack(side="top", fill="x", expand=True)
        self.position_minutes_y.pack(side="top", fill="x", expand=True)
        self.position_split_label.pack(side="top", fill="x")
        self.position_split_x.pack(side="top", fill="x", expand=True)
        self.position_split_y.pack(side="top", fill="x", expand=True)
        
        
        
        
        self.output.pack(side="top", fill="x", expand=True)
        self.prompt2.pack(side="top", fill="x")
        self.button.pack(side="top", fill="x", expand=True)
        self.prompt3.pack(side="top", fill="x")
        self.color.pack(side="top", fill="x", expand=True)
        self.submit.pack(side="right")
        
        self.combo_monitor.pack(side="top", fill="x", expand=True)

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
        
    def select_file(self):
        #https://pythonspot.com/tk-file-dialogs/
        #ask the user to select a file, then we get the ful path
        directory = filedialog.askopenfilename(title="Select File")
        print(directory)
        
    def choose_color(self):
        #https://pythonspot.com/tk-color-picker/
        #ask the user to select a color
        color = colorchooser.askcolor()
        print(color)
        
    def monitor_selected(self, event):
        #https://pythonspot.com/tk-drop-down-list/
        #get the selected value from the combobox
        monitor_id = self.combo_monitor.current()
        print(monitor_id)

# if this is run as a program (versus being imported),
# create a root window and an instance of our example,
# then start the event loop

if __name__ == "__main__":
    root = tk.Tk()
    Example(root).pack(fill="both", expand=True)
    root.mainloop()