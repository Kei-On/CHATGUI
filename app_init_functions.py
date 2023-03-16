import os,json,re
import tkinter as tk

default_config = {
    "ApiKey":"",
    "EnterToSend": False,
    "AutoPilot":False,
    "Names":{
        "system": "System",
        "user": "User",
        "assistant": "Assistant",
    },
    "ModelConfig":{
        "model":"gpt-3.5-turbo",
        "max_tokens":1000,
        "stop": None,
        "temperature": 0.3,
    },
    "History":{
        "Open":[],
    },
    "Toolbar": "Open,Save,Save as;Select all,Unselect all,Select interval,Reverse selection;Move up,Move down,Remove selected,Remove all;Copy json,Copy text,Copy code",
    "ToolbarSeparator":20,
    "ShowToolbar":True,
}

def load_installation_path(self):
    self.installation_path = os.getenv('CHATGUI_PATH')
    if self.installation_path is None:
        self.installation_path = os.getcwd()
        print("Set installation_path = {}. ".format(os.getcwd()))
        config_path = os.path.join(self.installation_path,"config.json")
        if not(os.path.isfile(config_path)):
            print("Config file not found, create one at: {}".format(config_path))
            with open(config_path,"w") as f:
                json.dump(default_config,f,indent=4)
        else:
            print("Config file at: {}".format(config_path))
    else:
        print("Load env CHATGUI_PATH == {}. ".format(os.getenv('CHATGUI_PATH')))
    


def create_panes(self):
    '''   Pane2
     _______________
    |FrameL | FrameR|
    |_______|_______|  Pane1
    |     FrameB    |
    |_______________|
    '''
    self.pane1 = tk.PanedWindow(self.root, orient="vertical", sashwidth=10, sashrelief="ridge")
    self.pane2 = tk.PanedWindow(self.pane1, orient="horizontal", sashwidth=10, sashrelief="ridge")
    self.frameL = tk.Frame(self.pane2)
    self.frameR = tk.Frame(self.pane2)
    self.frameB = tk.Frame(self.pane1)

    self.pane1.pack(fill="both", expand=True)
    self.pane1.add(self.pane2)
    self.pane1.add(self.frameB)
    self.pane2.add(self.frameL)
    self.pane2.add(self.frameR)

    def set():
        self.pane1.sash_place(0, 0, 500)
        self.pane2.sash_place(0, 500, 0)
    self.root.after(100,set)

def create_widgets(self):
    self.toolbar = tk.Frame(self.frameL)
    self.toolbar.pack(side = "left")
    self.listbox = tk.Listbox(
        self.frameL, 
        selectmode="multiple",
        selectbackground="lightgreen", 
        selectforeground="black",
        exportselection=False)
    self.listbox.pack(side = "right",fill="both", expand=True)

    scrollbar = tk.Scrollbar(self.frameR)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    self.textbox = tk.Text(self.frameR,borderwidth=2,
        yscrollcommand=scrollbar.set,state = "disabled")
    self.textbox.pack(side="left", fill="both", expand=True)
    scrollbar.config(command=self.textbox.yview)

    self.messagebox = tk.Text(self.frameB,width=50, height=10)
    self.messagebox.pack(side="left", fill="both", expand=True)

    self.send_button = tk.Button(self.frameB, text="Send", width = 10,command=self.send_message)
    self.send_button.pack(fill="both", expand=True)

def create_menubar(self):
    menubar = tk.Menu(self.root)
    self.menubar = menubar
    self.root.config(menu=menubar)

    file_menu = tk.Menu(menubar)
    self.file_menu = file_menu
    menubar.add_cascade(label="File", menu=file_menu)
    file_menu.add_command(label="New",command=self.new_file)
    file_menu.add_command(label="Open",command=self.open_file)
    file_menu.add_command(label="Save",command = self.save_file)
    file_menu.add_command(label="Save as",command = self.save_as)
    file_menu.add_command(label="Import",command = self.import_file)

    edit_menu = tk.Menu(menubar)
    self.edit_menu = edit_menu
    menubar.add_cascade(label="Edit", menu=edit_menu)
    edit_menu.add_command(label="Select all", command = self.select_all)
    edit_menu.add_command(label="Unselect all", command = self.unselect_all)
    edit_menu.add_command(label="Select interval", command = self.select_interval)
    edit_menu.add_command(label="Reverse selection", command = self.reverse_selection)
    edit_menu.add_command(label="Move up", command = self.move_up)
    edit_menu.add_command(label="Move down", command = self.move_down)
    edit_menu.add_command(label="Remove selected", command = self.remove_selected)
    edit_menu.add_command(label="Remove all", command = self.remove_all)
    edit_menu.add_command(label="Copy json", command = self.copy_json)
    edit_menu.add_command(label="Copy text", command = self.copy_text)
    edit_menu.add_command(label="Copy code", command = self.copy_code)
    edit_menu.add_command(label="Search from all", command = self.search_all)
    edit_menu.add_command(label="Search from selected", command = self.search_selected)

    settings_menu = tk.Menu(menubar)
    self.edit_menu = edit_menu
    menubar.add_cascade(label="Settings", menu=settings_menu)
    settings_menu.add_command(label="Toggle toolbar", command = self.toggle_toolbar)
    settings_menu.add_command(label="copy config path", command = self.copy_config_path)

    self.toggle_toolbar()
    self.toggle_toolbar()


def load_lastopen(self):
    config = self.read_config()
    try:
        history = config["History"]["Open"]
        if len(history) > 0:
            self.current_file_path = history[-1]
            with open(history[-1],"r",encoding="utf-8") as f:
                data = json.load(f)
            self.listbox.delete(0,tk.END)
            for message in data:
                item = json.dumps(message)
                self.listbox.insert(tk.END,item)
                self.listbox.selection_set(tk.END)

            self.render()
            self.root.title('ChatGUI {}'.format(self.current_file_path))
    except:
        config["History"]["Open"].pop()
        self.write_config(config)
        load_lastopen(self)

def bind_listening(self):
    def on_select(event):
        self.render()
    def on_deselect(event):
        self.render()
    # Bind the on_select function to the Listbox widget's selection event
    self.listbox.bind('<<ListboxSelect>>', on_select)
    # Bind the on_deselect function to the Listbox widget's deselection event
    self.listbox.bind('<<ListboxUnselect>>', on_deselect)

    def send_callback(event):
        if event.keysym == 'Return' and event.state == 0x1:
            self.send_button.invoke()
    self.root.bind('<Shift-Return>', send_callback)

