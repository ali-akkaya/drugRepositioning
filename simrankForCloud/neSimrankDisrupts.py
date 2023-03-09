import pandas as pd
import SimRank
import csv


# Read the data all predicates
dataWithDisruptsPredicate = pd.read_csv("disrupts_freq_5.csv",
                                 delimiter=';',error_bad_lines=False, encoding='unicode_escape')

print(f'Dataset Threats Shape: {dataWithDisruptsPredicate.shape}')

print(dataWithDisruptsPredicate.head())
data = dataWithDisruptsPredicate.head(22239)
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
s_airports.to_parquet('simrankOfGraphOfDisrupts.parquet', index=True)

#C0018801 C0271568
drugsWithCUI = pd.read_csv("seperated-condition-drugs-rating-with-only-one-cui.csv")
for index, row in drugsWithCUI.iterrows():
    for index2 in range(index + 1, len(drugsWithCUI)):
        if not pd.isnull(row["cui"]) and not pd.isnull(drugsWithCUI.iloc[index2]['cui']):
            try :
                simrank_score = s_airports[row["cui"]].loc[drugsWithCUI.iloc[index2]['cui']]
                print(f'Simrank between {row["cui"]} and {drugsWithCUI.iloc[index2]["cui"]}: {simrank_score}')
                with open('simrankScoresDisrupts.csv', 'a', newline='') as fd:
                    myCsvRow = [row["cui"], drugsWithCUI.iloc[index2]["cui"], simrank_score]
                    writer = csv.writer(fd)
                    writer.writerow(myCsvRow)
                    fd.close()
            except:
                with open('simrankScoresDisrupts.csv', 'a', newline='') as fd:
                    myCsvRow = [row["cui"], drugsWithCUI.iloc[index2]["cui"], 'ERROR']
                    writer = csv.writer(fd)
                    writer.writerow(myCsvRow)
                    fd.close()
                print("Error in simrank calculation for ", row["cui"], " and ", drugsWithCUI.iloc[index2]["cui"])