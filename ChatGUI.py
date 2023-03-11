import tkinter as tk
from tkinter import filedialog
import openai
import os
import json
import re

class ChatHistoryBox(tk.Frame):
    def __init__(self, master, render_text,APP_config_input,config_input, messages):
        super().__init__(master)

        self.render_text = render_text
        self.APP_config_input = APP_config_input
        self.config_input = config_input
        self.messages = messages

        # Create a sub-frame for the buttons
        self.button_frame = tk.Frame(self)
        self.button_frame.pack(side="left")
        # Create a sub-frame for the Listbox
        self.listbox_frame = tk.Frame(self)
        self.listbox_frame.pack(side="left", fill="both", expand=True)

        # Create a Listbox widget and add the messages to it
        self.listbox = tk.Listbox(self.listbox_frame, selectmode="multiple",selectbackground="lightgreen", selectforeground="black",exportselection=False)
        for message in self.messages:
            self.listbox.insert("end", message)
        # Add the Listbox to the left side of the pane, and fill and expand to take up all available space
        self.listbox.pack(side="left", fill="both", expand=True)



        self.select_all_button = tk.Button(self.button_frame, text="Select All", command=self.select_all)
        self.select_all_button.pack(side="top",expand=True, fill="both")

        self.unselect_all_button = tk.Button(self.button_frame, text="Unselect All", command=self.unselect_all)
        self.unselect_all_button.pack(side="top",expand=True, fill="both", pady=(0, 20))

        self.select_between_button = tk.Button(self.button_frame, text="Select Interval", command=self.select_between)
        self.select_between_button.pack(side="top",expand=True, fill="both")

        self.reverse_selection_button = tk.Button(self.button_frame, text="Reverse Selection", command=self.reverse_selection)
        self.reverse_selection_button.pack(side="top",expand=True, fill="both")

        # Create a button for clearing selected messages
        self.clear_button = tk.Button(self.button_frame, text="Remove", command=self.clear_selected)
        self.clear_button.pack(side="top",expand=True, fill="both", pady=(0, 20))

        self.copy_button = tk.Button(self.button_frame, text="Copy JSON", command=self.copy_json)
        self.copy_button.pack(side="top",expand=True, fill="both")

        self.copy_button = tk.Button(self.button_frame, text="Copy Text", command=self.copy_text)
        self.copy_button.pack(side="top",expand=True, fill="both", pady=(0, 20))

        self.move_up_button = tk.Button(self.button_frame, text="Move Up", command=self.move_up)
        self.move_up_button.pack(side="top",expand=True, fill="both")

        self.move_up_button = tk.Button(self.button_frame, text="Move Down", command=self.move_down)
        self.move_up_button.pack(side="top",expand=True, fill="both", pady=(0, 20))
        
        self.clear_button = tk.Button(self.button_frame, text="Open", command=self.open_file)
        self.clear_button.pack(side="top",expand=True, fill="both")

        self.copy_button = tk.Button(self.button_frame, text="Save", command=self.save_file)
        self.copy_button.pack(side="top",expand=True, fill="both", pady=(0, 20))

        self.move_up_button = tk.Button(self.button_frame, text="Import", command=self.import_file)
        self.move_up_button.pack(side="top",expand=True, fill="both")

        self.move_up_button = tk.Button(self.button_frame, text="Export", command=self.export_file)
        self.move_up_button.pack(side="top",expand=True, fill="both")

    def check_selected(self):
        # Iterate over the indices of the currently selected items and set their background to light green
        for index in self.listbox.curselection():
            self.listbox.itemconfig(index, bg="lightgreen")
        self.render()

    def uncheck_selected(self):
        # Iterate over the indices of the currently selected items and set their background to white
        for index in self.listbox.curselection():
            self.listbox.itemconfig(index, bg="white")
        self.render()

    def select_all(self):
        # Iterate over all items in the Listbox and set their background to light green, and select them
        for index in range(self.listbox.size()):
            self.listbox.itemconfig(index, bg="white")
            self.listbox.select_set(index)
        self.render()

    def unselect_all(self):
        # Iterate over all items in the Listbox and set their background to white, and unselect them
        for index in range(self.listbox.size()):
            self.listbox.itemconfig(index, bg="white")
            self.listbox.selection_clear(index)
        self.render()

    def import_file(self):
        # Open a file dialog to select a JSON file
        filename = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])

        # Read the JSON file as a list of dictionaries
        with open(filename,"r",encoding="utf8") as f:
            new_messages = json.load(f)

        # Append each dictionary to the Listbox
        for message in new_messages:
            self.listbox.insert("end", json.dumps(message))
            self.listbox.selection_set(self.listbox.size()-1)
        self.render()

    def export_file(self):
        # Get the selected messages from the Listbox
        selected_indices = self.listbox.curselection()

        # Open a file dialog to get the save location from the user
        file_path = filedialog.asksaveasfilename(defaultextension=".json",filetypes=(("Json", '*.json'),))
        with open(file_path, "w",encoding="utf8") as f:
            f.write("[\n")
            f.write(self.listbox.get(selected_indices[0]))
            
            for i in selected_indices[1:]:
                f.write(",\n")
                f.write(self.listbox.get(i))
            f.write("\n]")
        self.render()

    def open_file(self):
        # Open a file dialog to select a JSON file
        try:
            filename = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
            self.listbox.delete(0, tk.END)
            # Read the JSON file as a list of dictionaries
            with open(filename,"r",encoding="utf8") as f:
                new_messages = json.load(f)
            # Append each dictionary to the Listbox
            for message in new_messages:
                self.listbox.insert("end", json.dumps(message))
                self.listbox.selection_set(self.listbox.size()-1)
        except:
            pass
        self.render()


    def save_file(self):
        # Create a list of dictionaries containing the selected messages
        file_path = filedialog.asksaveasfilename(defaultextension=".json",filetypes=(("Json", '*.json'),))
        with open(file_path, "w",encoding="utf8") as f:
            f.write("[")
            f.write(self.listbox.get(0))
            for message in self.listbox.get(1, tk.END):
                f.write(",\n")
                f.write(message)
            f.write("]")
        self.render()

    def clear_selected(self):
        # Iterate over the indices of the currently selected items and remove them from the Listbox
        for index in reversed(self.listbox.curselection()):
            self.listbox.delete(index)
        self.render()

    def reverse_selection(self):
        # Get the current selection in the Listbox widget
        current_selection = self.listbox.curselection()
        for i in range(self.listbox.size()):
            if i in current_selection:
                self.listbox.selection_clear(i)
            else:
                self.listbox.selection_set(i)
        self.render()
    
    def select_between(self):
        selected_indices = self.listbox.curselection()
        if len(selected_indices) >= 2:
            first_index = selected_indices[0]
            last_index = selected_indices[-1]
            self.listbox.selection_clear(0, tk.END)
            self.listbox.selection_set(first_index, last_index)
        self.render()

    def copy_json(self):
        # Get the selected text from the Listbox
        selected_indices = self.listbox.curselection()
 
        ans = self.listbox.get(selected_indices[0])
            
        for i in selected_indices[1:]:
            ans += ",\n"
            ans += self.listbox.get(i)

        # Copy the selected text to the clipboard
        self.master.clipboard_clear()
        self.master.clipboard_append(ans)
        self.render()
    
    def copy_text(self):

        self.master.clipboard_clear()
        self.master.clipboard_append(self.render())

    def move_up(self):
            # Get the selected indices in reverse order
            selected_indices = self.listbox.curselection()
            if selected_indices[0] == 0:
                return
            for index in selected_indices:
                    # Get the text and state of the current item and its previous item
                    current_text = self.listbox.get(index)
                    current_state = self.listbox.selection_includes(index)
                    previous_text = self.listbox.get(index-1)
                    previous_state = self.listbox.selection_includes(index-1)
                    # Delete the current item and insert it before its previous item
                    self.listbox.delete(index)
                    self.listbox.insert(index-1, current_text)
                    # Set the selection state of the current item to that of its previous item
                    if current_state:
                        self.listbox.selection_set(index-1)
                    else:
                        self.listbox.selection_clear(index-1)
                    # Set the selection state of the previous item to that of the current item
                    if previous_state:
                        self.listbox.selection_set(index)
                    else:
                        self.listbox.selection_clear(index)
            self.render()

    def move_down(self):
            # Get the selected indices in reverse order
            selected_indices = self.listbox.curselection()[::-1]
            if selected_indices[0] == self.listbox.size()-1:
                return
            for index in selected_indices:
                    # Get the text and state of the current item and its previous item
                    current_text = self.listbox.get(index)
                    current_state = self.listbox.selection_includes(index)
                    previous_text = self.listbox.get(index+1)
                    previous_state = self.listbox.selection_includes(index+1)
                    # Delete the current item and insert it before its previous item
                    self.listbox.delete(index)
                    self.listbox.insert(index+1, current_text)
                    # Set the selection state of the current item to that of its previous item
                    if current_state:
                        self.listbox.selection_set(index+1)
                    else:
                        self.listbox.selection_clear(index+1)
                    # Set the selection state of the previous item to that of the current item
                    if previous_state:
                        self.listbox.selection_set(index)
                    else:
                        self.listbox.selection_clear(index)
            self.render()
    
    def render(self):
        text = ""
        selected_indices = self.listbox.curselection()
        for i in selected_indices:
            message = json.loads(self.listbox.get(i))
            pronoun = {"user":"[USR]","assistant":"[GPT]","system":"[SYS]"}
            text += "{} {}".format(pronoun[message['role']],message['content'])
            text = re.sub(r'[ \n]+$','',text)
            text = re.sub(r'^[ \n]+','',text)
            text+="\n\n" 

        w = len(text.split())
        l = len(text) - text.count(" ")
        t = int((w*1.33+l*0.25)/2)
        para = {"model":"gpt-3.5-turbo","max_tokens":1000,"stop":None,"temperature":0.3}
        exec(self.config_input.get(),para)
        out = para['max_tokens']
        x = {True:"<",False:">"}[t+out<4097]
        y = {True:"",False:"!!!"}[t+out<4097]
        text = "(word = {} token ≈ {} + {} = {} {} 4097{})\n\n{}".format(w,t,out,t+out,x,y,text)
        
        self.render_text.delete('1.0', 'end')
        self.render_text.insert('1.0', text)
        return text

