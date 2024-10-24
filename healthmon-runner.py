import paramiko
import time
import getpass

# Lista di indirizzi IP
ip_list = [
    "192.168.1.1",
    "192.168.1.2"
]

# Richiedi le credenziali una sola volta
username = input("Inserisci il nome utente: ")
password = getpass.getpass("Inserisci la password: ")

# Stringa da cercare
search_string = "System Health Report Page"

# Funzione per connettersi tramite SSH e catturare l'output della console
def ssh_connect(ip, username, password, search_string):
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(ip, username=username, password=password)
        print(f"Connessione riuscita a {ip}")

        # Apri una sessione interattiva
        channel = client.invoke_shell()
        
        # Imposta un buffer di lettura
        buffer_size = 2048
        output = ""
        end_of_output = False
        
        while not end_of_output:
            # Leggi l'output dalla console
            while channel.recv_ready():
                data = channel.recv(buffer_size)
                try:
                    data_decoded = data.decode('utf-8')
                except UnicodeDecodeError:
                    data_decoded = data.decode('utf-8', errors='ignore')
                
                output += data_decoded
            
            # Controlla se la stringa di ricerca è presente nell'output
            if search_string in output:
                start_index = output.index(search_string) + len(search_string)
                print(f"Output da {ip} a seguito della stringa '{search_string}':")
                print(output[start_index:].strip())
                end_of_output = True
            else:
                time.sleep(1)  # Attendi un secondo prima di continuare a leggere

        # Chiudi la sessione e la connessione
        channel.close()
        client.close()

    except Exception as e:
        print(f"Errore nella connessione a {ip}: {e}")

# Itera sulla lista di IP e connettiti a ciascuno
for ip in ip_list:
    ssh_connect(ip, username, password, search_string)