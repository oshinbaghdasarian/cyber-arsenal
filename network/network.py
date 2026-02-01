import socket

target_ip = input("Enter target IP: ")

print("Scanning target:", target_ip)
print("Starting scan...\n")

def grab_banner(sock):
    try:
        sock.send(b"HEAD / HTTP/1.1\r\n\r\n")
        banner = sock.recv(1024).decode(errors="ignore")
        return banner.strip()
    except:
        return None

with open("scan_results.txt", "w") as file:
    file.write(f"Scan results for {target_ip}\n")
    file.write("=" * 30 + "\n")

    for port in range(1, 65536):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.3)

            result = s.connect_ex((target_ip, port))

            if result == 0:
                banner = grab_banner(s)

                print(f"[+] Port {port} OPEN")
                file.write(f"Port {port} OPEN\n")

                if banner:
                    print(f"    Service info: {banner.splitlines()[0]}")
                    file.write(f"    Service info: {banner.splitlines()[0]}\n")
                else:
                    print("    Service info: Unknown")
                    file.write("    Service info: Unknown\n")

            s.close()
        except:
            pass

print("\nScan completed. Results saved to scan_results.txt")
