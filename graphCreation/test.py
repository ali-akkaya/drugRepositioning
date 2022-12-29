import networkx as nx

# Create a Graph object
G = nx.Graph()

# Add a node to the graph
G.add_node(1)

# Add a node with attributes to the graph
G.add_node(2, qui = '2')

# Access the attributes of the node
 # Output: "red"
print(G.nodes[2]['qui'])  # Output: 10
