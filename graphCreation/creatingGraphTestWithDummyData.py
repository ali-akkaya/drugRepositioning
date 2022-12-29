import networkx as nx
import matplotlib.pyplot as plt

# Creaate tuple list for test data that contains subject_name, subject_qui, predicate, object_name, object_qui
dummy_data = [
    ('A', 'A', '1', 'B', 'B'),
    ('A', 'A', '1', 'C', 'C'),
    ('C', 'C', '1', 'D', 'D'),
    ('D', 'D', '1', 'A', 'A'),
    ('E', 'E', '1', 'F', 'F'),
    ('C', 'C', '3', 'E', 'E'),
    ('G', 'G', '3', 'H', 'H'),
    ('G', 'G', '3', 'H', 'H'),
]

# Create a Graph object
G = nx.DiGraph()

# Create a dictionary to store the nodes that have been added to the graph
nodes = {}

# Process the results and add nodes and edges to the graph
for row in dummy_data:
    subject_name = row[0]
    subject_qui = row[1]
    predicate = row[2]
    object_name = row[3]
    object_qui = row[4]

    # Check if a node with the same name and qui already exists in the dictionary
    if (subject_name, subject_qui) in nodes:
        # Use the existing node
        subject_node = nodes[(subject_name, subject_qui)]
    else:
        # Add the subject as a new node to the graph
        subject_node = G.add_node(subject_qui, name=subject_name)
        # Store the node in the dictionary
        nodes[(subject_name, subject_qui)] = subject_node

    # Repeat the process for the object
    if (object_name, object_qui) in nodes:
        object_node = nodes[(object_name, object_qui)]
    else:
        object_node = G.add_node(object_qui, name=object_name)
        nodes[(object_name, object_qui)] = object_node

    # Add an edge between the subject and object, using the predicate as the edge weight
    G.add_edge(subject_qui, object_qui, weight=predicate)

# Visualize the graph using matplotlib
nx.draw(G, with_labels=True)
plt.show()
print(G.nodes)
print(nodes)
print(G.edges)