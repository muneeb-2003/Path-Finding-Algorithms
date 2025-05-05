import tkinter as tk
import math
import time

class JarvisMarchApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Jarvis March Convex Hull Visualizer")

        # Load the background image
        self.background_image = tk.PhotoImage(file="watercolor-splash-white-background.png")  # Replace with the actual image file

        # Create a canvas with the background image
        self.canvas = tk.Canvas(root, width=600, height=400)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.background_image)
        self.canvas.pack(expand=tk.YES, fill=tk.BOTH)

        self.points = []
        self.convex_hull = []

        self.canvas.bind("<Button-1>", self.add_point)
        self.run_button = tk.Button(root, text="Run Jarvis March", command=self.run_jarvis_march)
        self.run_button.pack()

        # Display labels for time complexity
        self.jarvis_march_time_label = tk.Label(root, text="Time Complexity (Jarvis March): ")
        self.jarvis_march_time_label.pack()

        self.logarithmic_algorithm_time_label = tk.Label(root, text="Time Complexity (Logarithmic Algorithm): ")
        self.logarithmic_algorithm_time_label.pack()

        # Label for O(log n)
        self.ologn_label = tk.Label(root, text="O(N log n)")
        self.ologn_label.pack()

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
            self.canvas.create_line(x1, y1, x2, y2, fill="blue", width=2, tags="convex_hull")

    def run_jarvis_march(self):
        if len(self.points) < 3:
            return

        # Measure the execution time for Jarvis March
        start_time_jarvis_march = time.time()
        self.convex_hull = self.jarvis_march(self.points)
        end_time_jarvis_march = time.time()

        # Calculate the time complexity for Jarvis March
        time_complexity_jarvis_march = end_time_jarvis_march - start_time_jarvis_march

        # Display the time complexity for Jarvis March
        self.jarvis_march_time_label.config(text=f"Time Complexity (Jarvis March): {time_complexity_jarvis_march:.6f} seconds")

        # Measure the execution time for the hypothetical logarithmic algorithm
        start_time_logarithmic_algorithm = time.time()
        self.logarithmic_algorithm(self.points)
        end_time_logarithmic_algorithm = time.time()

        # Calculate the time complexity for the hypothetical logarithmic algorithm
        time_complexity_logarithmic_algorithm = end_time_logarithmic_algorithm - start_time_logarithmic_algorithm

        # Display the time complexity for the hypothetical logarithmic algorithm
        self.logarithmic_algorithm_time_label.config(text=f"Time Complexity (Logarithmic Algorithm): {time_complexity_logarithmic_algorithm:.6f} seconds")

        # Display O(log n) for explanatory purposes (not a real logarithmic algorithm)
        self.ologn_label.config(text="O(log n)")

        # Draw the convex hulls for visualization
        self.draw_convex_hull()

    def logarithmic_algorithm(self, points):
        # Hypothetical algorithm with logarithmic time complexity
        # (Note: This is just a placeholder for explanatory purposes; not a real logarithmic algorithm)
        n = len(points)
        midpoint = n // 2
        left_half = points[:midpoint]
        right_half = points[midpoint:]

        # Recursive calls with logarithmic time complexity
        self.logarithmic_algorithm(left_half)
        self.logarithmic_algorithm(right_half)

        # ... (additional hypothetical logarithmic time complexity operations)

    def jarvis_march(self, points):
        def orientation(p, q, r):
            val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
            if val == 0:
                return 0
            return 1 if val > 0 else 2

        n = len(points)
        hull = []

        # Find the leftmost point
        leftmost = min(points, key=lambda p: p[0])
        hull.append(leftmost)

        while True:
            endpoint = points[0]
            for i in range(1, n):
                if endpoint == hull[-1] or orientation(hull[-1], points[i], endpoint) == 2:
                    endpoint = points[i]

            if endpoint == hull[0]:
                break

            hull.append(endpoint)
            
        # Draw the convex hull
        self.canvas.delete("convex_hull")
        for i in range(len(hull)):
            x1, y1 = hull[i]
            x2, y2 = hull[(i + 1) % len(hull)]
            self.canvas.create_line(x1, y1, x2, y2, fill="blue", width=2, tags="convex_hull")

        return hull

if __name__ == "__main__":
    WIDTH, HEIGHT = 600, 400
    root = tk.Tk()
    app = JarvisMarchApp(root)
    root.mainloop()
