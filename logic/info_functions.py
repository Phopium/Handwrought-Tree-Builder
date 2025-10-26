from pathlib import Path
import json

import tkinter as tk

import ui.config as uicfg


#==== GUI functions ====
def set_xp_total(self):
    self.xp_total = int(self.xp_entry.get())
    self.xp_remaining_val.configure(text=(self.xp_total - self.xp_spent))

def load_character(self):
    path = tk.filedialog.askopenfilename(title="Open character JSON", filetypes=[("JSON Files","*.json"),("All files","*.*")])
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
                btn.configure(fg_color=uicfg.tile_hlight_clr)
            else:
                btn.configure(fg_color=uicfg.default_tile_clr)
    
def save_character(self):
    # Build character file
    char_save = {
        "selected_talents": [[tree, tid] for (tree, tid) in self.selected_talents],
        "xp_total": self.xp_total,
        "xp_spent": self.xp_spent
    }
    # Ask for a filename to save to (asksaveas gives file selection)
    path = tk.filedialog.asksaveasfilename(title="Export character as...", defaultextension=".json",
                                filetypes=[("JSON Files","*.json"),("All files","*.*")])
    if not path:
        return
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(char_save, f, indent=4)
    except Exception as e:
        print("Failed to save file:", e)