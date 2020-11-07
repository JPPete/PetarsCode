from random import shuffle

suits = ('Hearts','Spades','Diamonds','Clubs')
ranks = ('Ace','Two','Three','Four','Five','Six','Seven','Eight','Nine','Ten','Jack','Queen','King')
values = {'Ace':11,'Two':2,'Three':3,'Four':4,'Five':5,'Six':6,'Seven':7,'Eight':8,'Nine':9,'Ten':10,'Jack':10,'Queen':10,'King':10}


#Card
class Card:

    def __init__(self,suit,rank):
        self.suit = suit.capitalize()
        self.rank = rank.capitalize()
        self.value = values[self.rank]

    def __str__(self):
        return self.rank + ' of ' + self.suit
#Deck
class Deck:

    def __init__(self):
        
        self.all_cards = []

        for suit in suits:
            for rank in ranks:
                created_card = Card(suit,rank)
                self.all_cards.append(created_card)

    def shuffle(self):
        shuffle(self.all_cards)

    def deal_one(self):
        return self.all_cards.pop()


#Player
class Player:

    def __init__(self,money = 1000):
        self.player_cards = []
        self.money = money
        self.money_on_table = 0

    #get cards on table
    def get_card(self,new_card):
        self.player_cards.append(new_card)

    #throw away cards
    def reset(self):
        self.player_cards =[]

    #place a bet (remove money from player)
    def bet(self,amount):

        self.money_on_table += amount
        self.money -= amount


    def won_round(self):
        self.money += self.money_on_table * 2

    #lost money in the round
    def lost_round(self):
        self.money_on_table = 0

    #Check if player busted
    def check_bust(self):
        self.bust_check = 0
        self.ace_counter = 0
        
        for j in self.player_cards:
            #check for aces
            if j.rank == 'Ace':
                self.ace_counter +=1
                
            self.bust_check += j.value
        #if bust_check is over 21 it removes 10 for every ace that the player has
        while self.ace_counter > 0 and self.bust_check > 21:
            self.bust_check -= 10
            self.ace_counter -= 1
        
        return self.bust_check

    #prints out cards held by the player
    def __str__(self):
        held = ''
        for i in self.player_cards:
            held += str(i) + ' :' + str(i.value) + '\n'
        return f'{held}\nPlayers money:{self.money}'
        

#Dealer
class Dealer:
    def __init__(self,money = 1000):
        self.dealer_cards = []
        self.money = money
        self.money_on_table = 0
        self.hidden_card = ''

    #get cards on table
    def get_card(self,new_card):
        self.dealer_cards.append(new_card)

    #throw away cards
    def reset(self):
        self.dealer_cards =[]

    #show hidden card
    def show_hidden(self):
        return self.hidden_card
    
    #Check if dealer busted
    def check_bust(self):
        self.bust_check = 0
        self.ace_counter = 0
        
        for j in self.dealer_cards:
            #check for aces
            if j.rank == 'Ace':
                self.ace_counter +=1
    
            self.bust_check += j.value
        #if bust_check is over 21 it removes 10 for every ace that the dealer has
        while self.ace_counter > 0 and self.bust_check > 21:
            self.bust_check -= 10
            self.ace_counter -= 1

        return self.bust_check
    
    #prints out cards held by the dealer except for the 1st one
    def __str__(self):
        held = ''
        for i in self.dealer_cards:
            if i == self.dealer_cards[0]:
                self.hidden_card = i
                continue
            else:
                held += str(i) + ' :' + str(i.value) + '\n'
        return held
 
   

    
#Game Logic

#create a deck and shuffle it
new_deck = Deck()
new_deck.shuffle()

#create a dealer
dealer = Dealer()

#create a player
player1 = Player()

#Game Starts
game_on = True

