# Distributed key-value storage with RPC

## About the project
This project develop an application based on Remote Procedure Calls (RPC). In the field of cloud application development, RPCs are arguably the most commonly used technique for communication between componentes of a network service.
Here, we will use gRPC to develop a simple key-value storage service emplying two types of servers to construct a more sophisticated service.
Consequently, the implementation can be divided into two parts: the key registration service and the actual query service.

## First: client/server pair
This pair communicates via gRPC to establish a key-value storage service.
When the client connects with the server, it has the following commands to execute:

### Insertion
Takes positive integers (key) and a string (value) and stores in server dictionary.

Usage format:
```
I,key,string
```

Examples:
```
I,0,raissa
I,1,maciel
I,2,likes
I,3,grpc
```

It will return 0 when the pair is correctly stored and -1 if it already exists.

### Query
Takes a positive integer (key) and returns the content of the string. If it doesn't exist, nothing is done.

Usage format:
```
C,key
```

Example
```
C,2
```

### Activation:
Takes a string identifier and send all pairs stored in its dictionary to central server.
It returns the number of pairs registered.

Usage format:
```
A,host:portnumber
```

Example
```
A,localhost:51511
```

### Termination:
It indicates the server should terminate its execution

Usage format:
```
T
```


## Second: Centralized Server
It's central server/client pair. Internally, it associates keys with the addresses of servers (from first section) that announced them.
The client has theses commands to execute:

### Termination:
It terminates the server, similar to the first part.

Usage format:
```
T
```

### Query
Central client submits the desired key for value retrieval. Central server responds with the address of the server that holds the corresponding key, prompting the client to establish a connection to this address.
Then, the client can search for the specified key.

Usage format:
```
C,key
```


## Instructions for execution
To install the program, it is necessary to navigate to the directory where the program is stored:
'''
cd <destinationDirectory>
'''

To initiate server and clients, the following scripts are useful:
```
make run_cli_pairs arg=hostname_of_pairs_server:5555      ->     launches the client for the first part
make run_serv_pairs_1 arg=5555                            ->     triggers the server for the first part without the ability to connect to the central server
make run_serv_pairs_2 arg=5555                            ->     launches the server for the first part enabling connection with the central server
make run_central_server arg=6666                          ->     initiates the central server
make run_cli_central arg=hostname_of_central_server:6666  ->     starts the central client
```

### Important notes
* Servers must be connected to different ports
* The client for the first part should specify the address of the central server when using the activation command.
* Each previously mentioned script should be executed in a separate terminal
* The port numbers were provided for illustrative purposes, and they can be modified as needed


## Example of execution
Start the server for the first part with activation for the central server and connect the client to it. 
Start the central server and connect the central client to it.

In the first part's client:
```
I,0,raissa
I,1,maciel
I,2,likes
I,3,grpc
I,2,somuch
C,3
A,localhost:6666
T
```

The outputs should be:
```
0
0
0
0
-1
grpc
4
```

In the central client:
```
C,0
T
```

The output should be:
```
raissa
```
