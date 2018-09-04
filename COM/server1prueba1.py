import sys
import zmq

def main():
    print("\nIniciando servidor1...")
    context=zmq.Context()
    servers=context.socket(zmq.REP)
    servers.bind("tcp://*:5555")

    clients=context.socket(zmq.REP)
    clients.bind("tcp://*:6666")

    poller=zmq.Poller()
    poller.register(servers,zmq.POLLIN)
    poller.register(clients,zmq.POLLIN)
    print("Servidor1 iniciado...\n")

    while True:
        print("\nEsperando peticiones...")
        socks=dict(poller.poll())

        if clients in socks:

            print("Mensaje de un cliente...")
            respuesta=clients.recv_json()
            print('Operacion: '+respuesta['operacion'])

            if respuesta['operacion'] == 'hola':
                resp={'res':'Mundo'}
                clients.send_json(resp)

            else:
                print("Operacion no soportada.")


if __name__=='__main__':
    main()