class ChatBox:
    def __init__(self, master):
        self.master = master
        self.chat_history_box = None
        self.create_widgets()
        self.create_menubar()

    def create_menubar(self):
        self.menubar = tk.Menu(self.master)
        self.master.config(menu=self.menubar)

        self.file_menu = tk.Menu(self.menubar)
        self.menubar.add_cascade(label="File", menu=self.file_menu)

        self.file_menu.add_command(label="Open", command=self.chat_history_box.open_file)
        self.file_menu.add_command(label="Save", command=self.chat_history_box.save_file)

        self.file_menu.add_separator()
        self.file_menu.add_command(label="Import", command=self.chat_history_box.import_file)
        self.file_menu.add_command(label="Export", command=self.chat_history_box.export_file)
        
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.master.quit)

    def create_widgets(self):
        # Create a PanedWindow with two panes, oriented horizontally
        self.chat_history_pane = tk.PanedWindow(self.master, orient="vertical", sashwidth=10, sashrelief="ridge")
        self.chat_history_pane.pack(fill="both", expand=True)

        self.chat_history_pane2 = tk.PanedWindow(self.chat_history_pane, orient="horizontal", sashwidth=10, sashrelief="ridge")
        self.chat_history_pane.add(self.chat_history_pane2)

        # Create a ChatHistoryBox widget and add it to the left pane of the PanedWindow
        input_box_frame = tk.Frame(self.chat_history_pane)
        app_config_frame = tk.Frame(input_box_frame,height = "50",borderwidth=2)
        config_frame = tk.Frame(input_box_frame,height = "50",borderwidth=2)
        self.app_config_input = tk.Entry(app_config_frame)
        self.config_input = tk.Entry(config_frame)
        self.render_text = tk.Text(self.chat_history_pane2,borderwidth=2)
        self.chat_history_box = ChatHistoryBox(self.master,self.render_text, self.app_config_input,self.config_input , [])
        self.chat_history_pane2.add(self.chat_history_box)
        self.chat_history_pane2.add(self.render_text)

        # Create a frame to hold the message input textbox and send button, and add it to the right pane of the PanedWindow
        #input_box_frame = tk.Frame(self.chat_history_pane)
        self.chat_history_pane.add(input_box_frame)
        
        token_frame = tk.Frame(input_box_frame,height = "50",borderwidth=2)
        label = tk.Label(token_frame,width = "10", text="API Key",borderwidth=2)
        label.pack(side="left")
        self.token_input = tk.Entry(token_frame,show='*')
        self.token_input.pack(side="left", fill="x", expand=True)
        token_frame.pack(side="top", fill="x")

        #app_config_frame = tk.Frame(input_box_frame,height = "50",borderwidth=2)
        label = tk.Label(app_config_frame,width = "10", text="APP Config",borderwidth=2)
        label.pack(side="left")
        #self.app_config_input = tk.Entry(app_config_frame)
        self.app_config_input.pack(side="left", fill="x", expand=True)
        app_config_frame.pack(side="top",fill="x")
        default = "SelectNewLines=True"
        self.app_config_input.delete('0', 'end')
        self.app_config_input.insert('0', default)

        #config_frame = tk.Frame(input_box_frame,height = "50",borderwidth=2)
        label = tk.Label(config_frame,width = "10", text="GPT Config",borderwidth=2)
        label.pack(side="left")
        #self.config_input = tk.Entry(config_frame)
        self.config_input.pack(side="left", fill="x", expand=True)
        config_frame.pack(side="top",fill="x")

        default = "model=\"gpt-3.5-turbo\"; max_tokens=1000; stop=None; temperature=0.3"

        self.config_input.delete('0', 'end')
        self.config_input.insert('0', default)


        search_frame = tk.Frame(input_box_frame,height = "50",borderwidth=2)
        self.search_button = tk.Button(search_frame,width = "10", text="RE Search",borderwidth=2,command=self.search)
        self.search_button.pack(side="left")
        self.search_input = tk.Entry(search_frame)
        self.search_input.pack(side="left", fill="x", expand=True)
        search_frame.pack(side="top",fill="x")
        default = "\\\"role\\\"\s*:\s*\\\"user\\\""
        self.search_input.delete('0', 'end')
        self.search_input.insert('0', default)

        
        # Create a Text widget for the message input, and pack it to the left side of the frame, filling and expanding to take up all available space
        self.message_input = tk.Text(input_box_frame,width=50, height=10)
        self.message_input.pack(side="left", fill="both", expand=True)

        # Create a Send button and pack it to the right side of the frame

        self.send_button = tk.Button(input_box_frame, text="Send", command=self.send_message)
        self.send_button.pack(fill="both", expand=True)
    
    def search(self):
        self.chat_history_box.listbox.selection_clear(0, tk.END)
        pattern = r'' + self.search_input.get()
        for index, item in enumerate(self.chat_history_box.listbox.get(0, tk.END)):
            match = re.search(pattern, item)
            if match:
                self.chat_history_box.listbox.selection_set(index)

    def send_message(self):
        model_input = []
        
        selected_indices = self.chat_history_box.listbox.curselection()
        for i in selected_indices:
            model_input.append(json.loads(self.chat_history_box.listbox.get(i)))
        text = self.message_input.get('1.0', 'end')
        text = re.sub(r'[ \n]+$','',text)
        text = re.sub(r'^[ \n]+','',text)
        message = {"role":"user","content":format(text)}
        model_input.append(message)

        openai.api_key = self.token_input.get()
        # Use OpenAI's ChatCompletion API to get the chatbot's response

        para = {"model":"gpt-3.5-turbo","max_tokens":1000,"stop":None,"temperature":0.3}
        exec(self.config_input.get(),para)
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
        
        para = {"SelectNewLines":True}
        exec(self.app_config_input.get(),para)
        

        self.chat_history_box.listbox.insert("end", json.dumps(message))
        if para["SelectNewLines"]:
            self.chat_history_box.listbox.selection_set(self.chat_history_box.listbox.size()-1)
        self.chat_history_box.listbox.insert("end", json.dumps(reply))
        if para["SelectNewLines"]:
            self.chat_history_box.listbox.selection_set(self.chat_history_box.listbox.size()-1)
        self.message_input.delete('1.0', 'end')
        self.chat_history_box.render()


if __name__ == "__main__":
    root = tk.Tk()
    root.title('GPT3.5')
    root.geometry("1366x768")
    chat_box = ChatBox(root)
    def set_sashes():
        chat_box.chat_history_pane.sash_place(0, 0, 500)
        chat_box.chat_history_pane2.sash_place(0, 500, 0)
    root.after(100,set_sashes)

    def send_callback(event):
        if event.keysym == 'Return' and event.state == 0x1:
            chat_box.send_button.invoke()
    root.bind('<Shift-Return>', send_callback)

    
    def on_select(event):
        chat_box.chat_history_box.render()
    def on_deselect(event):
        chat_box.chat_history_box.render()
    # Bind the on_select function to the Listbox widget's selection event
    chat_box.chat_history_box.listbox.bind('<<ListboxSelect>>', on_select)
    # Bind the on_deselect function to the Listbox widget's deselection event
    chat_box.chat_history_box.listbox.bind('<<ListboxUnselect>>', on_deselect)

    key = os.getenv("OPENAI_API_KEY")
    chat_box.token_input.delete('0', 'end')
    chat_box.token_input.insert('0', key)
    
    root.mainloop()

