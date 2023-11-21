from concurrent import futures

import grpc
import sys

import pairs_pb2
import pairs_pb2_grpc


class CentralServer:
    def __init__(self, server):
        self.keyToServerMap = {}
        # Store server object
        self.server = server

    def Register(self, request, context):
        print("Trying to register key " + str(request.key) + " with server " + request.server_id)

        for key in request.keysList:
            count = 0
            # Register key to server address
            self.keyToServerMap[key] = request.address
            count += 1
        # Return number of keys registered to server
        return pairs_pb2.RegisterResponse(keysCount = count)

    def ServerTerminate(self, request, context):
        print("Trying to terminate server")
        count = len(self.keyToServerMap)
        # Remove all keys registered to server
        self.keyToServerMap.clear()
        # Stop server
        self.server.stop(0)
        # Return number of keys removed from server
        return pairs_pb2.ServerTerminateResponse(keysCount = count)


def serve():
    # Read port number from command line
    if (len(sys.argv) == 2):
        portNumber = sys.argv[1]
    else:
        print("Usage: python3 centralServer.py <portNumber>")
        sys.exit(1)

    # Create new gRPC server instance. It uses a thread pool executor to handle requests with a maximum of 10 threads
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    # Add a service to the server. Service is defined by CentralServer class, which implement service methods
    # Instance of CentralServer class is created here and passed to the server
    pairs_pb2_grpc.add_CentralOperationsServicer_to_server(CentralServer(server), server)

    # Listen to specified port
    server.add_insecure_port('[::]:' + portNumber)

    # Start the server. Make it run and accept incoming requests
    server.start()

    # Keep thread alive
    server.wait_for_termination()

if __name__ == '__main__':
    serve()