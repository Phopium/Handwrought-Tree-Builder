import customtkinter as ctk
import logic.supa_tables as supa
from tkinter import messagebox

import ui.config as uicfg

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
                b.configure(fg_color=uicfg.tile_hlight_clr)
            else:
                b.configure(fg_color=uicfg.default_tile_clr)
        
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
        # Check if another concurrent user updated the database since last check.
        new_timestamp = supa.get_timestamp()
        if new_timestamp == self.timestamp:
            update_detected = False
            from_id = self.pos_edit_buffer
            to_id = talent_id
            self.modify_position(from_id, to_id)
        else:
            update_detected = True
            messagebox.showerror("Warning", f"Another concurrent user has updated the database. Refreshing...")

        self.pos_edit_buffer = None

        # Reset all button colors
        for tid, (b, _) in self.talent_buttons[tree_name].items():
            key = (tree_name, tid)
            if key in self.selected_talents:
                b.configure(fg_color=uicfg.tile_hlight_clr)
            else:
                b.configure(fg_color=uicfg.default_tile_clr)
        
        self.reset_tab(update_detected)
        self.timestamp = supa.get_timestamp()

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
    body_tb = ctk.CTkTextbox(top, width=400, height=200, wrap="word")
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