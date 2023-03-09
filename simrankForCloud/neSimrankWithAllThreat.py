import pandas as pd
import SimRank

paths = ["treats_freq_5.csv", "stimulates_freq_5.csv",
         "prevents_freq_5.csv", "disrupts_freq_5.csv",
         "coexists-with_freq_5.csv"]
# Read the data all predicates
dataWithThreatsPredicate = pd.read_csv("treats_freq_5.csv",
                                 delimiter=';',error_bad_lines=False, encoding='unicode_escape')

print(f'Dataset Threats Shape: {dataWithThreatsPredicate.shape}')
print(dataWithThreatsPredicate.head())
dataWithThreatsPredicate.drop([dataWithThreatsPredicate.index[180710]], inplace=True)
dataWithThreatsPredicate.drop([dataWithThreatsPredicate.index[180711]], inplace=True)
dataWithThreatsPredicate.drop([dataWithThreatsPredicate.index[180712]], inplace=True)
dataWithThreatsPredicate.drop([dataWithThreatsPredicate.index[180713]], inplace=True)
dataWithThreatsPredicate.drop([dataWithThreatsPredicate.index[180714]], inplace=True)
data = dataWithThreatsPredicate.head(180710)
data.reset_index(inplace=True)


sr = SimRank.SimRankPP()

s_airports = sr.fit(
    data,
    from_node_column='subject_cui',
    to_node_column = 'object_cui',
 )

print(s_airports)
s_airports.to_parquet('simrankOfGraph.parquet', index=True)
