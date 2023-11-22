import grpc
import pairs_pb2
import pairs_pb2_grpc
import sys

def run():

    if len(sys.argv) == 2:
        serviceIdentifier = sys.argv[1]
    else:
        # Default server address
        serviceIdentifier = 'localhost:50051'

    # Creates a channel to the provide server address
    channel = grpc.insecure_channel(serviceIdentifier)

    # Creates a client stub to call RPC methods on the server
    # When calling methods on the stub, it sends an RPC request to the server over the channel
    # CentralOperationsStub is generated by Protocol Buffers compiler from pairs.proto
    stub = pairs_pb2_grpc.CentralOperationsStub(channel)

    try:
        while(True):
            command = input()

            #Terminate request
            if command == 'T':
                # Call Terminate method on the stub and send a Terminate request to server
                response = stub.ServerTerminate(pairs_pb2.TerminateRequest())
                print(response.keysCount)
                break

            if command.startswith('C,'):
                _, key = command.split(',', 1)
                # Call Search method on the stub and send a Search request to server
                response = stub.Map(pairs_pb2.MapRequest(key=int(key)))
                print(response.address + ':')

    except EOFError:
        sys.exit(0)

if __name__ == '__main__':
    run()