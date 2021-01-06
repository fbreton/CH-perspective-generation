#######################################################################################
#
# Description:  This script parse a CSV file to create perspectives with group based
#               on values of tags. The format of the CSV file has to be as follow:
#                   - separator : ';'
#                   - column1, header: aws tags: tag keys to use to filter AWS assets
#                                   separated by ','
#                   - column2, header: azure tags: tag keys to use to filter Azure
#                                   assets separated by ','
#                   - column3, header: key: value expected for the assets to be part
#                                   of the group
#                   - column4 to column n, header: perspective name : name of the group
#                                   on which the assets with at least one of the tag
#                                   with the value equal to the one from key column
# Author:           Fred Breton
# Creation date:    8/5/2020
# Last change:      8/5/2020 by Fred Breton
#
#######################################################################################

import csv
import requests
import json

#Name and path of the csv file to parse
reffilename = "./reffile.csv"

#token to connect to the API for the targeted tenant
token = "<your token>"

url = "https://chapi.cloudhealthtech.com/v1/perspective_schemas"
header = {'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json'}
perspectives = []
csv.register_dialect('excel',delimiter=';',quotechar = '"')

# load the file and aggregate filter constraints to group
with open(reffilename) as csv_file:
    csv_reader = csv.reader(csv_file, dialect="excel")
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            if ((row[0] != "aws tags") and (row[1] != "azure tags") and (row[2] != "key")) or (len(row) < 4):
                print("Not expected format")
                exit(1)
            line_count += 1
            # Get perspective names
            for i in range(3,len(row)):
                perspectives.append([row[i],{}])
        else:
            # Get group name for each perspective and associated search key
            for i in range(3,len(row)):
                if row[i] in perspectives[i-3][1]:
                    perspectives[i-3][1][row[i]].append([row[0].split(','),row[1].split(','),row[2]])
                else:
                    perspectives[i-3][1][row[i]] = [[row[0].split(','),row[1].split(','),row[2]]]
csv_file.close()

# generate the JSON body to create perspectives
for i in range(len(perspectives)):
    rules = []
    refidList = []
    groupid = 10445360473710
    #Loop on the list of group that will be created in the perspective
    for group in perspectives[i][1].keys():
        #loop on the key values to filter the assets on
        for k in range(len(perspectives[i][1][group])):
            key = perspectives[i][1][group][k][2]
            # loop on the tags to filter the AWS assets on for the key value
            for t in range(len(perspectives[i][1][group][k][0])):
                tag = perspectives[i][1][group][k][0][t]
                awsasset={ "type": "filter","asset": "AwsAsset","to": str(groupid),"condition": { "clauses": [ { "tag_field": [ tag ], "op": "=", "val": key } ] } }
                awstaggableasset={ "type": "filter","asset": "AwsTaggableAsset","to": str(groupid),"condition": { "clauses": [ { "tag_field": [ tag ], "op": "=", "val": key } ] } }
                rules.append(awsasset)
                rules.append(awstaggableasset)
            # loop on the tags to filter the Azure assets on for the key value
            for t in range(len(perspectives[i][1][group][k][1])):
                tag = perspectives[i][1][group][k][1][t]
                azureasset = { "type": "filter","asset": "AzureTaggableAsset","to": str(groupid),"condition": { "clauses": [ { "tag_field": [ tag ], "op": "=", "val": key } ] } }
                rules.append(azureasset)
        refidList.append({"ref_id": str(groupid),"name":  group})
        groupid += 1
    body = {"schema": {"name": perspectives[i][0],"include_in_reports": "true","rules": rules,"merges":[],"constants": [{"type": "Static Group","list": refidList }]}}

    # call the REST API and provide feedback
    response = requests.post(url, json=body, headers=header)
    print("-------- Perspective: "+perspectives[i][0]+" --------")
    print(response)
    print(response.json())
