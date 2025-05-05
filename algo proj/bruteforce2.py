import tkinter as tk
import math
import time

def add_point(event):
    x, y = event.x, event.y
    points.append((x, y))
    canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill="black")

def orientation(p, q, r):
    val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
    if val == 0:
        return 0
    return 1 if val > 0 else 2

def brute_force_jarvis_style(points):
    n = len(points)
    if n < 3:
        return points

    hull = []

    # Find the point with the lowest y-coordinate as the starting point
    start_point = min(points, key=lambda p: (p[1], p[0]))
    hull.append(start_point)

    # Sort the remaining points based on the polar angle from the starting point
    sorted_points = sorted(points, key=lambda p: math.atan2(p[1] - start_point[1], p[0] - start_point[0]))

    # Iterate through the sorted points to build the convex hull
    for p in sorted_points:
        while len(hull) > 1 and orientation(hull[-2], hull[-1], p) != 2:
            hull.pop()
            draw_step_by_step(hull)

        hull.append(p)
        draw_step_by_step(hull)

    return hull

def run_algorithm():
    global convex_hull
    algorithm = algorithm_var.get()

    if algorithm == "BruteForce":
        start_time = time.time()
        convex_hull = brute_force_jarvis_style(points)
        end_time = time.time()
        elapsed_time = end_time - start_time

        # Display time complexity estimate
        time_complexity_label.config(text=f"Expected Time Complexity: O(N^2)\nElapsed Time: {elapsed_time:.6f} seconds")

    canvas.delete("all")
    draw_background()  # Draw the background
    draw_axes()
    for x, y in points:
        canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill="black")

    draw_convex_hull(convex_hull)

def draw_background():
    background_image = tk.PhotoImage(file="watercolor-splash-white-background.png")  # Replace with the actual image file
    canvas.create_image(0, 0, anchor=tk.NW, image=background_image)
    canvas.background = background_image  # Keep a reference to avoid garbage collection

def draw_axes():
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

def draw_convex_hull(hull):
    canvas.delete("convex_hull")
    for i in range(len(hull) - 1):
        x1, y1 = hull[i]
        x2, y2 = hull[i + 1]
        canvas.create_line(x1, y1, x2, y2, fill="red", width=2, tags=("convex_hull",))

    if hull:
        x1, y1 = hull[-1]
        x2, y2 = hull[0]
        canvas.create_line(x1, y1, x2, y2, fill="red", width=2, tags=("convex_hull",))

def draw_step_by_step(hull):
    canvas.delete("convex_hull")
    for i in range(len(hull) - 1):
        x1, y1 = hull[i]
        x2, y2 = hull[i + 1]
        canvas.create_line(x1, y1, x2, y2, fill="red", width=2, tags=("convex_hull",))
        canvas.update()
        canvas.after(200)  # Delay in milliseconds

    if hull:
        x1, y1 = hull[-1]
        x2, y2 = hull[0]
        canvas.create_line(x1, y1, x2, y2, fill="red", width=2, tags=("convex_hull",))
        canvas.update()
        canvas.after(200)  # Delay in milliseconds

if __name__ == "__main__":
    points = []
    convex_hull = []

    WIDTH, HEIGHT = 800, 600

    root = tk.Tk()
    root.title("Convex Hull Visualization")

    canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="white")
    canvas.pack()

    draw_background()  # Draw the background
    draw_axes()  # Draw axes before any points

    canvas.bind("<Button-1>", add_point)

    algorithm_var = tk.StringVar(value="BruteForce")
    brute_force_jarvis_radio = tk.Radiobutton(root, text="BruteForce", variable=algorithm_var, value="BruteForce")
    brute_force_jarvis_radio.pack(side=tk.LEFT)

    btn_run_algorithm = tk.Button(root, text="Run Brute Force", command=run_algorithm)
    btn_run_algorithm.pack()

    # Label to display time complexity
    time_complexity_label = tk.Label(root, text="")
    time_complexity_label.pack()

    root.mainloop()
