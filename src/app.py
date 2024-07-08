import tkinter as tk
from tkinter import filedialog, colorchooser, ttk, messagebox
from clockWallpaper import ClockWallpaper

class Example(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        # Init the options
        self.img_prompt = tk.Label(self, text="Enter a number:", anchor="w")
        self.img_entry = tk.Entry(self)
        self.img_button = tk.Button(self, text="...", command = lambda: self.select_file("image"))
        
        self.font_prompt = tk.Label(self, text="Enter a number:", anchor="w")
        self.font_entry = tk.Entry(self)
        self.font_button = tk.Button(self, text="...", command = lambda: self.select_file("font"))
        
        self.monitor_combo = ttk.Combobox(self, values=["Monitor 1", "Monitor 2", "Monitor 3"])
        self.monitor_combo.current(0)
        self.monitor_combo.bind("<<ComboboxSelected>>", self.monitor_selected)
        
        self.position_hours_label = tk.Label(self, text="Position hours", anchor="w")
        self.position_hours_x = tk.Entry(self)
        self.position_hours_x.insert(0, "X")
        self.position_hours_y = tk.Entry(self)
        self.position_hours_y.insert(0, "Y")
        self.position_minutes_label = tk.Label(self, text="Position minutes", anchor="w")
        self.position_minutes_x = tk.Entry(self)
        self.position_minutes_x.insert(0, "X")
        self.position_minutes_y = tk.Entry(self)
        self.position_minutes_y.insert(0, "Y")
        self.position_split_label = tk.Label(self, text="Position split", anchor="w")
        self.position_split_x = tk.Entry(self)
        self.position_split_x.insert(0, "X")
        self.position_split_y = tk.Entry(self)
        self.position_split_y.insert(0, "Y")
        
        self.color = tk.Button(self, text="Submit", command = self.choose_color)
        self.output = tk.Label(self, text="")

        # Show the options 
        self.img_prompt.pack(side="top", fill="x")
        self.img_entry.pack(side="top", fill="x", expand=True)
        self.img_button.pack(side="top", fill="x", expand=True)
        
        self.font_prompt.pack(side="top", fill="x")
        self.font_entry.pack(side="top", fill="x", expand=True)
        self.font_button.pack(side="top", fill="x", expand=True)
        
        self.monitor_combo.pack(side="top", fill="x", expand=True)
        
        self.position_hours_label.pack(side="top", fill="x")
        self.position_hours_x.pack(side="top", fill="x", expand=True)
        self.position_hours_y.pack(side="top", fill="x", expand=True)
        self.position_minutes_label.pack(side="top", fill="x")
        self.position_minutes_x.pack(side="top", fill="x", expand=True)
        self.position_minutes_y.pack(side="top", fill="x", expand=True)
        self.position_split_label.pack(side="top", fill="x")
        self.position_split_x.pack(side="top", fill="x", expand=True)
        self.position_split_y.pack(side="top", fill="x", expand=True)
        

        
        # TODO add the rest of the options (color, size)
        self.output.pack(side="top", fill="x", expand=True)
        self.prompt2.pack(side="top", fill="x")
        self.button.pack(side="top", fill="x", expand=True)
        self.prompt3.pack(side="top", fill="x")
        self.color.pack(side="top", fill="x", expand=True)
        self.submit.pack(side="right")
        
        self.monitor_combo.pack(side="top", fill="x", expand=True)

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
        
    def select_file(self, type):
        #https://pythonspot.com/tk-file-dialogs/
        #ask the user to select a file, then we get the ful path
        file = filedialog.askopenfilename(title="Select File")
        file = file.replace("/", "\\")
        clockWallpaper = ClockWallpaper()
        if type == "image":
            file_ok = clockWallpaper.check_image(file)
        elif type == "font":
            file_ok = clockWallpaper.check_font(file)
        while not file_ok and file:
            message = f"Selected {type} is incompatible. Please choose a different {type}."
            title = "Compatibility Warning"
            messagebox.showwarning(title, message)
            
            file = filedialog.askopenfilename(title="Select File")
            if type == "image":
                file_ok = clockWallpaper.check_image(file)
            elif type == "font":
                file_ok = clockWallpaper.check_font(file)
        if type == "image":
            self.img_entry.delete(0, "end")
            self.img_entry.insert(0, file)
        elif type == "font":
            self.font_entry.delete(0, "end")
            self.font_entry.insert(0, file)
        
    def choose_color(self):
        #https://pythonspot.com/tk-color-picker/
        #ask the user to select a color
        color = colorchooser.askcolor()
        print(color)
        
    def monitor_selected(self, event):
        #https://pythonspot.com/tk-drop-down-list/
        #get the selected value from the combobox
        monitor_id = self.monitor_combo.current()
        print(monitor_id)
        
    def __verify_inputs(self):
        # TODO Verify that all the inputs are correct
        pass

# if this is run as a program (versus being imported),
# create a root window and an instance of our example,
# then start the event loop

if __name__ == "__main__":
    root = tk.Tk()
    Example(root).pack(fill="both", expand=True)
    root.mainloop()