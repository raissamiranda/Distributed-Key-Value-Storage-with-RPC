# Run client from first part
run_cli_pares: generate_proto_files
	python3 client.py $(arg)

# Run server from first part
run_serv_pares_1: generate_proto_files
	python3 server.py $(arg)

# Run server with control flag
run_serv_pares_2: generate_proto_files
	python3 server.py $(arg) controlflag

# Run central server
run_serv_central: generate_proto_files
	python3 centralServer.py $(arg)

# Run central client
run_cli_central: generate_proto_files
	python3 centralClient.py $(arg)

# Check .proto and, if modified, regenerate before running any other rule
generate_proto_files: pairs.proto
	python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. pairs.proto

# Clean up .proto generated files
clean:
	rm -f *pb2.py *pb2_grpc.py
