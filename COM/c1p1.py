import time 
import zmq

def main():

	print("Running polling tests for REQ/REP sockets...")

	addr = 'tcp://127.0.0.1:5555'
	ctx = zmq.Context()
	s2 = ctx.socket(zmq.REQ)

	s2.connect(addr)


	# Sleep to allow sockets to connect.
	print('Sleep to allow sockets to connect.')
	time.sleep(1.0)


	poller = zmq.Poller()
	poller.register(s1, zmq.POLLIN|zmq.POLLOUT)

	# Make sure that s1 is in state 0 and s2 is in POLLOUT
	socks = dict(poller.poll())
	assert not socks.has_key(s1)
	assert socks[s2] == zmq.POLLOUT

if __name__=='__main__':
	main()











