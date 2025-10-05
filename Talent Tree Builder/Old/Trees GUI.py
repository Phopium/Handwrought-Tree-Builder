import customtkinter as ctk
import json

# == Load JSON Config ==
def load_config(path="testconfig.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

# == Tooltip Class ==
class Tooltip(ctk.CTkToplevel):
    def __init__(self, widget, text):
        super().__init__()
        self.withdraw()
        self.overrideredirect(True)
        self.attributes("-topmost", True)

        self.label = ctk.CTkLabel(self, text=text, fg_color="black", text_color="white", padx=5, pady=3)
        self.label.pack()

        self.widget = widget
        self.text = text

        widget.bind("<Enter>", self.show)
        widget.bind("<Leave>", self.hide)
        widget.bind("<Motion>", self.move)

    def show(self, event=None):
        self.deiconify()

    def hide(self, event=None):
        self.withdraw()

    def move(self, event):
        x = event.x_root + 15
        y = event.y_root + 15
        self.geometry(f"+{x}+{y}")

# == Talent Tree Frame ==
class TalentTreeFrame(ctk.CTkFrame):
    def __init__(self, master, button_grid):
        super().__init__(master)
        self.buttons = []

        for talent_button in button_grid:
            grid_col = talent_button["treeTier"] - 1   # adjust for 0-indexed grid
            grid_row = talent_button["position"] - 1
            label = talent_button["label"]
            desc = talent_button["description"]

            btn = ctk.CTkButton(
                self, text=label,
                command=lambda name=label: self.on_button_click(name)
            )
            btn.grid(row=grid_row, column=grid_col, padx=5, pady=5, sticky="nsew")

            # Store button state & widget
            talent_button["selected"] = False
            talent_button["widget"] = btn

            Tooltip(btn, desc)
            self.buttons.append(btn)

        # Make the grid expand nicely
        max_row = max(b["treeTier"] for b in button_grid)
        max_col = max(b["position"] for b in button_grid)
        for i in range(max_row):
            self.grid_rowconfigure(i, weight=1)
        for j in range(max_col):
            self.grid_columnconfigure(j, weight=1)

    def on_button_click(self, button_data):
        # Toggle selection state
        button_data["selected"] = not button_data["selected"]

        if button_data["selected"]:
            button_data["widget"].configure(fg_color="green")  # highlighted
        else:
            button_data["widget"].configure(fg_color="SystemButtonFace")  # reset

        print(f"{button_data['label']} selected: {button_data['selected']}")


# == Tab View ==
class TabView(ctk.CTkTabview):
    def __init__(self, master, tab_data, **kwargs):
        super().__init__(master, **kwargs)
        for tab in tab_data:
            tab_name = tab["name"]
            button_grid = tab["buttons"]

            self.add(tab_name)
            frame = TalentTreeFrame(master=self.tab(tab_name), button_grid=button_grid)
            frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

# ===== Main View ======
class MainView(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Talent Trees")
        self.geometry("1600x1000")
        self.config = load_config()
        self.create_widgets()

    def create_widgets(self):
        self.talent_tabs = TabView(self, self.config["tabs"])
        self.talent_tabs.pack(expand=True, fill="both", padx=10, pady=10)

# ===== Run GUI =====
if __name__ == "__main__":
    app = MainView()
    app.mainloop()
