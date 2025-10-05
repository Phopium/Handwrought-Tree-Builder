import customtkinter as ctk
import json

class TalentTreeFrame(ctk.CTkFrame):
    def __init__(self, master, button_data, connections=None):
        super().__init__(master)
        self.canvas = ctk.CTkCanvas(self, bg="#404040", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self.buttons = {}
        self.connections = connections or []

        # Place buttons on the canvas
        for talent in button_data:
            row = talent["treeTier"] - 1
            col = talent["position"] - 1
            label = talent["label"]

            btn = ctk.CTkButton(self.canvas, text=label, command=lambda b=label: self.toggle_button(b))
            # Create button as a canvas window
            self.canvas.create_window(
                col * 150 + 75,  # X position
                row * 100 + 50,  # Y position
                window=btn
            )
            self.buttons[label] = btn

        # After the layout is stable, draw connections
        self.after(200, self.draw_connections)

    def toggle_button(self, label):
        """Highlight/deselect a button when clicked"""
        btn = self.buttons[label]
        current_color = btn.cget("fg_color")
        if current_color != ("green"):  # default CTkButton colors
            btn.configure(fg_color="green")  # Selected
        else:
            btn.configure(fg_color="#1F6AA5")  # Back to default

    def draw_connections(self):
        """Draw lines between connected buttons"""
        for (from_label, to_label) in self.connections:
            btn1 = self.buttons[from_label]
            btn2 = self.buttons[to_label]

            # Get absolute button positions
            x1 = btn1.winfo_x() + btn1.winfo_width() // 2
            y1 = btn1.winfo_y() + btn1.winfo_height() // 2
            x2 = btn2.winfo_x() + btn2.winfo_width() // 2
            y2 = btn2.winfo_y() + btn2.winfo_height() // 2

            # Draw the line
            self.canvas.create_line(x1, y1, x2, y2, fill="black", width=2)


def load_config(filename="config.json"):
    with open(filename, "r") as f:
        return json.load(f)


if __name__ == "__main__":
    app = ctk.CTk()
    app.geometry("600x400")

    config = load_config()

    frame = TalentTreeFrame(app, config["buttons"], config.get("connections"))
    frame.pack(fill="both", expand=True, padx=10, pady=10)

    app.mainloop()
