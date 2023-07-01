#!/usr/bin/env python3

import socket
import requests

# Clear the contents of open_ports.txt
with open("open_ports.txt", "w") as file:
    pass

def check_port(ip, port):
    try:
        # Exclude IP addresses ending with '.25x'
        if ip.split('.')[-1].startswith('25'):
            return

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)  # Set the socket connection timeout to 2 seconds
        result = sock.connect_ex((ip, port))
        if result == 0:
            print(f"Port {port} is open on {ip}")
            url = f"http://{ip}:{port}/"

            try:
                response = requests.get(url, timeout=2)  # Set the HTTP request timeout to 2 seconds

                if "eventID" in response.text:
                    with open("open_ports.txt", "a") as file:
                        file.write(ip + "\n")
                    print(f"Content of {url} contains 'eventID'. IP address added to the list.")
                else:
                    print(f"Content of {url} does not contain 'eventID'. IP address not added.")

            except requests.exceptions.Timeout:
                print(f"Timeout occurred while accessing {url}. IP address not added.")

        else:
            print(f"Port {port} is closed on {ip}")
        sock.close()

    except socket.error as e:
        print(f"Error: {e}")

networks = ["123.6.81.0/24", "183.146.28.0/24"]
port = 80

for network in networks:
    ip_parts = network.split('/')
    network_ip = ip_parts[0]
    network_prefix = int(ip_parts[1])

    for i in range(2**(32 - network_prefix)):
        ip = ".".join(network_ip.split('.')[:-1] + [str(int(network_ip.split('.')[-1]) + i)])
        check_port(ip, port)