while game_on:
    player1.player_cards = []
    dealer.dealer_cards = []
    round_on = True

    #check if someone won
    if player1.money == 0 and player1.money_on_table == 0:
        print('The player doesnt have any more money')
        break
    


    #Round Happens
    while round_on:
        
        print('\nYou place 100 for the start of the round!\n')
        #initial bet
        player1.bet(100)

        #dealer gets two cards
        for x in range(2):
            dealer.get_card(new_deck.deal_one())
        #show dealers card
        print('The Dealer has: ')
        print('A HIDDEN Card')
        print(dealer)

        #player gets two cards
        for x in range(2):
            player1.get_card(new_deck.deal_one())
        
        player_bust_check = player1.check_bust()
        
        #show players cards
        print('The Player has: ')
        print(player1)
        print(f'Players value is {player_bust_check}')

        
        dealer_bust_check = dealer.check_bust()

        #Bet and Get new cards
        go_on = True
        while go_on:

            #checks if player has any money before asking to bet more
            if player1.money > 0:
                #does the player want to bet more
                bet_y_n = input('Do you want to bet more, y or n?\n')
            else:
                bet_y_n = 'n'
            
            if player_bust_check > 21:
                print('BUST!')
                print(f'Player has over 21:\n{player1}')
                print(f'Players current value is: {player_bust_check}')
                player1.money_on_table = 0
                round_on = False
                go_on = False
                break

            #counts so you can bet max 2 times
            count_bets = 0

            #if he wants to
            if bet_y_n.lower() == 'y' and count_bets <= 2:
                
                while True:
                    
                    try:
                        dont_have_enough = True
                        #asking for the amount and checking if the player has enoug money
                        while dont_have_enough == True:
                            bet_amount = int(input('How much do you want to bet?'))
                            if bet_amount <= player1.money:
                                player1.bet(bet_amount)
                                count_bets += 1
                                dont_have_enough == False
                                break
                            else:
                                print('You cant bet more then you have!')   
                    except:
                        print('You have to put your bet in integers!')
                        continue
                    else:
                        break
            
            #Do you want more cards
            get_new_card = input('Do you want a new card, y or n?\n')
            
                
            if get_new_card == 'y':
                player1.get_card(new_deck.deal_one())
                player_bust_check = player1.check_bust()
                print(f'Player has:\n{player1}')
                print(f'Players current value is: {player_bust_check}')
            else:
                print(f'Player has:\n{player1}')
                print(f'Players current value is: {player_bust_check}')
                go_on = False
                

           
            #Checking to see if player went over 21
            
            
            if player_bust_check > 21:
                print('\nBUST!!!\n')
                print(f'Player has over 21:\n{player1}')
                print(f'Players current value is: {player_bust_check}')
                player1.money_on_table = 0
                go_on = False
                round_on = False
                break
        if round_on == False:
            break
        #Show dealers hidden card
        print(f'\nDealers cards are:\n{dealer.hidden_card}\n{dealer}')

        #check to see if the player has less then the dealer
        if player1.check_bust() < dealer.check_bust():
            print(f'Players current value is: {player_bust_check}')
            print(f'Dealers current value is: {dealer_bust_check}')
            print('You have less then the dealer\nYOU HAVE LOST\n')
            player1.money_on_table = 0
            round_on = False
            break
            

        

        #Checking the dealer
        while True:
            
            dealer_bust_check = dealer.check_bust()
            if dealer_bust_check < player_bust_check or (dealer_bust_check == player_bust_check and dealer_bust_check != 21):
                dealer.get_card(new_deck.deal_one())
                dealer_bust_check = dealer.check_bust()
                   
                if dealer_bust_check > 21:
                    print('\nDEALER BUSTS!!!\n')
                    print(f'Dealer has over 21:\n')
                    print(f'Player won with:\n{player1}\n')
                    print(f'Dealer lost with:\n{dealer.hidden_card}\n{dealer}')
                    player1.won_round()
                    round_on = False
                    break
                if dealer_bust_check == player_bust_check == 21:
                    print('\nITS A TIE!!!\n')
                    print(f'Players cards are:\n{player1}')
                    print(f'Dealers cards are:\n{dealer.hidden_card}\n{dealer}')
                    print(f'Both player and the dealer have {player_bust_check}')
                    player1.money += player1.money_on_table
                    round_on = False
                    break
                if dealer_bust_check > player_bust_check:
                    print('\nDEALER WINS!!!\n')
                    print(f'Players cards are:\n{player1}')
                    print(f'\nDealers cards are:\n{dealer.hidden_card}\n{dealer}')
                    player1.money_on_table = 0
                    round_on = False
                    break

                

    continue_playing = input('Do you want to continue playing, y or n?')
    if continue_playing == 'n':
        print(f'Player has {player1.money} money')
        game_on = False
    
