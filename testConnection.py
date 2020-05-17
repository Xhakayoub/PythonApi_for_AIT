import socket
import time

def test_connection():
    try: 
        socket.create_connection(('Google.com', 80))
        time.sleep(5)
        return True
    except OSError:
        return False


print(test_connection())