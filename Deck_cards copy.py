from random import shuffle


class Card():
	def __init__(self, rank, suit, name):
		self.rank = rank
		self.suit = suit
		self.name = name

	def __str__(self):
		return '{} of {}'.format(self.rank, self.name)

rank = ['heart', 'spade', 'diamond', 'club']
suit = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
name = ['Ace', 2, 3, 4, 5, 6, 7, 8, 9, 10, 'Jack', 'Queen', 'King']

#card1 = Card(rank[0], suit[0], name[0])
#card2 = Card(rank[0], suit[1], name[1])

card_instances = []

for item in rank:
	for i in range(13):
		card1 = Card(item, suit[i], name[i])
		card_instances.append(card1)

# if you're trying to print items from a class in a list, if you just print the list, it will give the object type
# so you need to iterate through the list to get the object so you get what you want
for each in card_instances:
	print(each)

class Deck(Card): #putting Card in the () gives this function access to everything in class Card - inheritance
	def __init__(self, card_lst):
		self.cards = card_lst

	def card_shuffle(self):
		shuffle(self.cards)

	def remove_card(self, i): #this pops cards off the deck
		self.cards.pop(i)

	def deal_hand(self, num): #shuffles the deck, gets
		self.cards.card_shuffle() #we called card shuffle on the deck object
		deal = self.cards[:num]  #deal deck 1 cards - wanting to access object, type variable after self - this creates a Hand
		for i in range(num):
			self.cards.remove_card(0)
		return deal

class Hand():
	def __init__(self, lst):
		self.cards = lst

	def remove_card(self, i): #this pops cards off the hand
		self.cards.pop(i)


deck1 = Deck(card_instances) #need to read in a list of card_instances to create a deck
print(deck1.cards) #this will take the deck and access the card variable

for each in deck1.cards:
	print(each)

deck1.card_shuffle() #this calls a shuffle on the deck of cards

for each in deck1.cards:
	print(each)

# shuffle deck and read first five elements in the deck anad create a hand and pop off those three elements in the list
#deck1.card_shuffle() #we called card shuffle on the deck object
#deal = deck1.cards[:5]  #deal deck 1 cards - wanting to access object, type variable after self - this creates a Hand
#for i in range(5):
#	deck1.remove_card(0) #this will remove the first element each time for 5 times

deal = deck1.deal_hand(6)





print(len(deck1.cards))

#hand object
hand1 = Hand(deal) #read the deal into hands, we have a hand with 5 cards
for each in hand1.cards:  #so we don't get the object location numbers
	print(each)










