import os,json,re
import tkinter as tk
from tkinter import filedialog

from app_init_functions import *
from app_methods import *

def render_after(method):
    def new_method(self):
        method(self)
        self.render()
    return new_method

def unsave(method):
    def new_method(self):
        method(self)
        self.saved = False
    return new_method

def saved(method):
    def new_method(self):
        method(self)
        self.saved = True
    return new_method

class App:
    def __init__(self,root):
        self.root = root
        self.current_file_path = ""
        self.saved = True
        load_installation_path(self)
        create_panes(self)
        create_widgets(self)
        create_menubar(self)
        load_lastopen(self)
        bind_listening(self)

    @render_after
    @saved
    def new_file(self):
        new_file(self)

    @render_after
    @saved
    def open_file(self):
        open_file(self)

    @render_after
    @saved
    def save_file(self):
        save_file(self)
    @render_after
    @saved
    def save_as(self):
        save_as(self)
    
    @render_after
    @unsave
    def import_file(self):
        import_file(self)

    def render(self,show = True):
        render(self,show)
    
    def read_config(self):
        return read_config(self)
    def write_config(self,config):
        write_config(self,config)

    @render_after
    def select_all(self):
        select_all(self)
    @render_after
    def unselect_all(self):
        unselect_all(self)
    @render_after
    def select_interval(self):
        select_interval(self)
    @render_after
    def reverse_selection(self):
        reverse_selection(self)
    @render_after
    @unsave
    def remove_selected(self):
        remove_selected(self)
    @render_after
    @unsave
    def remove_all(self):
        remove_all(self)
    @render_after
    @unsave
    def move_up(self):
        move_up(self)
    @render_after
    @unsave
    def move_down(self):
        move_down(self)
    @render_after
    def copy_json(self):
        copy_json(self)
    @render_after
    def copy_text(self):
        copy_text(self)
    @render_after
    def copy_code(self):
        copy_code(self)
    @render_after
    def search_all(self):
        search_all(self)
    @render_after
    def toggle_toolbar(self):
        toggle_toolbar(self)
    
    @render_after
    def search_selected(self):
        search_selected(self)
    @render_after
    def copy_config_path(self):
        copy_config_path(self)

    def send_message(self):
        send_message(self)
if __name__ == "__main__":
    root = tk.Tk()
    root.title('ChatGUI')
    root.geometry("1366x768")
    app = App(root)
    root.mainloop()