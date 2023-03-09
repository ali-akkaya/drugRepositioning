import pandas as pd
import networkx as nx

data = pd.read_csv("test_data.csv", delimiter=';', error_bad_lines=False, encoding='unicode_escape')

G = nx.DiGraph()

for index, row in data.iterrows():
    G.add_edge(row['subject_cui'], row['object_cui'], label=row['predicate'], weight=row['frequency'])

nodes = ['C0087111', 'C0042196', 'C0027540', 'C0940933', 'C0003881', 'C0038039', 'C0021655']

for i, node in enumerate(nodes):
    for j, node2 in enumerate(nodes):
        simrank_score = nx.simrank_similarity(G, node, node2,
                                              max_iterations=100, tolerance=0.0001)
        print(f'Simrank between {node} and {node2}: {simrank_score}')