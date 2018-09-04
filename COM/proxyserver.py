import time
import zmq


def main():

    print("Running polling tests for REQ/REP sockets...")

    addr = 'tcp://127.0.0.1:5555'
    ctx = zmq.Context()
    s1 = ctx.socket(zmq.REP)
    
    s1.bind(addr)
    print("Started server")

    while True:
        message = socket.recv_json()
    
        print("Received request: " + message['operacion'])
        if message['operacion']=='suma':
            print 'Suma'
            res=message['arg1']+message['arg2']
            socket.send_json({'resultado':res})

    #  Do some 'work'
    time.sleep(1)


    # Sleep to allow sockets to connect.
    time.sleep(1.0)

    poller.register(s2, zmq.POLLIN|zmq.POLLOUT)

if __name__=='__main__':
    main():


