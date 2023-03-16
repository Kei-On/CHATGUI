import tkinter as tk
import re
class SearchWindow(tk.Toplevel):
    def __init__(self,app,mode = "all"):
        super().__init__(master=app.root)
        self.mode = mode
        self.app = app
        self.title("Search")
        self.geometry("250x60")
        self.resizable(False, False)
        self.wm_attributes("-topmost", 1)
        self.create_widgets()

    def create_widgets(self):
        
        frame1 = tk.Frame(self)
        frame1.pack(side = "top")
        self.all_radio = tk.Radiobutton(frame1, text="Search all", variable=self.mode, value="all")
        self.all_radio.pack(side = "left")
        self.selected_radio = tk.Radiobutton(frame1, text="Search selected", variable=self.mode, value="selected")
        self.selected_radio.pack(side = "left")
        if self.mode == "all":
            self.all_radio.select()
        else:
            self.selected_radio.select()

        frame2 = tk.Frame(self)
        frame2.pack(side = "top")
        self.pattern_label = tk.Label(frame2, text="Pattern:")
        self.pattern_label.pack(side = "left")
        self.pattern_entry = tk.Entry(frame2)
        self.pattern_entry.pack(side = "left")
        self.search_button = tk.Button(frame2, text="search",command=self.search)
        self.search_button.pack(side = "left")

    def search(self):
        if self.mode == "all":
            searched = range(self.app.listbox.size())
        else:
            searched = self.app.listbox.curselection()
        self.app.listbox.selection_clear(0, tk.END)
        pattern = r'' + self.pattern_entry.get()
        for index in searched:
            match = re.search(pattern, self.app.listbox.get(index))
            if match:
                self.app.listbox.selection_set(index)
        self.app.render()

if __name__ == "__main__":
    win = tk.Tk()
    #Set the geometry and title of tkinter Main window
    win.geometry("750x250")
    win.title("Main Window")
    search = SearchWindow(win)
    win.mainloop()