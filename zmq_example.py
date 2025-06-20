SERVER - ROUTER

import zmq

def main():
    context = zmq.Context()
    socket = context.socket(zmq.ROUTER)
    socket.bind("tcp://127.0.0.1:5555")
    print("ROUTER server started")

    while True:
        # ROUTER receives a multipart message: [identity, empty, payload]
        identity, empty, msg = socket.recv_multipart()
        print(f"Received from {identity}: {msg}")
        # Echo the message back to the client
        socket.send_multipart([identity, b'', b'ECHO: ' + msg])

if __name__ == "__main__":
    main()


# CLIENT - DEALER

import zmq
import sys
import time

def main(identity):
    context = zmq.Context()
    socket = context.socket(zmq.DEALER)
    socket.setsockopt(zmq.IDENTITY, identity.encode())
    socket.connect("tcp://127.0.0.1:5555")

    for i in range(3):
        msg = f"Hello {i} from {identity}".encode()
        print(f"Sending: {msg}")
        socket.send(msg)
        reply = socket.recv()
        print(f"Received reply: {reply}")
        time.sleep(1)

if __name__ == "__main__":
    # Pass a unique identity for each client, e.g., python zmq_dealer_client.py client1
    identity = sys.argv[1] if len(sys.argv) > 1 else "client"
    main(identity)


