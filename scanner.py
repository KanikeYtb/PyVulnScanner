import socket
import threading
from queue import Queue

def scan_port(ip, port, result_queue):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)  # Aguarda 1 segundo
        result = sock.connect_ex((ip, port))
        if result == 0:
            try:
                service = socket.getservbyport(port)
            except:
                service = "Desconhecido"
            result_queue.put(f"Porta {port} aberta: {service}")
        sock.close()
    except:
        pass

def main(ip, ports):
    print(f"Escaneando {ip}...")
    result_queue = Queue()
    threads = []
    
    for port in ports:
        t = threading.Thread(target=scan_port, args=(ip, port, result_queue))
        t.start()
        threads.append(t)
    
    for t in threads:
        t.join()
    
    results = []
    while not result_queue.empty():
        results.append(result_queue.get())
    
    if results:
        print(f"Resultados para {ip}:")
        for res in results:
            print(res)
    else:
        print(f"Nenhuma porta aberta encontrada em {ip}.")

if __name__ == "__main__":
    target_ip = "INSIRA_O_IP_AQUI"  # insira o seu ip
    common_ports = [80, 443, 22, 21]  # Portas para HTTP, HTTPS, SSH, FTP
    main(target_ip, common_ports)
