import tkinter as tk
from functools import cmp_to_key

WIDTH, HEIGHT = 800, 600
RED = "red"
BLUE = "white"

def orientation(p, q, r):
    val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
    if val == 0:
        return 0  # Collinear
    return 1 if val > 0 else 2  # Clockwise or Counterclockwise

def compare(p1, p2):
    o = orientation(p0, p1, p2)
    if o == 0:
        return (p1[0] - p0[0]) * 2 + (p1[1] - p0[1]) * 2 - (p2[0] - p0[0]) * 2 - (p2[1] - p0[1]) * 2
    return -1 if o == 2 else 1

def incremental_convex_hull(points):
    global p0
    n = len(points)
    
    p0 = min(points, key=lambda point: (point[1], point[0]))

    sorted_points = sorted(points, key=cmp_to_key(compare))

    hull = []
    hull.append(sorted_points[0])
    hull.append(sorted_points[1])

    for i in range(2, n):
        while len(hull) > 1 and orientation(hull[-2], hull[-1], sorted_points[i]) != 2:
            hull.pop()
        hull.append(sorted_points[i])

    return hull

def draw_axes(canvas):
    # Draw grid lines
    for i in range(-WIDTH//2, WIDTH//2, 50):
        canvas.create_line(i + WIDTH//2, 0, i + WIDTH//2, HEIGHT, fill="lightgray", width=1)
    for i in range(-HEIGHT//2, HEIGHT//2, 50):
        canvas.create_line(0, i + HEIGHT//2, WIDTH, i + HEIGHT//2, fill="lightgray", width=1)

    # Draw X and Y axes
    canvas.create_line(0, HEIGHT/2, WIDTH, HEIGHT/2, fill="black", width=1)  # X-axis
    canvas.create_line(WIDTH/2, 0, WIDTH/2, HEIGHT, fill="black", width=1)  # Y-axis

    # Draw ticks and labels
    for i in range(-WIDTH//2, WIDTH//2, 50):
        canvas.create_text(i + WIDTH//2, HEIGHT//2 + 10, text=str(i), anchor=tk.N)

    for i in range(-HEIGHT//2, HEIGHT//2, 50):
        canvas.create_text(WIDTH//2 + 10, i + HEIGHT//2, text=str(-i), anchor=tk.W)

class ConvexHullApp:
    def __init__(self, root):
        self.root = root
        self.root.title('Incremental Convex Hull Visualization')
        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="white")
        self.canvas.pack()

        self.points = []

        # Add background image
        self.background_image = tk.PhotoImage(file="watercolor-splash-white-background.png")  # Replace with the actual image file
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.background_image)
        self.canvas.background = self.background_image  # Keep a reference to avoid garbage collection

        self.canvas.bind('<Button-1>', self.add_point)

        # Display the estimated time complexity
        self.time_complexity_label = tk.Label(root, text="Estimated time complexity: O(n log h)")
        self.time_complexity_label.pack()

        # Draw axes
        draw_axes(self.canvas)

    def add_point(self, event):
        x, y = event.x, event.y
        self.points.append((x, y))
        self.canvas.create_oval(x - 2, y - 2, x + 2, y + 2, fill=RED)

        if len(self.points) >= 3:
            hull = incremental_convex_hull(self.points)
            self.canvas.delete(BLUE)
            self.canvas.create_polygon(hull, outline=BLUE)

if __name__ == "__main__":
    root = tk.Tk()
    app = ConvexHullApp(root)
    root.mainloop()
