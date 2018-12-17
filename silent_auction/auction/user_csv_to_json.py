import csv
import json

users={'users':[]}
with open('userInfo.csv',encoding='utf-8',errors= 'ignore',newline='\n') as csvfile:
	reader = csv.reader(csvfile,delimiter=',')
	for line in reader:
		user = {'paddle_num':int(line[0]), 'user_name':line[1]}
		users['users'].append(user)
jsonfile = open('users.json','w')
jsonfile.write(json.dumps(json.loads(json.dumps(users)), indent=4))
jsonfile.close()
