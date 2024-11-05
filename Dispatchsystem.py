import tkinter as tk
from tkinter import messagebox
import heapq
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Graph definition
graph = {
    'A': {'B': 4, 'C': 2}, 'B': {'A': 4, 'C': 1, 'D': 5},
    'C': {'A': 2, 'B': 1, 'D': 8, 'E': 10}, 'D': {'B': 5, 'C': 8, 'E': 2, 'F': 6},
    'E': {'C': 10, 'D': 2, 'F': 3}, 'F': {'D': 6, 'E': 3}
}

# Dijkstra's algorithm for shortest path
def dijkstra(graph, start, end):
    queue, distances, path = [(0, start)], {node: float('inf') for node in graph}, {}
    distances[start] = 0

    while queue:
        cost, current = heapq.heappop(queue)
        if current == end:
            route = []
            while current in path:
                route.append(current)
                current = path[current]
            return cost, [start] + route[::-1]

        for neighbor, weight in graph[current].items():
            distance = cost + weight
            if distance < distances[neighbor]:
                distances[neighbor], path[neighbor] = distance, current
                heapq.heappush(queue, (distance, neighbor))

    return float("inf"), []

# Display shortest path and visualize graph
def find_shortest_path():
    start, end = start_entry.get().upper(), end_entry.get().upper()
    if start not in graph or end not in graph:
        messagebox.showerror("Error", "Invalid nodes! Enter valid locations.")
        return
    distance, path = dijkstra(graph, start, end)
    result_label.config(text=(f"Shortest path: {' -> '.join(path)} (Distance: {distance})"
                              if distance != float("inf") else "No path found."))
    draw_graph(path)

# Graph visualization with Matplotlib
def draw_graph(path):
    G = nx.Graph()
    for node, edges in graph.items():
        G.add_edges_from((node, neighbor, {'weight': weight}) for neighbor, weight in edges.items())
    pos = nx.spring_layout(G)

    plt.clf()
    fig, ax = plt.subplots()
    nx.draw(G, pos, with_labels=True, node_size=500, node_color='lightblue', ax=ax)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=nx.get_edge_attributes(G, 'weight'), font_size=8)
    nx.draw_networkx_edges(G, pos, edgelist=[(path[i], path[i+1]) for i in range(len(path) - 1)], 
                           edge_color='red', width=2, ax=ax)

    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.draw()
    canvas.get_tk_widget().pack()

# Tkinter GUI setup
window = tk.Tk()
window.title("Emergency Response Dispatch System")

tk.Label(window, text="Enter Start and End Locations:").pack()
tk.Label(window, text="Start Location (A-F):").pack()
start_entry = tk.Entry(window)
start_entry.pack()
tk.Label(window, text="End Location (A-F):").pack()
end_entry = tk.Entry(window)
end_entry.pack()
tk.Button(window, text="Find Shortest Path", command=find_shortest_path).pack()
result_label = tk.Label(window, text="")
result_label.pack()

window.mainloop()
