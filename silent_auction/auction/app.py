"""
    Silent Auction python app.
	Author: Akash Bhandari (akashbhandari@bennington.edu)
	Date: Oct 7th, 2018
"""
import json
from flask import Flask, render_template, request 

global_paddle_number = 0
global_item_id = ""

app = Flask(__name__)
@app.route('/')
def index():
	return render_template('login.html')

# @app.route('/admin_registration')
# def admin_registration():
# 	return render_template('registration.html')

# @app.route('/confirm_admin_registration', methods=['POST'])
# def confirm_admin_registration():
# 	username = request.form['user_name']
# 	paddle_num = request.form['paddle_num']
# 	registration(username,paddle_num)
# 	return render_template('confirm_admin_registration.html', name = username, paddle_num = paddle_num)

@app.route('/confirmation', methods=['POST'])
def confirmation():
	global global_paddle_number
	paddle_num = request.form['paddle_num']
	global_paddle_number = int(paddle_num)
	name = get_name(int(paddle_num))
	return render_template('confirmation.html', name = name)

@app.route('/search', methods=['POST'])
def search():
	return render_template('item_search.html')

@app.route('/item_bidsheet', methods = ['POST'])
def item_bidsheet():
	global global_item_id
	item_id = request.form['item_id']
	global_item_id = str(item_id)
	item_dict = get_item_dict(item_id)
	if item_dict:
		return render_template('bid_page.html', item_dict = item_dict)
	return render_template('item_search.html')

@app.route('/bid_confirmation', methods=['POST'])
def bid_confirmation():
	global global_paddle_number
	global global_item_id
	bid_amount = float(request.form['amount'])
	place_bid(global_paddle_number, bid_amount, global_item_id)
	return render_template('bid_confirmation.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Regiter and render confirm html page"""
    if request.method == 'POST':
        username = request.form['username']
        paddle_number = int(request.form['paddle_number'])
        if registration(username, paddle_number): 
            return render_template('confirm.html', data = {'username': username, 'pin_number': paddle_number})
    return render_template('register.html')

#bids
def place_bid(paddle_num,bid_amount,item_id):
	item_dict = get_item_dict(item_id)
	if not check_bid_input(bid_amount) and (bid_amount<item_dict['min_bid']):
		return False
	else:
		items_dict=get_items_dict()
		user_name=get_name(int(paddle_num))
		item_index=find_index_of_item(items_dict,item_dict['item_id'])
		item_bid_dict = {"user_name":user_name, "paddle_num":paddle_num, "bid_amount":bid_amount}
		items_dict['items'][item_index]['bid_sheet'].append(item_bid_dict)
		write_item_json(items_dict)

def registration(username, paddle_num):
	if check_paddle_num_input(username, paddle_num):
		users_dict=get_users_dict()
		if check_registration(users_dict, username, paddle_num):
			user_dict={"paddle_num": paddle_num,"user_name": username}
			users_dict["users"].append(user_dict)
			write_user_json(users_dict)
			return True
	else:
		raise ValueError("Check your username and paddle number types!")
		return False

def check_registration(users,username, paddle_num):
		for user in users['users']:
			if user['paddle_num'] == paddle_num:
				raise ValueError("{0} already exists".format(paddle_num))
		return True

def check_bid_input(bid):
	if (type(bid) is not float) and (type(bid) is not int):
		raise ValueError("Must be a number value!")
	return True

def check_paddle_num_input(username, paddle_num):
	if type(paddle_num) is not int:
		raise ValueError("{0} should be integers".format(paddle_num))
	if type(username) is not str:
		raise ValueError("{0} should be string".format(username))
	return True

def get_item_bid_sheet(item_id):
	return get_item_dict(item_id)['bid_sheet']

def write_item_json(dict):
	jsonfile = open("items.json",'w')
	jsonfile.write(json.dumps(json.loads(json.dumps(dict)), indent=4))
	jsonfile.close()

def write_user_json(dict):
	jsonfile = open("users.json",'w')
	jsonfile.write(json.dumps(json.loads(json.dumps(dict)), indent=4))
	jsonfile.close()

def find_index_of_item(items_dict,item_id):
	for item in items_dict['items']:
		if item['item_id'] == item_id:
			return items_dict['items'].index(item)
#user for login
def get_name(paddle_num):
	users_dict=get_users_dict()
	for user in users_dict['users']:
		if user['paddle_num'] == paddle_num:
			return user['user_name']
	else:
		raise ValueError("We can't identify you!")

def get_users_dict():
	users_json = open ('users.json','r')
	users_dict = json.load(users_json)
	users_json.close()
	return users_dict

def get_items_dict():
	items_json = open ('items.json','r')
	items_dict = json.load(items_json)
	items_json.close()
	return items_dict

# we need a sleep function to check if the bidsheet displayed needs updating. Probably JS.

#gets information of item
def get_item_dict(input_id):
	items_dict=get_items_dict()
	for item in items_dict['items']:
		if item['item_id']==input_id:
			return item

def does_item_exist(input_id):
	items_dict=get_items_dict()
	for item in items_dict['items']:
			if item['item_id']==input_id:
					return True
	return False

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=50000, debug=True)
	# print(get_name(1616))
	#place_bid(1616, 100000, "S27")
	
