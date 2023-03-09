import pandas as pd


data = pd.read_parquet('simrankOfGraphOfAugments.parquet')
print(data.head())

searchMatrix = pd.read_csv("searchMatrix.csv", index_col=0)
print('Search Matrix shape: ', searchMatrix.shape)
print(searchMatrix.head())

for i in range(len(searchMatrix.keys())):
    for j in range(len(searchMatrix.keys())):
        try:
            simrank_score = data[searchMatrix.index[i].split('_')[2]].loc[searchMatrix.columns[j].split('_')[2]]
            searchMatrix.iloc[i,j] = simrank_score
            print(f'Simrank between {searchMatrix.index[i].split("_")[2]} and {searchMatrix.columns[j].split("_")[2]}: {simrank_score}')
        except:
            searchMatrix.iloc[i,j] = 'ERR'
            print("Error in simrank calculation for ", searchMatrix.index[i].split("_")[2], " and ", searchMatrix.columns[j].split("_")[2])

searchMatrix.to_csv('searchMatrixAugmentsScores.csv')