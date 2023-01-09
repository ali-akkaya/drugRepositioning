# This script returns UMLS CUIs based on an input file of strings, where each line in txt file is a separate string.
# If no results are found for a specific string, this will be noted in output and output file.
# Each set of results for a string is separated in the output file with '***'.

import requests
import argparse
import pandas as pd

parser = argparse.ArgumentParser(description='process user given parameters')
parser.add_argument('-k', '--apikey', required=True, dest='apikey', help='enter api key from your UTS Profile')
parser.add_argument('-v', '--version', required=False, dest='version', default='current',
                    help='enter version example-2015AA')
parser.add_argument('-o', '--outputfile', required=True, dest='outputfile', help='enter a name for your output file')
parser.add_argument('-s', '--sabs', required=False, dest='sabs',
                    help='enter a comma-separated list of vocabularies without spaces, like MSH,SNOMEDCT_US,RXNORM')
parser.add_argument('-t', '--ttys', required=False, dest='ttys',
                    help='enter a comma-separated list of term types, like PT,SY,IN')
parser.add_argument('-i', '--inputfile', required=True, dest='inputfile', help='enter a name for your input file')

args = parser.parse_args()
apikey = args.apikey
version = args.version
outputcsv = args.outputfile
inputcsv = args.inputfile
sabs = args.sabs
ttys = args.ttys

base_uri = 'https://uts-ws.nlm.nih.gov'

data = pd.read_csv(inputcsv, encoding='utf-8')
data = data.assign(CUI1=[None] * len(data))
data = data.assign(CUI2=[None] * len(data))
data = data.assign(CUI3=[None] * len(data))
with open(outputcsv, 'w', encoding='utf-8') as o:
    for index, row in data.iterrows():
        drugName = row['drugName']
        page = 1
        path = '/search/' + version
        query = {'string': drugName, 'apiKey': apikey, 'rootSource': sabs, 'termType': ttys, 'pageNumber': page}
        output = requests.get(base_uri + path, params=query)
        output.encoding = 'utf-8'

        outputJson = output.json()
        results = (([outputJson['result']])[0])['results']
        if len(results) == 0:
            if page == 1:
                print('No results found for ' + drugName + '\n')
                o.write('No results found.' + '\n' + '\n')
                break
            else:
                break

        for i, item in enumerate(results[:3]):
            o.write('UI: ' + item['ui'] + '\n' + 'Name: ' + item['name'] + '\n' + 'URI: ' + item[
                'uri'] + '\n' + 'Source Vocabulary: ' + item['rootSource'] + '\n' + '\n')
            data.at[index, 'CUI'+str(i+1)] = item['ui']

        o.write('***' + '\n' + '\n')

data.to_csv("condition-drugs-rating-cuis.csv", index=False)
