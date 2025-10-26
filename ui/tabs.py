import customtkinter as ctk

from logic.supa_tables import getTrees
import ui.config as uicfg
from ui.talent_tiles import TalentTile

def build_tabs(self):
    trees = getTrees()
    for tree in (trees):
        tab = self.tabs.add(tree["name"])
        print(f"Building tab: {tree["name"]}")
        tab.tree_index = tree["id"] # For getting the tree data later
        tab.canvas_lines = []
        self.populate_tab(tab, tree)


def populate_tab(self, tab, tree):
    frame = ctk.CTkScrollableFrame(tab, width=850, height=650)
    frame.pack(fill="both", expand=True)
    frame.canvas = ctk.CTkCanvas(frame, width=850, height=870, bg="#252525")
    frame.canvas.pack(fill="both", expand=True)
    frame.canvas.lines = []
    self.tab_frames[tree["name"]] = frame
    tab_lbl = ctk.CTkLabel(frame.canvas, text=tree["name"], font=("TkDefaultFont", 30))
    tab_lbl.place(relx=.03, rely=.05)

    self.talent_buttons[tree["name"]] = {}

    # Place buttons
    for talent in self.data:
        if talent["tree_id"] == tree["id"]:
            x_pos = talent["x_pos"]
            y_pos = talent["y_pos"]
            x_offset = 275
            y_offset = 30
            x_spacing = 200
            y_spacing =  170
            btn_xp = f"{self.tier_xp_values[x]} XP"

            # Exception for the main tree talent (denoted by negative position)
            if x_pos < 0 and y_pos < 0:
                btn_xp = ""
                px, py = uicfg.initial_tile_posx, uicfg.initial_tile_posy
                btn = TalentTile(frame.canvas, text=talent["name"], textbox_text=talent["description"], xp_text=btn_xp, width=(uicfg.btn_width * 1.2), height=(uicfg.btn_height * 2.5), fg_color=uicfg.default_tile_clr)
            # Normal talent tiles
            else:
                btn_xp = f"{self.tier_xp_values[x_pos]} XP"
                px, py = x_offset + x_pos * x_spacing, y_offset + y_pos * y_spacing
                btn = TalentTile(frame.canvas, text=talent["name"], textbox_text=talent["description"], xp_text=btn_xp, width=uicfg.btn_width, height=uicfg.btn_height, fg_color=uicfg.tile_hlight_clr)
            btn.place(x=px, y=py)
            btn.configure(command=lambda t_id=talent["id"], t_name=tree["name"], x_pos=x_pos, y_pos=y_pos: self.on_talent_click(t_name, t_id, x_pos, y_pos))
            self.talent_buttons[tree["name"]][talent["id"]] = (btn, (px, py))
            key = (tree["name"], talent["id"])
            if key in self.selected_talents:
                btn.configure(fg_color=uicfg.tile_hlight_clr)

    # Draw connection lines
    self.draw_connections(tree, frame.canvas)

# Clear the tab, then repopulate it with updated buttons (unused)
def reset_tab(self):
    this_tab_name = self.tabs.get()
    this_tab = self.tabs.tab(this_tab_name)
    child_frame = this_tab.winfo_children()[0] # Assumes frame is the first child
    child_frame.destroy()
    
    tree_data = self.data["trees"][this_tab.tree_index]
    self.populate_tab(this_tab, tree_data)