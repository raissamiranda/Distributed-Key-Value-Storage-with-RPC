from concurrent import futures

import grpc
import sys

import pairs_pb2
import pairs_pb2_grpc


# Server will receive requests from client
# Request has the structure defined in pairs.proto
class Pair:
    def __init__(self):
        self.pair = {}

    def Insert(self, request, context):
        print("Trying to insert key " + str(request.key) + " with value " + request.value)

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
        # TO DO
        return grpc.Empty()

    def Terminate(self, request, context):
        # TO DO
        return pairs_pb2.TerminateResponse(result=0)

def serve():
    # Create dictionary to store key-value pairs
    pair = Pair()

    # Read port number and control flag from command line
    if (len(sys.argv) > 3 or len(sys.argv) < 1):
        print("Usage: python3 server.py <portNumber> [controlFlag]")
        sys.exit(1)

    if (len(sys.argv) == 3):
        portNumber = sys.argv[1]
        controlFlag = sys.argv[2]

    if (len(sys.argv) == 1):
        portNumber = sys.argv[1]
        controlFlag = 0

    print("Server is running on port " + portNumber + " with control flag " + controlFlag)

    # Create new gRPC server instance. It uses a thread pool executor to handle requests with a maximum of 10 threads
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    # Add a service to the server. Service is defined by Pair class, which implement service methods
    pairs_pb2_grpc.add_OperationsServicer_to_server(Pair(), server)

    # Listen to port specified
    server.add_insecure_port('[::]:' + portNumber)

    # Start the server. Make it run and accept incoming requests
    server.start()

    # Keep thread alive
    server.wait_for_termination()

if __name__ == '__main__':
    serve()

