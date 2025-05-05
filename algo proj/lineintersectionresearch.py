import tkinter as tk
import math

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

def orientation(p, q, r):
    val = (q.y - p.y) * (r.x - q.x) - (q.x - p.x) * (r.y - q.y)
    if val == 0:
        return 0  # Collinear
    return 1 if val > 0 else 2  # Clockwise or Counterclockwise

def on_segment(p, q, r):
    return (q.x <= max(p.x, r.x) and q.x >= min(p.x, r.x) and
            q.y <= max(p.y, r.y) and q.y >= min(p.y, r.y))

def do_intersect(p1, q1, p2, q2):
    o1 = orientation(p1, q1, p2)
    o2 = orientation(p1, q1, q2)
    o3 = orientation(p2, q2, p1)
    o4 = orientation(p2, q2, q1)

    if o1 != o2 and o3 != o4:
        return True

    if o1 == 0 and on_segment(p1, p2, q1):
        return True
    if o2 == 0 and on_segment(p1, q2, q1):
        return True
    if o3 == 0 and on_segment(p2, p1, q2):
        return True
    if o4 == 0 and on_segment(p2, q1, q2):
        return True

    return False

def distance_point_to_line(p, a, b):
    numerator = abs((b.y - a.y) * p.x - (b.x - a.x) * p.y + b.x * a.y - b.y * a.x)
    denominator = math.sqrt((b.y - a.y)**2 + (b.x - a.x)**2)
    return numerator / denominator

class LineIntersectApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Line Intersection and Shortest Distance")

        # Load background image
        self.background_image = tk.PhotoImage(file="watercolor-splash-white-background.png")  # Replace with the actual image file path
        self.canvas = tk.Canvas(root, width=600, height=400)
        self.canvas.pack()

        # Create a background image item
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.background_image)

        # Draw axes
        self.canvas.create_line(50, 350, 550, 350, width=2)  # X-axis
        self.canvas.create_line(50, 50, 50, 350, width=2)  # Y-axis

        # Add labels for axes
        self.canvas.create_text(575, 360, text="X-axis")
        self.canvas.create_text(40, 25, text="Y-axis", anchor=tk.W)

        # Add numbering to X-axis
        for i in range(1, 6):
            x_position = 50 + i * 100
            self.canvas.create_line(x_position, 350, x_position, 355, width=2)
            self.canvas.create_text(x_position, 365, text=str(i * 100))

        self.points = []
        self.lines = []

        self.canvas.bind("<Button-1>", self.mark_point)
        self.check_intersection_button = tk.Button(root, text="Check Intersection", command=self.check_intersection)
        self.check_intersection_button.pack(pady=10)

        self.result_label = tk.Label(root, text="")
        self.result_label.pack()

        self.distance_label = tk.Label(root, text="")
        self.distance_label.pack()

    def mark_point(self, event):
        x, y = event.x, event.y
        self.points.append(Point(x, y))
        self.canvas.create_oval(x - 2, y - 2, x + 2, y + 2, fill='blue')

        if len(self.points) >= 2:
            self.lines.append(self.canvas.create_line(self.points[-2].x, self.points[-2].y, x, y, fill='black'))

    def check_intersection(self):
        if len(self.points) == 4:
            point1, point2, point3, point4 = self.points[0], self.points[1], self.points[2], self.points[3]

            if do_intersect(point1, point2, point3, point4):
                self.result_label.config(text="Lines intersect")
            else:
                self.result_label.config(text="Lines do not intersect")

            if len(self.points) == 5:
                point = self.points[4]
                line_start, line_end = self.points[2], self.points[3]
                distance = distance_point_to_line(point, line_start, line_end)
                self.distance_label.config(text=f"Shortest distance from point to line segment: {distance:.2f}")
        else:
            self.result_label.config(text="Please mark four points for line intersection check")
            self.distance_label.config(text="")

# Example usage:
if __name__ == "__main__":
    root = tk.Tk()
    app = LineIntersectApp(root)
    root.mainloop()
