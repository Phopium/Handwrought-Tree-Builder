from pathlib import Path
import json

import customtkinter as ctk
import tkinter as tk

import ui.config as uicfg
from ui.tabs import build_tabs, populate_tab, reset_tab
from ui.talent_tiles import TalentTile, on_talent_click
from edit_helpers import draw_connections, modify_connection, modify_position
from edit_modes import handle_connection_edit, handle_pos_edit, open_text_editor
from info_functions import set_xp_total, load_character, save_character
import supa_tables as supa


ctk.set_appearance_mode("dark")

    
def get_screen_res():
    root_window = tk.Tk()
    root_window.withdraw()
    screen_width = root_window.winfo_screenwidth()
    screen_height = root_window.winfo_screenheight()
    root_window.destroy()
    return screen_height



class TalentTreeApp(ctk.CTk):
    def __init__(self, data):
        super().__init__()
        self.title("Talent Tree Builder")
        if get_screen_res() > 1200:
            self.geometry("1520x1100")
        else:
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
        self.tier_xp_values = [4, 6, 8, 8, 10, 10]
        self.tree_xp_cost = 8
        self.xp_spent = 0
        self.xp_total = int(uicfg.starting_xp)

        #== UI Elements ==
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        #= Info frame =
        self.info_frame = ctk.CTkFrame(self, height=120)
        self.info_frame.grid(row=0, column=0, padx=5, pady=5, sticky="new")

        self.xp_frame = ctk.CTkFrame(self.info_frame, height=70)
        self.xp_frame.place(relx=.05)
        self.set_xp_btn = ctk.CTkButton(self.xp_frame, width=50, text="Set XP", command=self.set_xp_total)
        self.set_xp_btn.grid(row=1, column=0, padx=5)

        self.xp_entry = ctk.CTkEntry(self.xp_frame, placeholder_text=uicfg.starting_xp, width=70, height=65, font=("TkDefaultFont", 24))
        self.xp_entry.grid(row=1, column=1, padx=5, pady=5)
        self.xp_entry_lbl = ctk.CTkLabel(self.xp_frame, text="Total XP")
        self.xp_entry_lbl.grid(row=0, column=1, padx=5, pady=5)
        self.xp_remaining_val = ctk.CTkLabel(self.xp_frame, width=70, height=65, font=("TkDefaultFont", 24), text=uicfg.starting_xp)
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

        #= Tree frame =
        self.tree_frame = ctk.CTkFrame(self)
        self.tree_frame.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

        self.tabs = ctk.CTkTabview(self.tree_frame)
        self.tabs.pack(fill="both", expand=True)
        self.tab_frames = {}

        self.build_tabs()

    # Attach external methods to class
    build_tabs = build_tabs
    populate_tab = populate_tab
    reset_tab = reset_tab

    # ui.talent_tiles
    TalentTile = TalentTile
    on_talent_click = on_talent_click
    
    # edit_helpers
    draw_connections = draw_connections
    modify_connection = modify_connection
    modify_position = modify_position
    
    # edit_modes
    handle_connection_edit = handle_connection_edit
    handle_pos_edit = handle_pos_edit
    open_text_editor = open_text_editor

    # info_functions
    set_xp_total = set_xp_total
    load_character = load_character
    save_character = save_character

    #= Toggle button modes =
    def toggle_edit_connection_mode(self):
        self.edit_connection_mode = not self.edit_connection_mode
        if self.edit_connection_mode:
            self.edit_conn_btn.configure(fg_color="orange")
            self.connection_edit_buffer = None
        else:
            self.edit_conn_btn.configure(fg_color=uicfg.default_btn_clr)
            self.connection_edit_buffer = None

    def toggle_edit_position_mode(self):
        self.edit_position_mode = not self.edit_position_mode
        if self.edit_position_mode:
            self.edit_pos_btn.configure(fg_color="orange")
            self.pos_edit_buffer = None
        else:
            self.edit_pos_btn.configure(fg_color=uicfg.default_btn_clr)
            self.pos_edit_buffer = None
    
    def toggle_edit_text_mode(self):
        self.edit_text_mode = not self.edit_text_mode
        if self.edit_text_mode:
            self.edit_text_btn.configure(fg_color="orange")
            self.text_edit_buffer = None
        else:
            self.edit_text_btn.configure(fg_color=uicfg.default_btn_clr)
            self.text_edit_buffer = None




if __name__ == "__main__":
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")
    app = TalentTreeApp(supa.loadData())
    app.mainloop()
