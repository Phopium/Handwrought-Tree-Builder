import customtkinter as ctk

import ui.config as uicfg

class TalentTile(ctk.CTkFrame):
    def __init__(self, master, text="", textbox_text="", xp_text="", command=None, width=uicfg.btn_width, height=uicfg.btn_height, fg_color=uicfg.default_tile_clr, **kwargs):
        super().__init__(master, width=width, height=height, fg_color=uicfg.default_tile_clr, corner_radius=8, **kwargs)
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
            btn.configure(fg_color=uicfg.default_tile_clr)
            self.xp_spent -= btn_xp + tree_xp_total
            self.xp_remaining_val.configure(text=(self.xp_total - self.xp_spent))
        else:
            # Select talent
            self.selected_talents.add(key)
            btn.configure(fg_color=uicfg.tile_hlight_clr)
            tree_xp_total = get_tree_xp()
            self.xp_spent += btn_xp + tree_xp_total
            self.xp_remaining_val.configure(text=(self.xp_total - self.xp_spent))