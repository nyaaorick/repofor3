
# COMPX234-A3: Client-Server Tuple Space

## Project Overview

This project is the third programming assignment for the COMPX234 course. The goal is to develop a client/server networked system that implements a "Tuple Space." Clients can send requests to the server to add (PUT), read (READ), or retrieve and delete (GET) tuples. The server needs to be able to handle concurrent requests from multiple clients.

## Features

### Server (`multiserver.py`)

* **Multi-threaded Processing**: Creates an independent thread for each connected client to handle requests, supporting concurrent sessions.
* **Tuple Space Implementation**:
    * Stores key-value pairs (tuples), where both keys and values are strings.
    * Ensures key uniqueness.
    * Supports three operations: `PUT`, `GET`, `READ`.
* **Communication Protocol**:
    * Receives client requests formatted as `NNN R k`, `NNN G k`, or `NNN P k v`.
    * Sends responses formatted as `NNN OK ...` or `NNN ERR ...`.
    * `NNN` is a 3-digit number representing the total message length (maximum 999 characters).
* **Statistics Reporting**: Outputs a summary of the current tuple space and operational statistics to the server console every 10 seconds, including:
    * The current number of tuples in the tuple space.
    * Average tuple size, average key size, average value size.
    * Total number of connected clients.
    * Total number of operations, as well as separate counts for `READ`, `GET`, and `PUT` operations.
    * Total number of errors encountered.
* **Error Handling**: Capable of handling invalid requests, network issues, etc.
* **Command-Line Startup**: Specifies the listening port number 51234

### Client (`multiclient.py`)

* **Synchronous Communication**: After sending a request, waits for the server's response before sending the next request.
* **Request File Processing**:
    * Reads requests line by line from a specified text file.
    * Ignores empty lines and lines starting with `#` (comments).
    * For `PUT` operations, checks if the combined length of the "k v" part exceeds 970 characters; if so, an error is reported, and the entry is ignored.
* **Communication Protocol**:
    * Constructs messages adhering to the `NNN` protocol by taking requests from the file (e.g., `PUT key value`) as the payload to send to the server.
* **Output**:
    * For each processed request, displays the original request and the server's response on the client console.
* **Command-Line Startup**: Specifies the server hostname, server port number, and the path to a single text file containing requests via command-line arguments.

### Tuple Space (`tuple_space.py`)

* Uses a thread-safe data structure (e.g., a dictionary protected by `threading.Lock`) to store tuples.
* Implements `put(key, value)`, `get(key)`, and `read(key)` methods to handle tuple addition, deletion, and retrieval logic, ensuring atomic operations.
* Implements a `calculate_stats()` method to compute statistics related to the tuple space (tuple count, average sizes, etc.).

## Technology Stack

* **Language**: Python 3
* **Core Libraries**:
    * `socket` (for network communication)
    * `threading` (for server concurrency and client/server statistics threads)
    * `time` (for timestamps and delays in statistics reporting)

## How to Run

Run `multiserver.py`
Run `multiclient.py`

### 1. Start the Server

After the server starts, it will begin listening on the specified port and print statistics every 10 seconds.

### 2. Start the Client

After the client starts, it will send data from the `test-workload` directory.

### 3. Request File Format

The request file is a plain text file with one operation per line. Supported formats are:

* `PUT <key> <value>` (e.g., `PUT greeting Hello world`)
* `GET <key>` (e.g., `GET greeting`)
* `READ <key>` (e.g., `READ greeting`)

Where `<key>` is typically a string without spaces, and `<value>` can be a string that includes spaces.
Lines starting with `#` are treated as comments and ignored. Empty lines are also ignored.

## Project Structure

```
.
├── multiserver.py      # Main server program
├── multiclient.py      # Main client program
├── tuple_space.py      # Tuple space implementation module (to be implemented/completed by the user)
├── test-workload/      # Directory for test request files (e.g., client-1.txt, client-2.txt)
│   ├── client-1.txt
│   └── ...
└── README.md           # This file
```

## Notes and Known Limitations

* **Key Format**: The current server parsing for `PUT` commands (`message_body.split(' ', 2)`) assumes that keys do not contain spaces. If keys need to include spaces, the server-side parsing logic or the way the client sends `k v` might need adjustment.
* **Message Lengths**:
    * The client checks if the `k v` part of a `PUT` request exceeds 970 characters before sending.
    * The agreed maximum total message length for NNN protocol communication between client and server is 999 characters.
* **TupleSpace Implementation**: The thread safety and efficiency of `tuple_space.py` are crucial for the stable operation of the system. The program ensures that all access to shared tuple space data is properly locked.

## Author

20233006416 JUNYAO SHI - COMPX234 Course Assignment






