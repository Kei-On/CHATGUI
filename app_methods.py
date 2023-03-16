import json,os,re
from tkinter import filedialog
import tkinter as tk
from SearchWindow import SearchWindow
import openai

def new_file(self):
    self.current_file_path = ""
    remove_all(self)

def open_file(self):
    try:
        filename = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        self.current_file_path = filename
        with open(filename,"r",encoding="utf-8") as f:
            data = json.load(f)
        print("Opened file at {}. ".format(self.current_file_path))
        self.listbox.delete(0,tk.END)
        for message in data:
            item = json.dumps(message)
            self.listbox.insert(tk.END,item)
            self.listbox.selection_set(tk.END)
        config = self.read_config()
        config["History"]["Open"].append(self.current_file_path)
        self.write_config(config)
        self.root.title('ChatGUI {}'.format(self.current_file_path))
    except:
        pass

def save_file(self):
    with open(self.current_file_path, "w",encoding="utf-8") as f:
        data = [json.loads(item) for item in self.listbox.get(0,tk.END)]
        json.dump(data,f,indent=4)

def save_as(self):
    file_path = filedialog.asksaveasfilename(defaultextension=".json",filetypes=(("Json", '*.json'),))
    try:
        with open(file_path, "w",encoding="utf-8") as f:
            data = [json.loads(r''+item) for item in self.listbox.get(0,tk.END)]
            json.dump(data,f,indent=4)
        self.current_file_path = file_path
    except:
        pass

def import_file(self):
    try:
        filename = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        with open(filename,"r",encoding="utf-8") as f:
            data = json.load(f)
        for message in data:
            item = json.dumps(message)
            self.listbox.insert(tk.END,item)
            self.listbox.selection_set(tk.END)
        config = self.read_config()
        config["History"]["Open"].append(self.current_file_path)
        self.write_config(config)
        self.root.title('ChatGUI {}'.format(self.current_file_path))
    except:
        pass

def select_all(self):
    for index in range(self.listbox.size()):
        self.listbox.select_set(index)

def unselect_all(self):
    for index in range(self.listbox.size()):
        self.listbox.selection_clear(index)

def remove_selected(self):
    count = 0
    for index in self.listbox.curselection():
        self.listbox.delete(index-count)
        count = count + 1

def remove_all(self):
    for index in range(self.listbox.size()):
        self.listbox.delete(tk.END)

def reverse_selection(self):
    current_selection = self.listbox.curselection()
    for i in range(self.listbox.size()):
        if i in current_selection:
            self.listbox.selection_clear(i)
        else:
            self.listbox.selection_set(i)

def select_interval(self):
    selected_indices = self.listbox.curselection()
    if len(selected_indices) >= 2:
        first_index = selected_indices[0]
        last_index = selected_indices[-1]
        self.listbox.selection_clear(0, tk.END)
        self.listbox.selection_set(first_index, last_index)

def move_up(self):
        selected_indices = self.listbox.curselection()
        if len(selected_indices)==0:
            return
        if selected_indices[0] == 0:
            return
        for index in selected_indices:
            current_text = self.listbox.get(index)
            self.listbox.delete(index)
            self.listbox.insert(index-1, current_text)
            self.listbox.selection_set(index-1)

def move_down(self):
        # Get the selected indices in reverse order
        selected_indices = self.listbox.curselection()[::-1]
        if len(selected_indices)==0:
            return
        if selected_indices[0] == self.listbox.size()-1:
            return
        for index in selected_indices:
            current_text = self.listbox.get(index)
            self.listbox.delete(index)
            self.listbox.insert(index+1, current_text)
            self.listbox.selection_set(index+1)

def copy_json(self):
    selected_indices = self.listbox.curselection()

    data = [json.loads(r''+item) for item in self.listbox.get(0,tk.END)]
    text = json.dumps(data,indent=4)
    
    self.root.clipboard_clear()
    self.root.clipboard_append(text)

def copy_text(self):
    self.root.clipboard_clear()
    self.root.clipboard_append(render(self,False))

def copy_code(self):
    text = ""
    selected_indices = self.listbox.curselection()
    for i in selected_indices:
        message = json.loads(self.listbox.get(i))
        if message["role"] == "assistant":
            text += message['content']

    pattern = r"\`\`\`.*\n((.|\n)*?)\`\`\`"
    matches = re.findall(pattern, text)
    ans = ""
    for match in matches:
        ans += match[0]
    self.root.clipboard_clear()
    self.root.clipboard_append(ans)

def search_all(self):
    SearchWindow(self,"all")

def search_selected(self):
    SearchWindow(self,"selected")

