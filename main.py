import random
import tkinter as tk
class DesktopPet:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("桌宠")
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.wm_attributes("-transparentcolor", "white")
        self.root.configure(bg="white")

        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()

        self.pet_width = 180
        self.pet_height = 180
        self.x = random.randint(0, max(0, self.screen_width - self.pet_width))
        self.y = random.randint(0, max(0, self.screen_height - self.pet_height - 40))

        self.canvas = tk.Canvas(
            self.root,
            width=self.pet_width,
            height=self.pet_height,
            highlightthickness=0,
            bg="white",
        )
        self.canvas.pack()

        self.drag_data = {"x": 0, "y": 0}
        self.is_dragging = False

        self.state = "idle"
        self.frame = 0
        self.mood = "happy"
        self.direction = 1
        self.move_timer = 0

        self.root.geometry(f"{self.pet_width}x{self.pet_height}+{self.x}+{self.y}")
        self.create_bindings()
        self.draw_pet()
        self.schedule_animation()

    def create_bindings(self):
        self.canvas.bind("<ButtonPress-1>", self.start_drag)
        self.canvas.bind("<B1-Motion>", self.do_drag)
        self.canvas.bind("<ButtonRelease-1>", self.stop_drag)
        self.canvas.bind("<Button-3>", self.show_menu)
        self.canvas.bind("<Button-2>", self.toggle_state)

    def start_drag(self, event):
        self.is_dragging = True
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y
        self.state = "drag"

    def do_drag(self, event):
        dx = event.x - self.drag_data["x"]
        dy = event.y - self.drag_data["y"]
        self.x += dx
        self.y += dy
        self.x = min(max(self.x, 0), self.screen_width - self.pet_width)
        self.y = min(max(self.y, 0), self.screen_height - self.pet_height)
        self.root.geometry(f"{self.pet_width}x{self.pet_height}+{self.x}+{self.y}")

    def stop_drag(self, event):
        self.is_dragging = False
        self.state = "idle"

    def show_menu(self, event):
        menu = tk.Menu(self.root, tearoff=0)
        menu.add_command(label="关闭桌宠", command=self.root.destroy)
        menu.add_command(label="切换心情", command=self.change_mood)
        menu.tk_popup(event.x_root, event.y_root)

    def toggle_state(self, event=None):
        if self.state == "idle":
            self.state = "happy"
            self.mood = "happy"
        else:
            self.state = "idle"

    def change_mood(self):
        self.mood = random.choice(["happy", "curious", "sleepy", "surprised"])
        self.state = "idle"

    def schedule_animation(self):
        self.update_position()
        self.draw_pet()
        self.root.after(120, self.schedule_animation)

    def update_position(self):
        if self.is_dragging:
            return

        self.move_timer += 1
        if self.move_timer > 20:
            self.move_timer = 0
            self.direction = random.choice([-1, 0, 1])

        if self.direction != 0:
            self.x += self.direction * 3
            self.x = min(max(self.x, 0), self.screen_width - self.pet_width)
            self.state = "walk"
        else:
            self.state = "idle"

        if random.random() < 0.004:
            self.change_mood()

        self.root.geometry(f"{self.pet_width}x{self.pet_height}+{self.x}+{self.y}")
        self.frame = (self.frame + 1) % 4

    def draw_pet(self):
        self.canvas.delete("all")
        self.draw_shadow()
        self.draw_body()
        self.draw_face()
        self.draw_ears()
        self.draw_tail()

    def draw_shadow(self):
        self.canvas.create_oval(
            50,
            145,
            130,
            170,
            fill="#a1a1a1",
            outline="",
        )

    def draw_body(self):
        color = "#ffcc88" if self.mood != "sleepy" else "#d8b57c"
        self.canvas.create_oval(25, 45, 155, 150, fill=color, outline="#6b4d2f", width=2)
        self.canvas.create_oval(60, 70, 120, 110, fill="#fff7d1", outline="", width=0)

    def draw_face(self):
        eye_color = "black"
        mouth = "\u25cf"
        left_eye_x = 65
        right_eye_x = 115
        eye_y = 80

        if self.mood == "happy":
            self.canvas.create_arc(55, 90, 75, 110, start=0, extent=-180, style="arc", width=2)
            self.canvas.create_arc(105, 90, 125, 110, start=0, extent=-180, style="arc", width=2)
        elif self.mood == "sleepy":
            self.canvas.create_line(60, 80, 70, 80, fill=eye_color, width=3)
            self.canvas.create_line(110, 80, 120, 80, fill=eye_color, width=3)
            mouth = "Z"
        elif self.mood == "curious":
            self.canvas.create_oval(left_eye_x, eye_y, left_eye_x + 8, eye_y + 12, fill=eye_color)
            self.canvas.create_oval(right_eye_x, eye_y, right_eye_x + 8, eye_y + 12, fill=eye_color)
            mouth = "?"
        else:
            self.canvas.create_oval(left_eye_x, eye_y, left_eye_x + 8, eye_y + 12, fill=eye_color)
            self.canvas.create_oval(right_eye_x, eye_y, right_eye_x + 8, eye_y + 12, fill=eye_color)

        if self.mood != "curious":
            self.canvas.create_oval(left_eye_x, eye_y, left_eye_x + 10, eye_y + 12, fill=eye_color)
            self.canvas.create_oval(right_eye_x, eye_y, right_eye_x + 10, eye_y + 12, fill=eye_color)

        self.canvas.create_text(90, 115, text=mouth, font=("Arial", 18, "bold"), fill="#6b4d2f")

    def draw_ears(self):
        self.canvas.create_polygon(40, 45, 55, 10, 70, 45, fill="#ffcc88", outline="#6b4d2f", width=2)
        self.canvas.create_polygon(140, 45, 125, 10, 110, 45, fill="#ffcc88", outline="#6b4d2f", width=2)

    def draw_tail(self):
        tail_base_x = 160
        tail_base_y = 95
        phase = self.frame % 4
        offset = (phase - 1.5) * 4
        self.canvas.create_line(
            tail_base_x,
            tail_base_y,
            tail_base_x + 30,
            tail_base_y - 20 + offset,
            tail_base_x + 40,
            tail_base_y - 10 + offset,
            smooth=True,
            width=10,
            fill="#ffcc88",
        )

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = DesktopPet()
    app.run()
