import tkinter as tk
from functools import cmp_to_key
import math

class GrahamScanApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Graham's Scan Convex Hull Visualizer")

        self.canvas = tk.Canvas(root, width=600, height=400, bg="white")
        self.canvas.pack(expand=tk.YES, fill=tk.BOTH)

        # Load background image
        self.background_image = tk.PhotoImage(file="watercolor-splash-white-background.png")  # Replace "background_image.png" with your image file
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.background_image)

        self.points = []
        self.convex_hull = []

        self.canvas.bind("<Button-1>", self.add_point)
        self.run_button = tk.Button(root, text="Run Graham's Scan", command=self.run_grahams_scan)
        self.run_button.pack()

        # Label to display time complexity
        self.time_complexity_label = tk.Label(root, text="Time Complexity: ")
        self.time_complexity_label.pack()

        # Label to display O(log n)
        self.logarithmic_complexity_label = tk.Label(root, text="O(log n)")
        self.logarithmic_complexity_label.pack()

        # Draw x-axis and y-axis
        self.draw_axes()

    def draw_axes(self):
        # Draw grid lines
        for i in range(-WIDTH//2, WIDTH//2, 50):
            self.canvas.create_line(i + WIDTH//2, 0, i + WIDTH//2, HEIGHT, fill="lightgray", width=1)
        for i in range(-HEIGHT//2, HEIGHT//2, 50):
            self.canvas.create_line(0, i + HEIGHT//2, WIDTH, i + HEIGHT//2, fill="lightgray", width=1)

        # Draw X and Y axes
        self.canvas.create_line(0, HEIGHT/2, WIDTH, HEIGHT/2, fill="black", width=1)  # X-axis
        self.canvas.create_line(WIDTH/2, 0, WIDTH/2, HEIGHT, fill="black", width=1)  # Y-axis

        # Draw ticks and labels
        for i in range(-WIDTH//2, WIDTH//2, 50):
            self.canvas.create_text(i + WIDTH//2, HEIGHT//2 + 10, text=str(i), anchor=tk.N)

        for i in range(-HEIGHT//2, HEIGHT//2, 50):
            self.canvas.create_text(WIDTH//2 + 10, i + HEIGHT//2, text=str(-i), anchor=tk.W)

    def add_point(self, event):
        x, y = event.x, event.y
        self.points.append((x, y))
        self.canvas.create_oval(x - 2, y - 2, x + 2, y + 2, fill="black")

    def draw_convex_hull(self):
        self.canvas.delete("convex_hull")
        for i in range(len(self.convex_hull)):
            x1, y1 = self.convex_hull[i]
            x2, y2 = self.convex_hull[(i + 1) % len(self.convex_hull)]
            self.canvas.create_line(x1, y1, x2, y2, fill="red", width=2, tags="convex_hull")

    def run_grahams_scan(self):
        if len(self.points) < 3:
            return

        # Measure the execution time for Graham's Scan
        import time
        start_time = time.time()

        self.convex_hull = self.graham_scan(self.points)

        end_time = time.time()

        # Display the time taken for the algorithm
        time_taken = end_time - start_time
        print(f"Time taken for Graham's Scan: {time_taken:.6f} seconds")

        # Calculate and display the time complexity
        time_complexity = time_taken  # Time complexity of the sorting operation
        print(f"Calculated Time Complexity: {time_complexity}")
        self.time_complexity_label.config(text=f"Time Complexity: {time_complexity}")

        # Display O(log n) complexity
        logarithmic_complexity = "O(N log n)"
        self.logarithmic_complexity_label.config(text=logarithmic_complexity)

        self.draw_convex_hull()

    def graham_scan(self, points):
        def cmp_to_origin(p1, p2):
            angle1 = math.atan2(p1[1] - min_y, p1[0] - min_x)
            angle2 = math.atan2(p2[1] - min_y, p2[0] - min_x)
            return 1 if angle1 - angle2 > 0 else -1 if angle1 - angle2 < 0 else 0

        min_point = min(points, key=lambda p: (p[1], p[0]))
        min_x, min_y = min_point

        sorted_points = sorted(points, key=cmp_to_key(cmp_to_origin))

        convex_hull = [sorted_points[0], sorted_points[1]]
        for point in sorted_points[2:]:
            while len(convex_hull) > 1 and self.orientation(convex_hull[-2], convex_hull[-1], point) != 2:
                convex_hull.pop()
            convex_hull.append(point)

        return convex_hull

    def orientation(self, p, q, r):
        val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
        if val == 0:
            return 0
        return 1 if val > 0 else 2

if __name__ == "__main__":
    WIDTH, HEIGHT = 600, 400
    root = tk.Tk()
    app = GrahamScanApp(root)
    root.mainloop()