def copy_config_path(self):
    filename = os.path.join(self.installation_path,"config.json")
    self.root.clipboard_clear()
    self.root.clipboard_append(filename)

def toggle_toolbar(self):
    config = read_config(self)
    if config["ShowToolbar"]:
        config["ShowToolbar"] = False
        write_config(self,config)

        self.toolbar.destroy()
        self.toolbar = tk.Frame(self.frameL)
        self.toolbar.pack(side = "left")

    else:
        config["ShowToolbar"] = True
        write_config(self,config)

        toolbar_string = config["Toolbar"]
        tool_groups = [s.split(",") for s in toolbar_string.split(";")]

        for tool_group in tool_groups:
            for i,tool_name in enumerate(tool_group):
                command = None
                for menu in self.menubar.winfo_children():
                    for index in range(menu.index('end')):
                        try:
                            if menu.entryconfig(index, 'label')[-1] == tool_name:
                                command = menu.entrycget(index, 'command')
                        except:
                            pass
                button = tk.Button(self.toolbar, text=tool_name,command = command)
                if i<len(tool_group)-1:
                    button.pack(fill="x")
                else:
                    button.pack(fill="x",pady=(0, config["ToolbarSeparator"]))
            


def render(self,show = True):
    text = ""
    config = self.read_config()
    for i in self.listbox.curselection():
        message = json.loads(self.listbox.get(i))
        text += "[{}] {}\n\n".format(config["Names"][message["role"]],message["content"])

    if show:
        self.textbox.config(state="normal")
        self.textbox.delete('1.0', 'end')
        self.textbox.insert('1.0', text)
        self.textbox.config(state="disabled")

        w = len(text.split())
        l = len(text) - text.count(" ")
        t = int((w*1.33+l*0.25)/2)
        out = config['ModelConfig']['max_tokens']
        x = {True:"<",False:">"}[t+out<4097]
        y = {True:"",False:"!!!"}[t+out<4097]
        count = "token ≈ {} + {} = {} {} 4097{}".format(t,out,t+out,x,y)

        if not(self.saved):
            self.root.title('ChatGUI {} (unsaved)  ----  {}'.format(self.current_file_path,count))
        else:
            self.root.title('ChatGUI {}  ----  {}'.format(self.current_file_path,count))
        



    return text

def read_config(self):
    config_path = os.path.join(self.installation_path,"config.json")
    with open(config_path,"r",encoding="utf8") as f:
        data = json.load(f)
    return data

def write_config(self,config):
    config_path = os.path.join(self.installation_path,"config.json")
    with open(config_path,"w",encoding="utf-8") as f:
        json.dump(config,f,indent=4)


def get_chatlog_all(self):
    return [r""+item for item in self.listbox.get(0, tk.END)]
    
def get_chatlog_selected(self):
    return [r""+item for item in self.listbox.get(self.listbox.curselection())]

def send_message(self):
    model_input = []
    selected_indices = self.listbox.curselection()

    for i in selected_indices:
        model_input.append(json.loads(self.listbox.get(i)))
    text = self.messagebox.get('1.0', 'end')
    text = re.sub(r'[ \n]+$','',text)
    text = re.sub(r'^[ \n]+','',text)
    if(not(text=="")):
        message = {"role":"user","content":format(text)}
        model_input.append(message)

    config = read_config(self)
    if config["ApiKey"] == "":
        openai.api_key = os.getenv("OPENAI_API_KEY")

    para = config["ModelConfig"]

    response = openai.ChatCompletion.create(
        model=para["model"],  # The name of the OpenAI chatbot model to use
        messages=model_input,   # The conversation history up to this point, as a list of dictionaries
        max_tokens=para["max_tokens"],        # The maximum number of tokens (words or subwords) in the generated response
        stop=para["stop"],              # The stopping sequence for the generated response, if any (not used here)
        temperature=para["temperature"],        # The "creativity" of the generated response (higher temperature = more creative)
    )

    # Find the first response from the chatbot that has text in it (some responses may not have text)
    for choice in response.choices:
        if "text" in choice:
            return choice.text

    # If no response with text is found, return the first response's content (which may be empty)
    reply = response.choices[0].message.content
    reply = re.sub(r'[ \n]+$','',reply)
    reply = re.sub(r'^[ \n]+','',reply)
    reply = {"role":"assistant","content":reply}    

    if(not(text=="")):
        self.listbox.insert("end", json.dumps(message))
        self.saved = False

    self.listbox.selection_set(self.listbox.size()-1)
    self.listbox.insert("end", json.dumps(reply))
    self.saved = False

    self.listbox.selection_set(self.listbox.size()-1)
    self.messagebox.delete('1.0', 'end')
    render(self)
    
    self.textbox.see(tk.END)