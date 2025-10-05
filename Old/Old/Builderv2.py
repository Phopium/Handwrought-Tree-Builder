from pathlib import Path
import customtkinter as ctk
import json
import tkinter.filedialog as fd
import os

ctk.set_appearance_mode("dark")



def loadData(filename: str | None = None):
    here = Path(__file__).resolve().parent
    path = here / (filename or "data.json")   # default: data.json next to Builder.py
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)
    
# Define talent tile GUI attributes
default_btn_clr = "#3790cc"
btn_width = 165
btn_height = 100

starting_xp = "10"


class TalentTile(ctk.CTkFrame):
    def __init__(self, master, text="", textbox_text="", xp_text="", command=None, width=btn_width, height=btn_height, fg_color=default_btn_clr, **kwargs):
        super().__init__(master, width=width, height=height, fg_color=fg_color, corner_radius=8, **kwargs)
        self.command = command

        # Main label
        self.label = ctk.CTkLabel(self, text=text, anchor="center")
        self.label.pack(side="top")

        self.textbox = ctk.CTkTextbox(self, height=height, width=width, font=("TkDefaultFont", 11))
        self.textbox.insert("1.0", textbox_text)
        self.textbox.configure(wrap="word", state="disabled")
        self.textbox.pack(side="bottom", padx=3, pady=3)
        self.talent_xp_lbl = ctk.CTkLabel(self, fg_color="#222222", text=xp_text, font=("TkDefaultFont", 11, "bold"))
        self.talent_xp_lbl.place(relx=0.96, rely=0.96, anchor="se")

        # Click binding
        self.bind("<Button-1>", self._on_click)
        self.label.bind("<Button-1>", self._on_click)
        self.textbox.bind("<Button-1>", self._on_click)

    def _on_click(self, event):
        if self.command:
            self.command()

    def configure(self, **kwargs):
        if "command" in kwargs:
            self.command = kwargs.pop("command")
        if "text" in kwargs:
            self.label.configure(text=kwargs.pop("text"))
        if "textbox_text" in kwargs:
            self.textbox.configure(state="normal")
            self.textbox.delete("1.0", "end")
            self.textbox.insert("1.0", kwargs.pop("textbox_text"))
            self.textbox.configure(state="disabled")
        if "fg_color" in kwargs:
            super().configure(fg_color=kwargs.pop("fg_color"))
        super().configure(**kwargs)



