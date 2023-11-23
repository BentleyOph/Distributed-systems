import multiprocessing
import random
import time

def gossip(node_id, shared_data, neighbors, lock):
    # Simulate gossip-based data dissemination
    time.sleep(1)  # Simulating some computation/update

    # Choose a random neighbor
    random_neighbor = random.choice(neighbors)

    with lock:
        received_data = shared_data[random_neighbor]

    # Update local data based on received data
    updated_data = max(shared_data[node_id], received_data)

    with lock:
        shared_data[node_id] = updated_data

    print(f"Node {node_id} updated data: {updated_data} (Received from Node {random_neighbor})")

def simulate_system(node_id, shared_data, connections, lock):
    neighbors = connections[node_id]
    
    for _ in range(3):  # Simulate 3 rounds of gossip
        gossip(node_id, shared_data, neighbors, lock)
        time.sleep(1)  # Simulate some time passing between rounds

if __name__ == "__main__":
    num_nodes = 5

    # Define shared data using multiprocessing.Manager().dict() for shared memory
    shared_data = multiprocessing.Manager().dict({i: 0 for i in range(num_nodes)})
    shared_data[0] = 2  # Initialize Node 1 with the number 2

    lock = multiprocessing.Lock()

    # Define connections between nodes
    connections = {
        0: [1, 2],
        1: [0, 2, 3],
        2: [0, 1, 4],
        3: [1, 4],
        4: [2, 3]
    }

    processes = []

    for i in range(num_nodes):
        process = multiprocessing.Process(target=simulate_system, args=(i, shared_data, connections, lock))
        processes.append(process)

    for process in processes:
        process.start()

    for process in processes:
        process.join()

    # Print the final state of each node
    for i in range(num_nodes):
        print(f"Node {i} final data: {shared_data[i]}")
