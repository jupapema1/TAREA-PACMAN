import zmq
import sys

DIRECCION='localhost'
PUERTO='6666'


def main():

	try:
		context=zmq.Context()
		server=context.socket(zmq.REQ)
		print('Conectando con servidor1 en el puerto '+PUERTO)
		server.connect('tcp://'+DIRECCION+':'+PUERTO)
		print('Enviando mensaje...')
		server.send_json({'operacion':'hola'})
		resp=server.recv_json()
		print('Respuesta del servidor : '+resp['res'])

	except ValueError:
		print ("\nError al conectar el servidor!!")

if __name__=='__main__':
	main()