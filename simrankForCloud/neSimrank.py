import csv

import pandas as pd
import SimRank
import pandas as pd
paths = ["treats_freq_5.csv", "stimulates_freq_5.csv",
         "prevents_freq_5.csv", "disrupts_freq_5.csv",
         "coexists-with_freq_5.csv"]
# Read the data all predicates
dataWithThreatsPredicate = pd.read_csv("treats_freq_5.csv",
                                 delimiter=';',error_bad_lines=False, encoding='unicode_escape')

print(f'Dataset Threats Shape: {dataWithThreatsPredicate.shape}')
print(dataWithThreatsPredicate.head())
data = dataWithThreatsPredicate.head(180709)
data.reset_index(inplace=True)

print(f'Unique subject_id: {len(data["subject_cui"].unique())}')
print(f'Unique object_id: {len(data["object_cui"].unique())}')

print(len(set(data["subject_cui"].unique()).intersection(set(data["object_cui"].unique()))))
sr = SimRank.SimRankPP()

s_airports = sr.fit(
    data,
    from_node_column='subject_cui',
    to_node_column = 'object_cui',
 )

#print(s_airports)
print('Simrank calculated')
s_airports.to_parquet('simrankOfGraphTreat100000.parquet', index=True)

#C0018801 C0271568
drugsWithCUI = pd.read_csv("seperated-condition-drugs-rating-with-only-one-cui.csv")
for index, row in drugsWithCUI.iterrows():
    for index2 in range(index + 1, len(drugsWithCUI)):
        if not pd.isnull(row["cui"]) and not pd.isnull(drugsWithCUI.iloc[index2]['cui']):
            try :
                simrank_score = s_airports[row["cui"]].loc[drugsWithCUI.iloc[index2]['cui']]
                print(f'Simrank between {row["cui"]} and {drugsWithCUI.iloc[index2]["cui"]}: {simrank_score}')
                with open('simrankScoresTreat100000.csv', 'a', newline='') as fd:
                    myCsvRow = [row["cui"], drugsWithCUI.iloc[index2]["cui"], simrank_score]
                    writer = csv.writer(fd)
                    writer.writerow(myCsvRow)
                    fd.close()
            except:
                with open('simrankScorestreat100000.csv', 'a', newline='') as fd:
                    myCsvRow = [row["cui"], drugsWithCUI.iloc[index2]["cui"], 'ERROR']
                    writer = csv.writer(fd)
                    writer.writerow(myCsvRow)
                    fd.close()
                print("Error in simrank calculation for ", row["cui"], " and ", drugsWithCUI.iloc[index2]["cui"])