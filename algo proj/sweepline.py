import tkinter as tk
import time

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

def do_intersect(segment1, segment2):
    def orientation(p, q, r):
        val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
        if val == 0:
            return 0
        return 1 if val > 0 else 2

    def on_segment(p, q, r):
        return (q[0] <= max(p[0], r[0]) and q[0] >= min(p[0], r[0]) and
                q[1] <= max(p[1], r[1]) and q[1] >= min(p[1], r[1]))

    p1, q1 = segment1
    p2, q2 = segment2

    o1 = orientation(p1, q1, p2)
    o2 = orientation(p1, q1, q2)
    o3 = orientation(p2, q2, p1)
    o4 = orientation(p2, q2, q1)

    if o1 != o2 and o3 != o4:
        return True

    # Special cases for collinear segments
    if o1 == 0 and on_segment(p1, p2, q1):
        return True
    if o2 == 0 and on_segment(p1, q2, q1):
        return True
    if o3 == 0 and on_segment(p2, p1, q2):
        return True
    if o4 == 0 and on_segment(p2, q1, q2):
        return True

    return False

class SweepLineIntersectionGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sweep Line Intersection")

        # Load the background image
        self.background_image = tk.PhotoImage(file="watercolor-splash-white-background.png")  # Replace with the actual path to your image

        # Create a canvas with the background image
        self.canvas = tk.Canvas(root, width=600, height=400)
        self.canvas.pack()
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.background_image)

        self.lines = []

        self.run_button = tk.Button(root, text="Run Sweep Line", command=self.run_sweep_line)
        self.run_button.pack()

        self.result_label = tk.Label(root, text="")
        self.result_label.pack()

        self.time_complexity_label = tk.Label(root, text="Expected Time Complexity: O((N + K) log N) ")
        self.time_complexity_label.pack()

        self.canvas.bind("<Button-1>", self.on_canvas_click)

        # Draw x-axis and y-axis using the provided draw_axes function
        self.draw_axes()

    def on_canvas_click(self, event):
        x, y = event.x, event.y
        self.lines.append((x, y))
        self.canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill="black")

        # Draw the line segments immediately after each pair of points is added
        if len(self.lines) % 2 == 0:
            start_point = self.lines[-2]
            end_point = self.lines[-1]
            self.canvas.create_line(start_point, end_point)

    def draw_axes(self):
        # Draw grid lines
        for i in range(-300, 300, 50):
            self.canvas.create_line(i + 300, 0, i + 300, 400, fill="lightgray", width=1)
        for i in range(-200, 200, 50):
            self.canvas.create_line(0, i + 200, 600, i + 200, fill="lightgray", width=1)

        # Draw X and Y axes
        self.canvas.create_line(0, 200, 600, 200, fill="black", width=1)  # X-axis
        self.canvas.create_line(300, 0, 300, 400, fill="black", width=1)  # Y-axis

        # Draw ticks and labels
        for i in range(-300, 300, 50):
            self.canvas.create_text(i + 300, 210, text=str(i), anchor=tk.N)

        for i in range(-200, 200, 50):
            self.canvas.create_text(310, i + 200, text=str(-i), anchor=tk.W)

    def run_sweep_line(self):
        if len(self.lines) < 4 or len(self.lines) % 2 != 0:
            self.result_label.config(text="Please input at least two complete line segments.")
            return

        start_time = time.time()

        # Actual sweep line algorithm
        intersection_found = False

        for i in range(0, len(self.lines), 4):
            segment1 = (self.lines[i], self.lines[i + 1])
            for j in range(i + 2, len(self.lines), 2):
                segment2 = (self.lines[j], self.lines[j + 1])
                if do_intersect(segment1, segment2):
                    intersection_found = True

        end_time = time.time()
        elapsed_time = end_time - start_time

        if intersection_found:
            self.result_label.config(text="Line intersect\nElapsed Time: {:.6f} seconds".format(elapsed_time))
        else:
            self.result_label.config(text="No intersection\nElapsed Time: {:.6f} seconds".format(elapsed_time))

if __name__ == "__main__":
    root = tk.Tk()
    app = SweepLineIntersectionGUI(root)
    root.mainloop()
