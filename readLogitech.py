import pygame

# Initialize Pygame
pygame.init()

# Initialize the joystick
pygame.joystick.init()

# Check if the G920 is connected
if pygame.joystick.get_count() == 0:
    print("No joystick detected!")
    exit()

# Get the G920 joystick
g920 = pygame.joystick.Joystick(0)
g920.init()

print(f"Detected: {g920.get_name()}")

# Main loop to read input
running = True
while running:
    pygame.event.pump()  # Process events

    # Read accelerator and brake (usually axes 1 and 2)
    accelerator = (1 - g920.get_axis(1)) / 2  # Normalize 0 (unpressed) to 1 (fully pressed)
    brake = (1 - g920.get_axis(2)) / 2
    clutch = (1 - g920.get_axis(3))/2
    # Read steering (usually axis 0)
    steering = g920.get_axis(0)  # -1 (left), 0 (center), 1 (right)

    # Read buttons (e.g., A, B, X, Y)
    a_button = g920.get_button(0)  # A button (0 = not pressed, 1 = pressed)
    b_button = g920.get_button(1)  # B button

    # Print values
    print(f"Steering: {steering:.2f}, Accelerator: {accelerator:.2f}, Brake: {brake:.2f}, Clutch: {clutch:.2f}, A: {a_button}, B: {b_button}")

    # Exit condition (Press B to stop)
    if b_button:
        running = False

pygame.quit()