class TalentTreeApp(ctk.CTk):
    def __init__(self, data):
        super().__init__()
        self.title("Talent Tree Builder")
        self.geometry("1520x900")
        self.data = data

        self.selected_talents = set()
        self.edit_connection_mode = False
        self.edit_position_mode = False
        self.edit_text_mode = False
        self.connection_edit_buffer = None
        self.pos_edit_buffer = None
        self.text_edit_buffer = None
        self.talent_buttons = {}  # {tree_name: {id: (button, position)}}
        self.tier_xp_values = [4, 6, 8, 10, 12, 14]
        self.tree_xp_cost = 8
        self.xp_spent = 0
        self.xp_total = int(starting_xp)

        #== UI Elements ==
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Info frame
        self.info_frame = ctk.CTkFrame(self, height=120)
        self.info_frame.grid(row=0, column=0, padx=5, pady=5, sticky="new")

        self.xp_frame = ctk.CTkFrame(self.info_frame, height=70)
        self.xp_frame.place(relx=.05)
        self.set_xp_btn = ctk.CTkButton(self.xp_frame, width=50, text="Set XP", command=self.set_xp_total)
        self.set_xp_btn.grid(row=1, column=0, padx=5)

        self.xp_entry = ctk.CTkEntry(self.xp_frame, placeholder_text=starting_xp, width=70, height=65, font=("TkDefaultFont", 24))
        self.xp_entry.grid(row=1, column=1, padx=5, pady=5)
        self.xp_entry_lbl = ctk.CTkLabel(self.xp_frame, text="Total XP")
        self.xp_entry_lbl.grid(row=0, column=1, padx=5, pady=5)
        self.xp_remaining_val = ctk.CTkLabel(self.xp_frame, width=70, height=65, font=("TkDefaultFont", 24), text=starting_xp)
        self.xp_remaining_val.grid(row=1, column=2, padx=5)
        self.xp_remaining_lbl = ctk.CTkLabel(self.xp_frame, text="Remaining XP")
        self.xp_remaining_lbl.grid(row=0, column=2, padx=5)

        # Info buttons
        self.info_btn_frame = ctk.CTkFrame(self.info_frame)
        self.info_btn_frame.place(relx=.3, rely=.2)

        self.load_char_btn = ctk.CTkButton(self.info_btn_frame, text="Load Character", command=self.load_character)
        self.load_char_btn.grid(row=0, column=2, padx=5, pady=5)
        self.save_char_btn = ctk.CTkButton(self.info_btn_frame, text="Save Character", command=self.save_character)
        self.save_char_btn.grid(row=0, column=1, padx=5, pady=5)

        self.edit_text_btn = ctk.CTkButton(self.info_btn_frame, text="Edit: Text", command=self.toggle_edit_text_mode)
        self.edit_text_btn.grid(row=1, column=0, padx=5, pady=5)
        self.edit_pos_btn = ctk.CTkButton(self.info_btn_frame, text="Edit: Positions", command=self.toggle_edit_position_mode)
        self.edit_pos_btn.grid(row=1, column=1, padx=5, pady=5)
        self.edit_conn_btn = ctk.CTkButton(self.info_btn_frame, text="Edit: Connections", command=self.toggle_edit_connection_mode)
        self.edit_conn_btn.grid(row=1, column=2, padx=5, pady=5)
        self.save_json_btn = ctk.CTkButton(self.info_btn_frame, text="Save Changes", command=self.save_data)
        self.save_json_btn.grid(row=1, column=3, padx=5, pady=5)

        # Tree frame
        self.tree_frame = ctk.CTkFrame(self)
        self.tree_frame.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

        self.tabs = ctk.CTkTabview(self.tree_frame)
        self.tabs.pack(fill="both", expand=True)
        self.tab_frames = {}

        self.build_tabs()



    #==== Button logic ====
    def on_talent_click(self, tree_name, talent_id, column, row):
        if self.edit_connection_mode:
            self.handle_connection_edit(tree_name, talent_id)
        elif self.edit_position_mode:
            self.handle_pos_edit(tree_name, talent_id)
        elif self.edit_text_mode:
            self.open_text_editor(tree_name, talent_id)
        # Normal tile select
        else:
            # Exception for initial tree talent (negative position)
            if column < 0:
                btn_xp = 0
            else:
                btn_xp = self.tier_xp_values[column]
            btn, _ = self.talent_buttons[tree_name][talent_id]
            key = (tree_name, talent_id)
            
            def get_tree_xp():
                distinct_trees = len({tree for tree, _ in self.selected_talents})
                if distinct_trees > 2:
                    tree_sum = distinct_trees - 2
                    return tree_sum * self.tree_xp_cost
                else:
                    return 0
                
            # add/subtract xp and set tile color
            if key in self.selected_talents:
                # Unselect talent
                tree_xp_total = get_tree_xp()
                self.selected_talents.remove(key)
                btn.configure(fg_color=default_btn_clr)
                self.xp_spent -= btn_xp + tree_xp_total
                self.xp_remaining_val.configure(text=(self.xp_total - self.xp_spent))
            else:
                # Select talent
                self.selected_talents.add(key)
                btn.configure(fg_color="green")
                tree_xp_total = get_tree_xp()
                self.xp_spent += btn_xp + tree_xp_total
                self.xp_remaining_val.configure(text=(self.xp_total - self.xp_spent))


    #= Toggle button modes =
    def toggle_edit_connection_mode(self):
        self.edit_connection_mode = not self.edit_connection_mode
        if self.edit_connection_mode:
            self.edit_conn_btn.configure(fg_color="orange")
            self.connection_edit_buffer = None
        else:
            self.edit_conn_btn.configure(fg_color=default_btn_clr)
            self.connection_edit_buffer = None

    def toggle_edit_position_mode(self):
        self.edit_position_mode = not self.edit_position_mode
        if self.edit_position_mode:
            self.edit_pos_btn.configure(fg_color="orange")
            self.pos_edit_buffer = None
        else:
            self.edit_pos_btn.configure(fg_color=default_btn_clr)
            self.pos_edit_buffer = None
    
    def toggle_edit_text_mode(self):
        self.edit_text_mode = not self.edit_text_mode
        if self.edit_text_mode:
            self.edit_text_btn.configure(fg_color="orange")
            self.text_edit_buffer = None
        else:
            self.edit_text_btn.configure(fg_color=default_btn_clr)
            self.text_edit_buffer = None


    #= Button functions =
    def handle_connection_edit(self, tree_name, talent_id):
        btn, _ = self.talent_buttons[tree_name][talent_id]
        if self.connection_edit_buffer is None:
            self.connection_edit_buffer = talent_id
            btn.configure(fg_color="yellow")
        else:
            from_id = self.connection_edit_buffer
            to_id = talent_id
            self.modify_connection(tree_name, from_id, to_id)
            self.connection_edit_buffer = None

            # Reset all button colors
            for tid, (b, _) in self.talent_buttons[tree_name].items():
                key = (tree_name, tid)
                if key in self.selected_talents:
                    b.configure(fg_color="green")
                else:
                    b.configure(fg_color=default_btn_clr)
            
            # Get tab info
            this_tab_name = self.tabs.get()
            this_tab = self.tabs.tab(this_tab_name)
            frame = self.tab_frames[tree_name]
            canvas = frame.canvas
            
            # Clear lines then draw new ones
            for line in canvas.lines:
                canvas.delete(line)
            canvas.lines.clear()
            
            tree_data = self.data["trees"][this_tab.tree_index]
            self.draw_connections(tree_data, canvas)
    
    def handle_pos_edit(self, tree_name, talent_id):
        btn, _ = self.talent_buttons[tree_name][talent_id]
        if self.pos_edit_buffer is None:
            self.pos_edit_buffer = talent_id
            btn.configure(fg_color="yellow")
        else:
            from_id = self.pos_edit_buffer
            to_id = talent_id
            self.modify_position(tree_name, from_id, to_id)
            self.pos_edit_buffer = None

            # Reset all button colors
            for tid, (b, _) in self.talent_buttons[tree_name].items():
                key = (tree_name, tid)
                if key in self.selected_talents:
                    b.configure(fg_color="green")
                else:
                    b.configure(fg_color=default_btn_clr)
            
            self.reset_tab()    
    
    def open_text_editor(self, tree_name, talent_id):
        # get talent data
        tree = next(t for t in self.data["trees"] if t["name"] == tree_name)
        talent = next(t for t in tree["talents"] if t["id"] == talent_id)

        # create modal window
        top = ctk.CTkToplevel(self)
        top.title(f"Edit Talent — {talent.get('name','')}")
        top.transient(self)
        top.grab_set()

        # Title
        ctk.CTkLabel(top, text="Title:").grid(row=0, column=0, padx=8, pady=(8,4), sticky="w")
        title_entry = ctk.CTkEntry(top, width=400)
        title_entry.grid(row=1, column=0, padx=8, pady=(0,8), sticky="we")
        title_entry.insert(0, talent.get("name", ""))

        # Body (description)
        ctk.CTkLabel(top, text="Description:").grid(row=2, column=0, padx=8, pady=(4,4), sticky="w")
        body_tb = ctk.CTkTextbox(top, width=400, height=200)
        body_tb.grid(row=3, column=0, padx=8, pady=(0,8), sticky="nsew")
        body_text = talent.get("description", talent.get("text", ""))
        if body_text:
            body_tb.insert("1.0", body_text)

        # Buttons
        btn_frame = ctk.CTkFrame(top)
        btn_frame.grid(row=4, column=0, padx=8, pady=8, sticky="e")
        def on_save():
            new_title = title_entry.get().strip()
            new_body = body_tb.get("1.0", "end").rstrip("\n")
            # persist to data
            talent["name"] = new_title
            # store under "description"
            talent["description"] = new_body

            # update UI button/label
            btn, _ = self.talent_buttons[tree_name][talent_id]
            btn.configure(text=new_title, textbox_text=new_body)

            top.grab_release()
            top.destroy()

        def on_cancel():
            top.grab_release()
            top.destroy()

        save_btn = ctk.CTkButton(btn_frame, text="Save", command=on_save)
        save_btn.grid(row=0, column=0, padx=(0,8))
        cancel_btn = ctk.CTkButton(btn_frame, text="Cancel", command=on_cancel)
        cancel_btn.grid(row=0, column=1)

        # ensure closing via window manager is handled
        top.protocol("WM_DELETE_WINDOW", on_cancel)

        # allow the textbox to expand vertically
        top.grid_rowconfigure(3, weight=1)
        top.grid_columnconfigure(0, weight=1)

    def load_character(self):
        path = fd.askopenfilename(title="Open character JSON", filetypes=[("JSON Files","*.json"),("All files","*.*")])
        if not path:
            return
        try:
            #new_data = loadData(path)
            with open(path, "r", encoding="utf-8") as f:
                char_save = json.load(f)
        except Exception as e:
            print("Failed to load file:", e)
            return
        
        # restore selected talents (stored as list of [tree_name, talent_id])
        sel = char_save.get("selected_talents", [])
        try:
            self.selected_talents = set((t[0], t[1]) for t in sel)
        except Exception:
            self.selected_talents = set()
        # Restore xp
        try:
            self.xp_total = int(char_save.get("xp_total", self.xp_total))
        except Exception:
            pass
        try:
            self.xp_spent = int(char_save.get("xp_spent", self.xp_spent))
        except Exception:
            pass
        try:
            self.xp_entry.delete(0, "end")
            self.xp_entry.insert(0, str(self.xp_total))
        except Exception:
            pass
        self.xp_remaining_val.configure(text=(self.xp_total - self.xp_spent))

        # update tile colors to reflect selection
        for tree_name, talents in self.talent_buttons.items():
            for tid, (btn, _) in talents.items():
                key = (tree_name, tid)
                if key in self.selected_talents:
                    btn.configure(fg_color="green")
                else:
                    btn.configure(fg_color=default_btn_clr)
        
    def save_character(self):
        # Build character file
        char_save = {
            "selected_talents": [[tree, tid] for (tree, tid) in self.selected_talents],
            "xp_total": self.xp_total,
            "xp_spent": self.xp_spent
        }
        # Ask for a filename to save to (asksaveas gives file selection)
        path = fd.asksaveasfilename(title="Export character as...", defaultextension=".json",
                                    filetypes=[("JSON Files","*.json"),("All files","*.*")])
        if not path:
            return
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(char_save, f, indent=4)
        except Exception as e:
            print("Failed to save file:", e)
        


    #==== GUI functions ====
    def set_xp_total(self):
        self.xp_total = int(self.xp_entry.get())
        self.xp_remaining_val.configure(text=(self.xp_total - self.xp_spent))

    
    def populate_tab(self, tab, tree):
        frame = ctk.CTkScrollableFrame(tab, width=850, height=650)
        frame.pack(fill="both", expand=True)
        frame.canvas = ctk.CTkCanvas(frame, width=850, height=870, bg="#252525")
        frame.canvas.pack(fill="both", expand=True)
        frame.canvas.lines = []
        self.tab_frames[tree["name"]] = frame
        tab_lbl = ctk.CTkLabel(frame.canvas, text=tree["name"], font=("TkDefaultFont", 24))
        tab_lbl.place(relx=.05, rely=.1)

        self.talent_buttons[tree["name"]] = {}

        # Place buttons
        for talent in tree["talents"]:
            x, y = talent["position"]
            x_offset = 275
            y_offset = 30
            x_spacing = 200
            y_spacing =  170
            btn_xp = f"{self.tier_xp_values[x]} XP"

            # Exception for the main tree talent (denoted by negative position)
            if x < 0 and y < 0:
                btn_xp = ""
                px, py = 30, 300
                btn = TalentTile(frame.canvas, text=talent["name"], textbox_text=talent["description"], xp_text=btn_xp, width=(btn_width * 1.2), height=(btn_height * 2.5), fg_color=default_btn_clr)
            # Normal talent tiles
            else:
                btn_xp = f"{self.tier_xp_values[x]} XP"
                px, py = x_offset + x * x_spacing, y_offset + y * y_spacing
                btn = TalentTile(frame.canvas, text=talent["name"], textbox_text=talent["description"], xp_text=btn_xp, width=btn_width, height=btn_height, fg_color=default_btn_clr)
            btn.place(x=px, y=py)
            btn.configure(command=lambda t_id=talent["id"], t_name=tree["name"], column=x, row=y: self.on_talent_click(t_name, t_id, column, row))
            self.talent_buttons[tree["name"]][talent["id"]] = (btn, (px, py))
            key = (tree["name"], talent["id"])
            if key in self.selected_talents:
                btn.configure(fg_color="green")

        # Draw connection lines
        self.draw_connections(tree, frame.canvas)


    def build_tabs(self):
        for i, tree in enumerate(self.data["trees"]):
            tab = self.tabs.add(tree["name"])
            print(f"Building tab: {tree["name"]}")
            tab.tree_index = i # For getting the tree data later
            tab.canvas_lines = []
            self.populate_tab(tab, tree)


    def draw_connections(self, tree, canvas):
        for talent in tree["talents"]:
                sx, sy = self.talent_buttons[tree["name"]][talent["id"]][1]
                for conn_id in talent["connections"]:
                    ex, ey = self.talent_buttons[tree["name"]][conn_id][1]
                    line_id = canvas.create_line(sx + (btn_width/2), sy + (btn_height/1.5), ex + (btn_width/2), ey + (btn_height/1.5), fill="light gray", width=2)
                    canvas.lines.append(line_id)


    def modify_connection(self, tree_name, from_id, to_id):
        tree = next(t for t in self.data["trees"] if t["name"] == tree_name)
        from_talent = next(t for t in tree["talents"] if t["id"] == from_id)
        to_talent = next(t for t in tree["talents"] if t["id"] == to_id)
        if to_id in from_talent["connections"]:
            from_talent["connections"].remove(to_id)
        elif from_id in to_talent["connections"]:
            to_talent["connections"].remove(from_id)
        else:
            from_talent["connections"].append(to_id)

    def modify_position(self, tree_name, from_id, to_id):
        tree = next(t for t in self.data["trees"] if t["name"] == tree_name)
        from_talent = next(t for t in tree["talents"] if t["id"] == from_id)
        to_talent = next(t for t in tree["talents"] if t["id"] == to_id)

        # copy and swap the position values
        from_pos = list(from_talent["position"])
        to_pos = list(to_talent["position"])
        from_talent["position"], to_talent["position"] = to_pos, from_pos


    def save_data(self, filename="Current/data.json"):
        with open(filename, "w") as f:
            json.dump(self.data, f, indent=4)
            
    
    # Clear the tab, then repopulate it with updated buttons (unused)
    def reset_tab(self):
            this_tab_name = self.tabs.get()
            this_tab = self.tabs.tab(this_tab_name)
            child_frame = this_tab.winfo_children()[0] # Assumes frame is the first child
            child_frame.destroy()
            
            tree_data = self.data["trees"][this_tab.tree_index]
            self.populate_tab(this_tab, tree_data)


if __name__ == "__main__":
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")
    app = TalentTreeApp(loadData())
    app.mainloop()
