import pygame
import subprocess
import sys

def run_algorithm():
    selected_algorithm = algorithms[algorithm_var]
    algorithm_files = {
        "graham scan": "ghramscan2.py",
        "jarvis march": "jarvismarch2.py",
        "bruteforce": "bruteforce2.py",
        "quick elimination" : "quickhull.py",
        "incremental convex hull":"incrementalconvex.py",
        "line intersection": "lineintersection2.py",
        "line intersection2" : "lineintersection_2.py",
        "sweep line intersection": "sweepline.py"
        
    }

    selected_file = algorithm_files.get(selected_algorithm)

    if selected_file:
        subprocess.run(["python", selected_file])
    else:
        print("Invalid selection")

# Initialize Pygame
pygame.init()

# Set up Pygame window
window_size = (1500, 700)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Algorithm Runner")

# Pygame clock for controlling the frame rate
clock = pygame.time.Clock()

# Load background image
background_image = pygame.image.load("algobg.JPEG")
background_image = pygame.transform.scale(background_image, window_size)

# Colors
light_blue = (255, 0, 230)

# Fonts
font = pygame.font.Font(None, 30)

# Create a dropdown menu
algorithms = ["graham scan", "jarvis march", "bruteforce","quick elimination", "incremental convex hull", "line intersection","line intersection2","sweep line intersection"]
algorithm_var = 0  # Set the default value

# Run the Pygame event loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if algorithm_dropdown_rect.collidepoint(event.pos):
                algorithm_var = (algorithm_var + 1) % len(algorithms)
            elif run_button_rect.collidepoint(event.pos):
                run_algorithm()

    # Draw background image
    screen.blit(background_image, (0, 0))

    # Draw label
    label_text = font.render("Select an algorithm:", True, (0,139,139))
    label_rect = label_text.get_rect(center=(window_size[0] // 2, 50))
    screen.blit(label_text, label_rect)

    # Draw dropdown menu
    algorithm_dropdown_text = font.render(algorithms[algorithm_var], True, (0,139,139))
    algorithm_dropdown_rect = algorithm_dropdown_text.get_rect(center=(window_size[0] // 2, 120))
    screen.blit(algorithm_dropdown_text, algorithm_dropdown_rect)

    # Draw run button
    pygame.draw.rect(screen, (0,139,139), (window_size[0] // 4, 200, window_size[0] // 2, 40))
    run_button_text = font.render("Run Algorithm", True, (3, 3, 3))
    run_button_rect = run_button_text.get_rect(center=(window_size[0] // 2, 220))
    screen.blit(run_button_text, run_button_rect)

    pygame.display.flip()

    # Cap the frame rate
    clock.tick(30)

# Quit Pygame
pygame.quit()

# Exit the script
sys.exit()
