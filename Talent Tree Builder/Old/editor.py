import json
import customtkinter as ctk
from tkinter import filedialog, messagebox

# Initialize appearance
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class JSONEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("JSON Tab/Button Editor")
        self.root.geometry("1100x500")

        self.tabs_data = []
        self.current_tab_index = 0

        # --- UI Components ---
        # Tab selection
        self.tab_var = ctk.StringVar()
        self.tab_menu = ctk.CTkOptionMenu(root, variable=self.tab_var, values=[], command=self.change_tab)
        self.tab_menu.grid(row=0, column=0, columnspan=6, sticky="ew", padx=10, pady=10)

        # Grid of entries for buttons
        self.entries = [[None for _ in range(6)] for _ in range(5)]
        for r in range(5):
            for c in range(6):
                e = ctk.CTkEntry(root, width=150, height=35)
                e.grid(row=r+1, column=c, padx=10, pady=10)
                self.entries[r][c] = e

        # Load and save buttons
        self.load_btn = ctk.CTkButton(root, text="Load JSON", command=self.load_json)
        self.load_btn.grid(row=6, column=0, columnspan=3, sticky="ew", padx=10, pady=10)

        self.save_btn = ctk.CTkButton(root, text="Save JSON", command=self.save_json)
        self.save_btn.grid(row=6, column=3, columnspan=3, sticky="ew", padx=10, pady=10)

    def load_json(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])
        if not file_path:
            return
        with open(file_path, 'r') as f:
            self.tabs_data = json.load(f).get("tabs", [])
        self.update_tab_menu()
        self.load_tab_data()

    def save_json(self):
        self.update_tab_data()
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json")])
        if not file_path:
            return
        with open(file_path, 'w') as f:
            json.dump({"tabs": self.tabs_data}, f, indent=4)
        messagebox.showinfo("Saved", f"JSON saved to {file_path}")

    def update_tab_menu(self):
        values = [tab["name"] for tab in self.tabs_data]
        self.tab_menu.configure(values=values)
        if self.tabs_data:
            self.select_tab(0)

    def select_tab(self, index):
        self.current_tab_index = index
        self.tab_var.set(self.tabs_data[index]["name"])
        self.load_tab_data()

    def change_tab(self, choice):
        for i, tab in enumerate(self.tabs_data):
            if tab["name"] == choice:
                self.select_tab(i)
                break

    def load_tab_data(self):
        if not self.tabs_data:
            return
        tab = self.tabs_data[self.current_tab_index]
        buttons_grid = [[None for _ in range(6)] for _ in range(5)]
        for btn in tab.get("buttons", []):
            r = (btn["position"] - 1) % 5
            c = btn["treeTier"] - 1
            buttons_grid[r][c] = f"{btn.get('label','')}|{btn.get('description','')}"

        # Load entries
        for r in range(5):
            for c in range(6):
                self.entries[r][c].delete(0, ctk.END)
                if buttons_grid[r][c]:
                    self.entries[r][c].insert(0, buttons_grid[r][c])

    def update_tab_data(self):
        tab = self.tabs_data[self.current_tab_index]
        tab["buttons"] = []
        for r in range(5):
            for c in range(6):
                val = self.entries[r][c].get().strip()
                if val:
                    if '|' in val:
                        label, description = val.split('|', 1)
                    else:
                        label, description = val, ""
                    tab["buttons"].append({
                        "position": r + 1,
                        "treeTier": c + 1,
                        "label": label.strip(),
                        "description": description.strip()
                    })

if __name__ == "__main__":
    root = ctk.CTk()
    app = JSONEditor(root)
    root.mainloop()
