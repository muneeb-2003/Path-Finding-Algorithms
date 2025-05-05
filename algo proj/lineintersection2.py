import tkinter as tk
import time

class LineIntersectionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Line Intersection Visualizer")

        # Load the background image
        self.background_image = tk.PhotoImage(file="watercolor-splash-white-background.png")  # Replace with the actual image file

        self.canvas = tk.Canvas(root, width=600, height=400, bg="#F0F0F0")
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.background_image)
        self.canvas.pack(expand=tk.YES, fill=tk.BOTH)

        self.lines = []

        self.canvas.bind("<Button-1>", self.add_point)
        self.run_button = tk.Button(root, text="Show Intersections", command=self.show_intersections)
        self.run_button.pack()

        # Draw x-axis and y-axis
        self.draw_axes(600, 400)

    def draw_axes(self, width, height):
        # Draw grid lines
        for i in range(-width//2, width//2, 50):
            self.canvas.create_line(i + width//2, 0, i + width//2, height, fill="lightgray", width=1)
        for i in range(-height//2, height//2, 50):
            self.canvas.create_line(0, i + height//2, width, i + height//2, fill="lightgray", width=1)

        # Draw X and Y axes
        self.canvas.create_line(0, height/2, width, height/2, fill="black", width=1)  # X-axis
        self.canvas.create_line(width/2, 0, width/2, height, fill="black", width=1)  # Y-axis

        # Draw ticks and labels
        for i in range(-width//2, width//2, 50):
            self.canvas.create_text(i + width//2, height//2 + 10, text=str(i), anchor=tk.N)

        for i in range(-height//2, height//2, 50):
            self.canvas.create_text(width//2 + 10, i + height//2, text=str(-i), anchor=tk.W)

    def add_point(self, event):
        x, y = event.x, event.y
        self.lines.append([(x, y), None])
        self.canvas.create_oval(x - 2, y - 2, x + 2, y + 2, fill="black")

        if len(self.lines) % 2 == 0:
            self.canvas.create_line(self.lines[-2][0], self.lines[-1][0])

    def show_intersections(self):
        self.canvas.delete("intersections")

        start_time = time.time()

        for i in range(0, len(self.lines), 2):
            for j in range(i + 2, len(self.lines), 2):
                intersection = self.get_line_intersection(self.lines[i][0], self.lines[i + 1][0],
                                                           self.lines[j][0], self.lines[j + 1][0])

                if intersection:
                    x, y = intersection
                    self.canvas.create_oval(x - 2, y - 2, x + 2, y + 2, fill="red", tags="intersections")

        end_time = time.time()

        # Calculate and print the time complexity
        elapsed_time = end_time - start_time
        time_complexity_label = tk.Label(self.root, text=f"Actual Time Complexity: O(n^2), Calculated Time: {elapsed_time:.6f} seconds")
        time_complexity_label.pack()

    @staticmethod
    def get_line_intersection(p1, p2, p3, p4):
        x1, y1 = p1
        x2, y2 = p2
        x3, y3 = p3
        x4, y4 = p4

        # Counter-clockwise turn test
        def ccw(A, B, C):
            return (C[1] - A[1]) * (B[0] - A[0]) > (B[1] - A[1]) * (C[0] - A[0])

        # Check for intersection using counter-clockwise turn test
        if ccw(p1, p3, p4) != ccw(p2, p3, p4) and ccw(p1, p2, p3) != ccw(p1, p2, p4):
            # Calculate the intersection point
            denominator = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
            if denominator == 0:
                return None  # Lines are parallel

            px = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / denominator
            py = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / denominator

            return px, py
        else:
            return None  # No intersection

if __name__ == "__main__":
    root = tk.Tk()
    app = LineIntersectionApp(root)
    root.mainloop()
