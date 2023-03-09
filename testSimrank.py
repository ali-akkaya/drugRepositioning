import pandas as pd

data = pd.read_parquet('simrankOfGraph.parquet')
print(data.shape)
print(data.head())


drugsWithCUI = pd.read_csv("seperated-condition-drugs-rating-cui.csv")
for index, row in drugsWithCUI.iterrows():
    for index2 in range(index + 1, len(drugsWithCUI)):
        if not pd.isnull(row["cui"]) and not pd.isnull(drugsWithCUI.iloc[index2]['cui']):
            try :
                simrank_score = data[row["cui"]].loc[drugsWithCUI.iloc[index2]['cui']]
                print(f'Simrank between {row["cui"]} and {drugsWithCUI.iloc[index2]["cui"]}: {simrank_score}')
            except:
                print("Error in simrank calculation for ", row["cui"], " and ", drugsWithCUI.iloc[index2]["cui"])