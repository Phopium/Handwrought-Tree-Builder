import customtkinter as ctk

import ui.config as uicfg

class InfoPanel(ctk.CTkFrame):
    def __init__(self, master, app, **kwargs):
        """
        master: parent widget (usually self in main app)
        app: reference to the main TalentTreeApp for callbacks
        """
        super().__init__(master, **kwargs)
        self.app = app

        # Buttons
        self.edit_conn_btn = ctk.CTkButton(self, text="Edit Connections", command=self.toggle_edit_connection_mode)
        self.edit_pos_btn = ctk.CTkButton(self, text="Edit Positions", command=self.toggle_edit_position_mode)
        self.edit_text_btn = ctk.CTkButton(self, text="Edit Text", command=self.toggle_edit_text_mode)

        # Layout
        self.edit_conn_btn.grid(row=0, column=0, padx=5, pady=5)
        self.edit_pos_btn.grid(row=0, column=1, padx=5, pady=5)
        self.edit_text_btn.grid(row=0, column=2, padx=5, pady=5)

        #= Toggle button modes =
    def toggle_edit_connection_mode(self):
        self.app.edit_connection_mode = not self.app.edit_connection_mode
        if self.app.edit_connection_mode:
            self.edit_conn_btn.configure(fg_color="orange")
            self.app.connection_edit_buffer = None
        else:
            self.edit_conn_btn.configure(fg_color=uicfg.default_btn_clr)
            self.app.connection_edit_buffer = None

    def toggle_edit_position_mode(self):
        self.app.edit_position_mode = not self.app.edit_position_mode
        if self.app.edit_position_mode:
            self.edit_pos_btn.configure(fg_color="orange")
            self.app.pos_edit_buffer = None
        else:
            self.edit_pos_btn.configure(fg_color=uicfg.default_btn_clr)
            self.app.pos_edit_buffer = None
    
    def toggle_edit_text_mode(self):
        self.edit_text_mode = not self.edit_text_mode
        if self.app.edit_text_mode:
            self.edit_text_btn.configure(fg_color="orange")
            self.app.text_edit_buffer = None
        else:
            self.edit_text_btn.configure(fg_color=uicfg.default_btn_clr)
            self.app.text_edit_buffer = None