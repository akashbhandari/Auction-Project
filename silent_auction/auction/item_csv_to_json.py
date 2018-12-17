import csv
import json

items={'items':[]}
with open('itemInfo.csv',encoding='utf-8',errors= 'ignore',newline='\n') as csvfile:
	reader = csv.reader(csvfile,delimiter=',')
	for line in reader:
		item = {'item_id':line[0], 'item_name':line[1],'item_amount':int(line[4]),'min_bid':int(line[6]),'bid_sheet':[]}
		items['items'].append(item)
jsonfile = open('items.json','w')
jsonfile.write(json.dumps(json.loads(json.dumps(items)), indent=4))
jsonfile.close()
