import customtkinter as ctk
import json


def loadData(filename="data.json"):
    with open(filename, "r") as f:
        return json.load(f)
    
default_btn_clr = "#3790cc"
btn_width = 120
btn_height = 40


class TalentTile(ctk.CTkFrame):
    def __init__(self, master, text="", textbox_text="", command=None, width=120, height=60, fg_color=default_btn_clr, **kwargs):
        super().__init__(master, width=width, height=height, fg_color=fg_color, corner_radius=8, **kwargs)
        self.command = command

        # Main label
        self.label = ctk.CTkLabel(self, text=text, anchor="center")
        self.label.grid(row=0, column=0, padx=5, pady=0, sticky="n")

        # Optional textbox
        self.textbox = ctk.CTkTextbox(self, height=80, width=width)
        self.textbox.insert("1.0", textbox_text)
        self.textbox.configure(state="disabled")  # Make it read-only unless you want it editable
        self.textbox.grid(row=1, column=0, padx=3, pady=3, sticky="nsew")

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
        self.geometry("1400x900")
        self.data = data

        self.selected_talents = set()
        self.edit_connection_mode = False
        self.connection_edit_buffer = None
        self.talent_buttons = {}  # {tree_name: {id: (button, position)}}

        #== UI Elements ==
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.info_frame = ctk.CTkFrame(self)
        self.info_frame.grid(row=0, column=0, padx=5, pady=10, sticky="nsew")

        self.tree_frame = ctk.CTkFrame(self)
        self.tree_frame.grid(row=1, column=0, padx=5, pady=10, sticky="nsew")
        self.edit_conn_btn = ctk.CTkButton(self.tree_frame, text="Edit Connections", command=self.toggle_edit_connection_mode)
        self.edit_conn_btn.pack(pady=5)

        self.tabs = ctk.CTkTabview(self.tree_frame)
        self.tabs.pack(fill="both", expand=True)

        self.build_tabs()
    

    def build_tabs(self):
        for tree in self.data["trees"]:
            tab = self.tabs.add(tree["name"])
            #canvas_frame = ctk.CTkScrollableFrame(tab, width=700, height=600)
            #canvas_frame.pack(fill="both", expand=True)
            canvas = ctk.CTkCanvas(tab, width=700, height=800, bg="#252525")
            canvas.pack(fill="both", expand=True)
            btn_width = 120
            btn_height = 40

            self.talent_buttons[tree["name"]] = {}

            # Place buttons
            for talent in tree["talents"]:
                x, y = talent["position"]
                x_offset = 275
                y_offset = 30
                x_spacing = 180
                y_spacing =  150
                px, py = x_offset + x * x_spacing, y_offset + y * y_spacing
                btn = TalentTile(canvas, text=talent["name"], width=btn_width, height=btn_height, fg_color=default_btn_clr)
                btn.place(x=px, y=py)
                btn.configure(command=lambda t_id=talent["id"], t_name=tree["name"]: self.on_talent_click(t_name, t_id))
                self.talent_buttons[tree["name"]][talent["id"]] = (btn, (px, py))

            # Draw connection lines
            self.draw_connections(tree, canvas)

    def on_talent_click(self, tree_name, talent_id):
        if self.edit_connection_mode:
            self.handle_connection_edit(tree_name, talent_id)
        else:
            btn, _ = self.talent_buttons[tree_name][talent_id]
            key = (tree_name, talent_id)
            if key in self.selected_talents:
                self.selected_talents.remove(key)
                btn.configure(fg_color=default_btn_clr)
            else:
                self.selected_talents.add(key)
                btn.configure(fg_color="green")

    def toggle_edit_connection_mode(self):
        self.edit_connection_mode = not self.edit_connection_mode
        if self.edit_connection_mode:
            self.edit_conn_btn.configure(fg_color="orange")
            self.connection_edit_buffer = None
        else:
            self.edit_conn_btn.configure(fg_color=default_btn_clr)
            self.connection_edit_buffer = None

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
                b.configure(fg_color=default_btn_clr)
            self.redraw_canvas(tree_name)

    def draw_connections(self, tree, canvas):
        for talent in tree["talents"]:
                sx, sy = self.talent_buttons[tree["name"]][talent["id"]][1]
                for conn_id in talent["connections"]:
                    ex, ey = self.talent_buttons[tree["name"]][conn_id][1]
                    canvas.create_line(sx + (btn_width/2), sy + (btn_height/2), ex + (btn_width/2), ey + (btn_height/2), fill="light gray", width=2)

    def modify_connection(self, tree_name, from_id, to_id):
        tree = next(t for t in self.data["trees"] if t["name"] == tree_name)
        from_talent = next(t for t in tree["talents"] if t["id"] == from_id)
        if to_id in from_talent["connections"]:
            from_talent["connections"].remove(to_id)
        else:
            from_talent["connections"].append(to_id)

    def redraw_canvas(self, tree_name):
        tab = self.tabs.tab(tree_name)
        canvas = tab.winfo_children()[0]  # Assumes canvas is the first child
        canvas.delete("all")

        # Re-place buttons
        for tid, (btn, (x, y)) in self.talent_buttons[tree_name].items():
            btn.place(x=x, y=y)

        # Re-draw connections
        tree = next(t for t in self.data["trees"] if t["name"] == tree_name)
        self.draw_connections(tree, canvas)


if __name__ == "__main__":
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")
    app = TalentTreeApp(loadData())
    app.mainloop()
