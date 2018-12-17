import json
from operator import itemgetter
from collections import OrderedDict
import collections

dict1 = {}
itemsWithWinner ={}

def sortBidSheet(bidsheet, min_bid_value):
    bidSheet = {}
    array = []
    for item in bidsheet:
        bidSheet[item["bid_amount"]] = item["user_name"]
    print(bidSheet)
    #Bids = collections.namedtuple('UserName', 'BidAmount')
    #sortedBidSheet = sorted([Bids(k,v) for (k,v) in bidSheet.items()], reverse = True)
    #firstFive = sortBidSheet[:5]
    return 0

with open('items2.json', 'r') as f:
    data_dict = json.load(f)
    data = data_dict["items"]
    for i in data:
        itemsWithWinner[i["item_name"]] = sortBidSheet(i["bid_sheet"],i["min_bid"])
        print(itemsWithWinner[i["item_name"]])
        break
        #dict1[i["item_id"]] = 
#print(data_dict)
