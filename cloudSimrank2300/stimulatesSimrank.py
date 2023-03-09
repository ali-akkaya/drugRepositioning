import pandas as pd
import csv

data = pd.read_parquet('simrankOfGraphStimulates.parquet')

print(data.head())


drugsWithCUI = pd.read_csv("seperated-condition-drugs-rating-cui.csv")
for index, row in drugsWithCUI.iterrows():
    for index2 in range(index + 1, len(drugsWithCUI)):
        if not pd.isnull(row["cui"]) and not pd.isnull(drugsWithCUI.iloc[index2]['cui']):
            try :
                simrank_score = data[row["cui"]].loc[drugsWithCUI.iloc[index2]['cui']]
                print(f'Simrank between {row["cui"]} and {drugsWithCUI.iloc[index2]["cui"]}: {simrank_score}')
                with open('stimulatesWithScoresAll.csv', 'a', newline='') as fd:
                    myCsvRow = [row["cui"], drugsWithCUI.iloc[index2]["cui"], simrank_score]
                    writer = csv.writer(fd)
                    writer.writerow(myCsvRow)
                    fd.close()
            except:
                with open('stimulatesWithScoresAll.csv', 'a', newline='') as fd:
                    myCsvRow = [row["cui"], drugsWithCUI.iloc[index2]["cui"], 'ERROR']
                    writer = csv.writer(fd)
                    writer.writerow(myCsvRow)
                    fd.close()
                print("Error in simrank calculation for ", row["cui"], " and ", drugsWithCUI.iloc[index2]["cui"])