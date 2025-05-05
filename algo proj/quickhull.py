import tkinter as tk
import time

class QuickHullGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Quick Hull Algorithm")

        # Load the background image
        self.background_image = tk.PhotoImage(file="watercolor-splash-white-background.png")  # Replace with the actual image file

        self.canvas = tk.Canvas(master, width=600, height=400)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.background_image)
        self.canvas.pack()

        self.points = []

        self.canvas.bind("<Button-1>", self.add_point)
        self.solve_button = tk.Button(master, text="Run Quickelemination", command=self.solve_quick_hull)
        self.solve_button.pack()

        self.time_complexity_label = tk.Label(master, text="")
        self.time_complexity_label.pack()

        self.draw_axes()

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

    def add_point(self, event):
        x, y = event.x, event.y
        self.points.append((x, y))
        self.canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill="black")

    def quick_hull(self, points):
        if len(points) <= 1:
            return points

        def dist(p, q, r):
            x1, y1 = p
            x2, y2 = q
            x3, y3 = r
            return abs((y2 - y1) * (x3 - x1) - (x2 - x1) * (y3 - y1))

        def find_side(p, q, r):
            val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
            if val > 0:
                return 1
            elif val < 0:
                return -1
            else:
                return 0

        def hull_set(p, q, points):
            hull = []
            for r in points:
                if find_side(p, q, r) == -1:
                    hull.append(r)
            return hull

        def quick_hull_rec(a, b, points):
            if not points:
                return []

            max_dist = -1
            farthest_point = None

            for r in points:
                d = dist(a, b, r)
                if d > max_dist:
                    max_dist = d
                    farthest_point = r

            if not farthest_point:
                return []

            hull = []

            hull.extend(quick_hull_rec(a, farthest_point, hull_set(a, farthest_point, points)))
            hull.append(farthest_point)
            hull.extend(quick_hull_rec(farthest_point, b, hull_set(farthest_point, b, points)))

            return hull

        points.sort()

        leftmost = points[0]
        rightmost = points[-1]

        upper_hull = quick_hull_rec(leftmost, rightmost, hull_set(leftmost, rightmost, points))
        lower_hull = quick_hull_rec(rightmost, leftmost, hull_set(rightmost, leftmost, points))

        return [leftmost] + upper_hull + [rightmost] + lower_hull

    def solve_quick_hull(self):
        if len(self.points) < 3:
            return

        start_time = time.time()
        convex_hull = self.quick_hull(self.points)
        end_time = time.time()
        elapsed_time = end_time - start_time

        n = len(self.points)
        h = len(convex_hull)
        time_complexity_text = f"Elapsed Time: {elapsed_time:.6f} seconds\nTime Complexity: O({n} * log({h}))"

        self.time_complexity_label.config(text=time_complexity_text)

        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.background_image)
        self.draw_axes()

        for point in self.points:
            self.canvas.create_oval(point[0] - 3, point[1] - 3, point[0] + 3, point[1] + 3, fill="black")

        if convex_hull:
            for i in range(len(convex_hull) - 1):
                self.canvas.create_line(convex_hull[i][0], convex_hull[i][1],
                                        convex_hull[i + 1][0], convex_hull[i + 1][1], fill="red")
            self.canvas.create_line(convex_hull[-1][0], convex_hull[-1][1],
                                    convex_hull[0][0], convex_hull[0][1], fill="red")

if __name__ == "__main__":
    root = tk.Tk()
    app = QuickHullGUI(root)
    root.mainloop()
