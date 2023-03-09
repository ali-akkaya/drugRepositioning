import pandas as pd
import networkx as nx
from tqdm import tqdm
import timeit
import csv

paths = ["treats_freq_5.csv", "stimulates_freq_5.csv",
         "prevents_freq_5.csv", "disrupts_freq_5.csv",
         "coexists-with_freq_5.csv"]
# Read the data all predicates
dataWithThreatsPredicate = pd.read_csv("treats_freq_5.csv",
                                       delimiter=';', error_bad_lines=False, encoding='unicode_escape')
dataWithStimulatesPredicate = pd.read_csv("stimulates_freq_5.csv",
                                          delimiter=';', error_bad_lines=False, encoding='unicode_escape')
dataWithPreventsPredicate = pd.read_csv("prevents_freq_5.csv",
                                        delimiter=';', error_bad_lines=False, encoding='unicode_escape')
dataWithDisruptsPredicate = pd.read_csv("disrupts_freq_5.csv",
                                        delimiter=';', error_bad_lines=False, encoding='unicode_escape')
dataWithCoexistsWithPredicate = pd.read_csv("coexists-with_freq_5.csv",
                                            delimiter=';', error_bad_lines=False, encoding='unicode_escape')


# Find skipped Rows

def find_skipped_rows(filePath):
    skipped_rows = 0
    with open(filePath, "r", encoding='unicode_escape') as f:
        for i, line in enumerate(f):
            try:
                # Try to parse the row as a list of values
                values = line.split(";")
                # Validate the number of values
                if len(values) != 6:
                    raise ValueError("Wrong number of fields")
                # If no errors are raised, the row is valid
            except ValueError:
                # If an error is raised, the row is invalid
                skipped_rows += 1
        f.close()

    print(f"Skipped {skipped_rows} rows due to errors")


for path in paths:
    find_skipped_rows(path)

# Print Dataset shapes
print(f'Dataset Threats Shape: {dataWithThreatsPredicate.shape}')
print(f'Dataset Stimulates Shape: {dataWithStimulatesPredicate.shape}')
print(f'Dataset Prevents Shape: {dataWithPreventsPredicate.shape}')
print(f'Dataset Disrupts Shape: {dataWithDisruptsPredicate.shape}')
print(f'Dataset Coexist-With Shape: {dataWithCoexistsWithPredicate.shape}')

# Create Graph
print(f'Creation of dataset started ...')
t_0 = timeit.default_timer()
G = nx.DiGraph()

for index, row in tqdm(dataWithThreatsPredicate.iterrows(), desc="Threats", total=dataWithThreatsPredicate.shape[0]):
    G.add_edge(row['subject_cui'], row['object_cui'], label=row['predicate'], weight=row['frequency'])

print('All rows of Threats predicate added to the graph')

for index, row in tqdm(dataWithStimulatesPredicate.iterrows(), desc="Stimulates",
                       total=dataWithStimulatesPredicate.shape[0]):
    G.add_edge(row['subject_cui'], row['object_cui'], label=row['predicate'], weight=row['frequency'])

print('All rows of Stimulates predicate added to the graph')

for index, row in tqdm(dataWithPreventsPredicate.iterrows(), desc="Prevents", total=dataWithPreventsPredicate.shape[0]):
    G.add_edge(row['subject_cui'], row['object_cui'], label=row['predicate'], weight=row['frequency'])

print('All rows of Prevents predicate added to the graph')

for index, row in tqdm(dataWithDisruptsPredicate.iterrows(), desc="Disrupts", total=dataWithDisruptsPredicate.shape[0]):
    G.add_edge(row['subject_cui'], row['object_cui'], label=row['predicate'], weight=row['frequency'])

print('All rows of Disrupts predicate added to the graph')

for index, row in tqdm(dataWithCoexistsWithPredicate.iterrows(), desc="Coexists-With",
                       total=dataWithCoexistsWithPredicate.shape[0]):
    G.add_edge(row['subject_cui'], row['object_cui'], label=row['predicate'], weight=row['frequency'])

print('All rows of Coexists-With predicate added to the graph')

t_1 = timeit.default_timer()
elapsed_time = round((t_1 - t_0) * 10 ** 6, 3)
print(f'Creation of dataset finished in {t_1 - t_0} seconds')
print(f"Elapsed time to create dataset: {elapsed_time} µs")

print(f'Total number of nodes: {len(G.nodes)}')
print(f'Total number of edges: {len(G.edges)}')
print(f'.\n.\n.\n')

# Read CUI from file

print(f'CUIs read from file')
drugsWithCUI = pd.read_csv("seperated-condition-drugs-rating-with-only-one-cui.csv")
drugsWithCUI = drugsWithCUI.head(5).reset_index(drop=True)
print(f'Shape of drugs and cui data: {drugsWithCUI.shape}')

print(G.nodes.__contains__(drugsWithCUI.iloc[0]['cui']))
print(G.nodes.__contains__(drugsWithCUI.iloc[1]['cui']))

exit()

# Find Simrank Similarity
print(f'Find SimRank started...')
t_0 = timeit.default_timer()
for index, row in tqdm(drugsWithCUI.iterrows(), desc="SimRank Source", total=drugsWithCUI.shape[0]):
    for index2 in tqdm(range(index + 1, len(drugsWithCUI)), desc="SimRank Target",
                       total=drugsWithCUI.shape[0] - index - 1):
        if not pd.isnull(row["cui"]) and not pd.isnull(drugsWithCUI.iloc[index2]['cui']):

            if G.nodes.__contains__(row["cui"]) and G.nodes.__contains__(drugsWithCUI.iloc[index2]['cui']):
                print(f'{index} - {index2}')
                print(f'{row["cui"]} - {drugsWithCUI.iloc[index2]["cui"]}')
                simrank_score = nx.simrank_similarity(G, row["cui"], drugsWithCUI.iloc[index2]["cui"],
                                                      max_iterations=100, tolerance=0.0001)
                print(f'Simrank between {row["cui"]} and {drugsWithCUI.iloc[index2]["cui"]}: {simrank_score}')
                with open('document.csv', 'a', newline='') as fd:
                    myCsvRow = [row["cui"], drugsWithCUI.iloc[index2]["cui"], simrank_score]
                    writer = csv.writer(fd)
                    writer.writerow(myCsvRow)
                    fd.close()

t_1 = timeit.default_timer()
elapsed_time = round((t_1 - t_0) * 10 ** 6, 3)
print(f'Creation of dataset finished in {t_1 - t_0} seconds')
print(f"Elapsed time to create dataset: {elapsed_time} µs")
d
