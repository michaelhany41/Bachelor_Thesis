import socket
import keyboard  # Requires `pip install keyboard`
import time

# ESP32 details
ESP_IP = "192.168.1.126"  # Change this to your ESP32's IP
ESP_PORT = 1234

# Create UDP socket
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Function to send commands
def send_command(command):
    udp_socket.sendto(command.encode(), (ESP_IP, ESP_PORT))
    print(f"Sent: {command}")

print("Press 'W' to move forward, 'S' to move backward. Release to stop.")
print("Press 'Q' to exit.")

last_command = ""  # Store the last sent command

# Main loop
while True:
    try:
        if keyboard.is_pressed("w"):
            if last_command != "W":  # Send only if different from last command
                send_command("W")
                last_command = "W"

        elif keyboard.is_pressed("s"):
            if last_command != "S":
                send_command("S")
                last_command = "S"

        else:
            if last_command != "STOP":  # Send "STOP" only once
                send_command("STOP")
                last_command = "STOP"

        # **Check if "Q" is pressed to stop the script**
        if keyboard.is_pressed("q"):
            print("\nStopping script...")
            send_command("STOP")  # Ensure motors stop before exiting
            break  # Exit loop

        time.sleep(0.1)  # Small delay to reduce CPU usage

    except KeyboardInterrupt:
        print("\nExiting...")
        send_command("STOP")  # Ensure motors stop before exiting
        break

# Close socket when done
udp_socket.close()
print("Script stopped.")
