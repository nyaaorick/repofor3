# file: multiclient.py
# -*- coding: utf-8 -*-
import threading
import socket


def send_nnn_message(sock, payload_str, client_id_for_log="?"):

    try:
        payload_bytes = payload_str.encode('utf-8')
        total_len = len(payload_bytes) + 3
        if not (0 <= total_len <= 999):
            print(
                f"[Client-{client_id_for_log}] Error: Message length {total_len} is out of allowed range (e.g., 7-999). Payload: '{payload_str[:30]}...'")
            return False

        header = f"{total_len:03d}"
        full_message = header.encode('utf-8') + payload_bytes
        sock.sendall(full_message)
        return True

    except Exception as e:
        print(f"[Client-{client_id_for_log}] Exception in send_nnn_message: {e}")
        return False


 # Send a message to the server
def receive_nnn_message(sock, client_id_for_log="?"):  # 保持 client_id_for_log

    message_body = None
    try:
        header_bytes = sock.recv(3)
        if not header_bytes or len(header_bytes) < 3:
            print(f"[Client-{client_id_for_log}] Error: Failed to receive complete header.")
            return None  # header err
        try:
            msg_len_str = header_bytes.decode('utf-8')
            total_msg_len = int(msg_len_str)
            if not (3 < total_msg_len <= 999):
                print(
                    f"[Client-{client_id_for_log}] Error: Received message length {total_msg_len} from header is out of allowed range (e.g., >3 and <=999).")
                raise ValueError(f"Invalid message length from header: {total_msg_len}")

        except (ValueError, UnicodeDecodeError) as e:
            print(f"[Client-{client_id_for_log}] Exception decoding header or invalid length: {e}")
            return None

        bytes_to_read = total_msg_len - 3

        if bytes_to_read < 0:
            print(f"[Client-{client_id_for_log}] Error: Calculated bytes_to_read ({bytes_to_read}) is negative.")
            return None

        body_bytes_list = []
        bytes_read = 0
        while bytes_read < bytes_to_read:
            chunk = sock.recv(min(bytes_to_read - bytes_read, 4096))

            if not chunk:
                print(f"[Client-{client_id_for_log}] Error: Socket connection broken while reading message body.")
                return None
            body_bytes_list.append(chunk)
            bytes_read += len(chunk)
        message_body = b"".join(body_bytes_list).decode('utf-8')


    except socket.timeout:
        print(f"[Client-{client_id_for_log}] Socket timeout during receive_nnn_message.")
        return None
    except Exception as e:
        print(f"[Client-{client_id_for_log}] Exception in receive_nnn_message: {e}")
        return None

    return message_body

# This function will be run by each client thread
def client_task(client_id, server_host, server_port, request_filename):
    thread_name = f"Client-{client_id}({request_filename})"  # 使用 client_id 构造 thread_name
    print(f"[{thread_name}] ,this thread started...")

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.settimeout(30.0)

    try:
        client_socket.connect((server_host, server_port))
        print(f"[{thread_name}] success.")
    except Exception as e:
        print(f"[{thread_name}] fail: {e}")
        return

    line_num = 0
    processed_count = 0
    error_count = 0

    try:
        with open(request_filename, 'r', encoding='utf-8') as f:
            for line in f:
                line_num += 1
                original_request_line = line.strip()

                if not original_request_line or original_request_line.startswith('#'):
                    continue
                # check length of k v
                parts = original_request_line.split(maxsplit=1)
                command = ""
                if len(parts) > 0:
                    command = parts[0].upper()

                if command == "PUT":
                    if len(parts) > 1:
                        kv_part = parts[1]
                        if len(kv_part) > 970:
                            print(
                                f"[{thread_name}] Line {line_num}: Error - Request '{original_request_line[:50]}...' (k/v part) exceeds 970 characters. Ignoring.")
                            error_count += 1
                            continue
                    else:
                        print(
                            f"[{thread_name}] Line {line_num}: Error - PUT command '{original_request_line}' is missing key/value part. Ignoring.")
                        error_count += 1
                        continue
                if not send_nnn_message(client_socket, original_request_line, str(client_id)):
                    error_count += 1
                    print(
                        f"[{thread_name}] Line {line_num}: Error sending message for '{original_request_line[:50]}...'. Ending session.")
                    break

                response_body = receive_nnn_message(client_socket, str(client_id))

                if response_body is None:
                    error_count += 1
                    print(
                        f"[{thread_name}] Line {line_num}: Error receiving response for '{original_request_line[:50]}...'. Ending session.")
                    break

                print(f"[{thread_name}] {original_request_line}: {response_body}")
                processed_count += 1

                if processed_count > 0 and processed_count % 1000 == 0:  # 确保 processed_count > 0
                    print(f"[{thread_name}] managed to handle {processed_count} times of request ...")

    except FileNotFoundError:
        print(f"[{thread_name}] Error: Request file '{request_filename}' not found.")
        error_count += 1
    except Exception as e:
        print(f"[{thread_name} err] during file processing or communication: {e}")
        error_count += 1
    finally:
        print(
            f"[{thread_name}] finished !  it handle {processed_count}  request,  and it find {error_count}  err  now ")
        client_socket.close()


if __name__ == "__main__":
    server_host = 'localhost'
    server_port = 51234

    filenames = [
        'test-workload/client_1.txt',
        'test-workload/client_2.txt',
        'test-workload/client_3.txt',
        'test-workload/client_4.txt',
        'test-workload/client_5.txt',
        'test-workload/client_6.txt',
        'test-workload/client_7.txt',
        'test-workload/client_8.txt',
        'test-workload/client_9.txt',
        'test-workload/client_10.txt'
    ]

    threads = []
    for i, filename in enumerate(filenames):
        client_id = i + 1
        thread = threading.Thread(target=client_task, args=(client_id, server_host, server_port, filename))
        threads.append(thread)
        thread.start()
        print(f"thread Client-{client_id} ({filename}) successfully started.")

    for thread in threads:
        thread.join()

    print("all clients have finished sending messages.")