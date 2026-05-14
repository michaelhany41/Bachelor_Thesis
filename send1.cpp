#include <iostream>
#include <winsock2.h>

#pragma comment(lib, "ws2_32.lib")

#define SERVER_IP "192.168.4.1"  // ESP32 AP IP
#define SERVER_PORT 1234

void sendUDPCommand(const char* command) {
    WSADATA wsa;
    SOCKET sock;
    sockaddr_in server;

    // Initialize Winsock
    if (WSAStartup(MAKEWORD(2, 2), &wsa) != 0) {
        std::cerr << "WSAStartup failed!\n";
        return;
    }

    // Create socket
    sock = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);
    if (sock == INVALID_SOCKET) {
        std::cerr << "Socket creation failed!\n";
        WSACleanup();
        return;
    }

    // Setup server address
    server.sin_family = AF_INET;
    server.sin_addr.s_addr = inet_addr(SERVER_IP);
    server.sin_port = htons(SERVER_PORT);

    // Send UDP command
    sendto(sock, command, strlen(command), 0, (sockaddr*)&server, sizeof(server));
    std::cout << "Sent: " << command << std::endl;

    // Cleanup
    closesocket(sock);
    WSACleanup();
}

int main() {
    char key;
    std::cout << "Press W to move forward, S to move backward, and Q to quit.\n";

    while (true) {
        std::cin >> key;
        if (key == 'W' || key == 'w') {
            sendUDPCommand("W");
        } else if (key == 'S' || key == 's') {
            sendUDPCommand("S");
        } else if (key == 'Q' || key == 'q') {
            break;
        }
    }

    return 0;
}
