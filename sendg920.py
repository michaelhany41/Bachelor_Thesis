import socket
import pygame
import time

ESP_IP = "192.168.1.126"  # Change this to your ESP32's IP
ESP_PORT = 1234

#initialize UDP socket 
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#initialize pygame
pygame.init()
pygame.joystick.init()

#check for G920
if pygame.joystick.get_count() == 0 :
    print("no joystick detected")
    exit()

g920 = pygame.joystick.Joystick(0)
g920.init()
print(f"Detected: {g920.get_name()}")

def send_command(command):
    udp_socket.sendto(command.encode(), (ESP_IP, ESP_PORT))
    print(f"Sent: {command}")



#last_command1 =""
last_command = ""
motor_speed = 0

def normalize_pedal(value):
    return int(((1 - value) / 2) * 255)  # Normalize -1 to 1 range to 0-255


STEER_DEADZONE = 0.02  # Ignore small steering movements
PEDAL_DEADZONE = 10    # Ignore very light pedal presses


print("Use the G920 pedals and wheel to control the ESP32.")
print("Press 'B' on the wheel to exit.")

running = True
while running:
    pygame.event.pump()

    # Read steering (axis 0)
    steering = g920.get_axis(0)  # -1 (left) to 1 (right)

    # Read accelerator (axis 1) and brake (axis 2)
    accelerator = normalize_pedal(g920.get_axis(1))
    brake = normalize_pedal(g920.get_axis(2))

    if abs(steering) < STEER_DEADZONE:
        steering = 0
    if accelerator < PEDAL_DEADZONE:
        accelerator = 0
    if brake < PEDAL_DEADZONE:
        brake = 0

    command = f"STEER:{int(steering * 100)},ACC:{accelerator},BRAKE:{brake}"

    # Send only if the command has changed
    if command != last_command:
        send_command(command)
        last_command = command

    # Exit if 'B' button is pressed (button index 1)
    if g920.get_button(1):
        print("Exiting...")
        send_command("STOP")
        running = False

    time.sleep(0.1)

# Close socket when done
udp_socket.close()
pygame.quit()
print("Script stopped.")