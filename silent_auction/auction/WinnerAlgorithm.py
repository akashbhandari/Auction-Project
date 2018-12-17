# File: WinnerAlgorithm.py
from operator import itemgetter, attrgetter, methodcaller
import json
from pprint import pprint

num_o_listings = 100
data = {}
data['items'] = []
lumped_data = {}
lumped_data['winning_bids'] = []

class Bid():

    def __init__(self,val,bidpad):
        self.value = val
        self.timestamp = 0
        self.BidderPaddle = bidpad
        self.isWinner = False

    def setWinner(self):
        self.isWinner = true

    def __str__(self):
        concatArray = ["(",str(self.value),", ", str(self.timestamp), ", ", str(self.BidderPaddle),")"]
        return "".join(concatArray)

    def __repr__(self):
        concatArray = ["(",str(self.value),", ", str(self.timestamp), ", ", str(self.BidderPaddle),")"]
        return "".join(concatArray)

class User():

    def __init__(self,pad_name,fname):
        self.PaddleNumber = pad_name
        self.FullName = fname

class Item():

    def __init__(self,name,repwin,quant,IID,SID):
        self.itemname = name
        self.repeatWinners = repwin
        self.quantity = quant
        self.itemID = IID
        self.sellerID = SID
        self.Bidsheet = []
        self.Winnersheet = []

    def addBid(self,addedbid):
        self.Bidsheet.append(addedbid)

    def printWinners(self):
        if(len(self.Winnersheet) == 0):
            print("Nobody Bid On This Item")
        else:
            for currentBid in self.Winnersheet:
                print(currentBid)

    def addWinnersToJson(self):
        WinnerEntries = []
        sample_item = {
            'item_name': self.itemname,
            'item_id': self.itemID,
            'winning_bids': []}

        for i in range(len(self.Winnersheet)):
            winningBid = self.Winnersheet[i]
            print(type(winningBid))

            if type(winningBid) is dict:
                jsobj = {'value':winningBid['value'], 'timestamp':winningBid['timestamp'],'bidder_id':winningBid['bidder_id']}
            else:
                jsobj = {'value': str(winningBid.value),'timestamp': str(winningBid.timestamp),'bidder_id': str(winningBid.BidderPaddle)}
            sample_item['winning_bids'].append(jsobj)
            lumped_data['winning_bids'].append(jsobj)

        data['items'].append(sample_item)
        return

    def chooseWinner(self):
        print("WinnerAlg Called")

        for r in range(0,len(self.Bidsheet)):
            self.Bidsheet[r].timestamp = len(self.Bidsheet)-r


        if (len(self.Bidsheet) <= self.quantity):
            self.Winnersheet.extend(self.Bidsheet)
            self.addWinnersToJson()
            return

        tempSheet = sorted(self.Bidsheet, key=attrgetter('value'), reverse = True)
        #print(str(tempSheet[0]))

        if(self.repeatWinners == False):
            NameRegistry = []

            for currentBid in tempSheet:
                for Name in NameRegistry:
                    if (currentBid.BidderPaddle == Name):
                        tempSheet.remove(CurrentBid)
                    else:
                        NameRegistry.add(currentBid.BidderPaddle)

        if(tempSheet[self.quantity-1].value == tempSheet[self.quantity].value):
            print("There's a tie!")
            isFirstTie = True
            FirstTieIndex = 0
            LastTieIndex = 0

            for currentBid in tempSheet:
                if(currentBid.value == tempSheet[self.quantity-1].value and isFirstTie == True):
                    FirstTieIndex = tempSheet.index(currentBid)
                    isFirstTie = False
                elif(currentBid.value != tempSheet[self.quantity-1].value and isFirstTie == False):
                    LastTieIndex = tempSheet.index(currentBid)-1

            if(LastTieIndex == 0):
                LastTieIndex = len(tempSheet)-1

            #print("First Tie Index:")
            #print(FirstTieIndex)
            #print("Last Tie Index:")
            #print(LastTieIndex)

            print(FirstTieIndex)
            allotedTies = self.quantity - FirstTieIndex
            NumTies = LastTieIndex-FirstTieIndex

            UnsortedTieList = tempSheet[FirstTieIndex:LastTieIndex+1]
            if (len(UnsortedTieList)==0):
              print("UnsortedTieList is empty")
            SortedTieList = sorted(UnsortedTieList, key=attrgetter('timestamp'), reverse = False)
            if (len(SortedTieList)==0):
              print("SortedTieList is empty")
            TieWinners = SortedTieList[0:allotedTies]
            print(len(TieWinners))

            WinnersList = tempSheet[0:FirstTieIndex]+TieWinners
            print(len(WinnersList))
            if (len(WinnersList)==0):
              print("WinnersList is empty")
            self.Winnersheet.extend(WinnersList)
            self.addWinnersToJson()
            return

        if (len(tempSheet)==0):
          print("tempSheet is empty")
        self.Winnersheet.extend(tempSheet[0:self.quantity])
        print(str(self.Winnersheet[0]))
        self.addWinnersToJson()
        return

ItemList = []

with open('items.json', 'r') as f:
    data_dict = json.load(f)
#pprint(data_dict)
for q in range(0,num_o_listings):
    just_made_item = Item(data_dict["items"][q]["item_name"],False,int(data_dict["items"][q]["item_amount"]),data_dict["items"][q]["item_id"],0) #def __init__(self,name,repwin,quant,IID,SID):
    for r in data_dict["items"][q]["bid_sheet"]:
        just_made_bid = Bid(int(r['bid_amount']),int(r['paddle_num']))
        just_made_item.Bidsheet.append(just_made_bid)
    ItemList.append(just_made_item)
#for currentItem in ItemList:
#    print(currentItem.itemname)

#print(Bid1)
#print(Bid1.BidderPaddle)

#Item1 = Item("Bicycle",False,1,"M42",1)
#Item1.addBid(Bid1)
#Item1.addBid(Bid2)
#Item1.addBid(Bid3)
#Item2 = Item("Another Bicycle",False,2,"M43",1)
#Item2.addBid(Bid1)
#Item2.addBid(Bid2)
#Item2.addBid(Bid3)
#print(str(Item1.Bidsheet[0]))
#print(str(Item1.Bidsheet[1]))
#print(str(Item1.Bidsheet[2]))

#Item1.chooseWinner()
#Item2.chooseWinner()

#Item3 = ItemList[0]
#print(type(Item3.Bidsheet[0]))
#Item3.chooseWinner()
#Item1.printWinners()
#Item2.printWinners()
#Item3.printWinners()
print(len(ItemList))
#print(str(Item1.Winnersheet[1]))

for k in range(0,len(ItemList)):
	ItemList[k].chooseWinner()

with open('WinnerResults.json', 'w') as outfile:
    json.dump(data, outfile, indent = 4)
with open('LumpedWinnerResults.json', 'w') as outfile:
    json.dump(lumped_data, outfile, indent = 4)
