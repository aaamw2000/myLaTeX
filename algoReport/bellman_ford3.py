import time
import random

# Function to generate vertices and edges with a specified negative-to-positive weight ratio
def generate_graph_with_ratio(num_vertices, num_edges, negative_to_positive_ratio, weight_range=(-10, 10)):
    edges = []
    vertices = list(range(num_vertices))
    
    # Calculate the number of negative and positive weights based on the ratio
    negative_edges_count = int(num_edges * negative_to_positive_ratio / (1 + negative_to_positive_ratio))
    positive_edges_count = num_edges - negative_edges_count

    # Generate negative weight edges
    for _ in range(negative_edges_count):
        u = random.choice(vertices)
        v = random.choice(vertices)
        while v == u:  # Avoid self-loop
            v = random.choice(vertices)
        weight = random.randint(weight_range[0], -1)  # Negative weight
        edges.append((u, v, weight))

    # Generate positive weight edges
    for _ in range(positive_edges_count):
        u = random.choice(vertices)
        v = random.choice(vertices)
        while v == u:  # Avoid self-loop
            v = random.choice(vertices)
        weight = random.randint(1, weight_range[1])  # Positive weight
        edges.append((u, v, weight))
    
    return vertices, edges

# Bellman-Ford algorithm
def bellman_ford(vertices, edges, start_vertex):
    # Step 1: Initialize the distance to all vertices as infinity
    distances = {vertex: float('inf') for vertex in vertices}
    distances[start_vertex] = 0

    # Step 2: Relax edges repeatedly
    for _ in range(len(vertices) - 1):
        for u, v, weight in edges:
            if distances[u] + weight < distances[v]:
                distances[v] = distances[u] + weight

    # Step 3: Check for negative-weight cycles
    for u, v, weight in edges:
        if distances[u] + weight < distances[v]:
            raise ValueError("Graph contains a negative-weight cycle")
    
    return distances

# Function to calculate the time taken for Bellman-Ford algorithm
def calculate_time(vertices, edges, start_vertex):
    start_time = time.time()
    distances = bellman_ford(vertices, edges, start_vertex)
    end_time = time.time()
    elapsed_time = end_time - start_time
    return distances, elapsed_time

# Function to calculate the ratio of negative weights to positive weights
def calculate_negative_positive_ratio(edges):
    negative_weights = 0
    positive_weights = 0

    for u, v, weight in edges:
        if weight < 0:
            negative_weights += 1
        elif weight > 0:
            positive_weights += 1

    if positive_weights == 0:
        return float('inf')  # To handle the case where there are no positive weights
    
    ratio = negative_weights / positive_weights
    return ratio

# Function to find the number of vertices that have a path to the starting vertex
def count_reachable_vertices(vertices, edges, start_vertex):
    # Use the Bellman-Ford algorithm to get the shortest paths
    distances = bellman_ford(vertices, edges, start_vertex)

    # Count how many vertices have a finite distance (i.e., are reachable)
    reachable_count = sum(1 for distance in distances.values() if distance != float('inf'))
    
    return reachable_count

# Example usage
num_vertices = 100000
num_edges = num_vertices
negative_to_positive_ratio = 0.05 # Set the ratio of negative weights to positive weights

vertices, edges = generate_graph_with_ratio(num_vertices, num_edges, negative_to_positive_ratio)

start_vertex = 0
distances, elapsed_time = calculate_time(vertices, edges, start_vertex)

# Calculate the ratio of negative to positive weights
ratio = calculate_negative_positive_ratio(edges)

# Count the number of vertices reachable from the start vertex
reachable_count = count_reachable_vertices(vertices, edges, start_vertex)
