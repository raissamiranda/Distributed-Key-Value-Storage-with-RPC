from concurrent import futures

import grpc
import sys
import socket

import pairs_pb2
import pairs_pb2_grpc


# Server will receive requests from client
# Request has the structure defined in pairs.proto
class Pair:
    def __init__(self, server):
        self.pair = {}
        self.server = server

    def Insert(self, request, context):
        if request.key in self.pair:
            return pairs_pb2.InsertResponse(result=-1)
        else:
            self.pair[request.key] = request.value
            return pairs_pb2.InsertResponse(result=0)

    def Search(self, request, context):
        if request.key in self.pair:
            return pairs_pb2.SearchResponse(value=self.pair[request.key])
        else:
            return pairs_pb2.SearchResponse(value = "")

    def Activate(self, request, context):
        # If there is control flag, then connect to central server
        if len(sys.argv) == 3:
            # Create gRPC channel to central server
            channel = grpc.insecure_channel(request.id)
            # Create stub to call RPC methods on central server
            stub = pairs_pb2_grpc.CentralOperationsStub(channel)
            # Call Register method on the stub and send a Register request to central server
            port = sys.argv[1]
            response = stub.Register(pairs_pb2.RegisterRequest(address=f"{socket.getfqdn()}:{port}", keysList=self.pair.keys()))
            return pairs_pb2.ActivateResponse(count=response.keysCount)
        return pairs_pb2.ActivateResponse(count=0)

    def Terminate(self, request, context):
        # Remove all keys registered to server
        self.pair.clear()
        # Stop server
        self.server.stop(0)
        return pairs_pb2.TerminateResponse(result=0)

def serve():
    # Read port number and control flag from command line
    if (len(sys.argv) > 3 or len(sys.argv) < 1):
        print("Usage: python3 server.py <portNumber> [controlFlag]")
        sys.exit(1)

    if (len(sys.argv) == 2):
        portNumber = sys.argv[1]

    if (len(sys.argv) == 3):
        portNumber = sys.argv[1]
        controlFlag = sys.argv[2]

    # Create new gRPC server instance. It uses a thread pool executor to handle requests with a maximum of 10 threads
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    # Add a service to the server. Service is defined by Pair class, which implement service methods
    # Instance of Pair class is created here and passed to the server
    pairs_pb2_grpc.add_OperationsServicer_to_server(Pair(server), server)

    # Listen to pecified port
    server.add_insecure_port('[::]:' + portNumber)

    # Start the server. Make it run and accept incoming requests
    server.start()

    # Keep thread alive
    server.wait_for_termination()

def getMyIP():
    socket.gethostbyname(socket.gethostname())

if __name__ == '__main__':
    serve()
