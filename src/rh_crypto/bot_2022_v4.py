import math
from robin_stocks import robinhood
from pyotp.totp import TOTP
from os import environ

# Program description:
# A Robinhood bot created to automatically monitor and trade crypto currency currently supported by Robinhood.
# Works specifically for DOGE, but can work for other tokens that have miniscule values.
#
# This bot runs a scheduler every 10 seconds in order to update the prices on a 10 second interval for a 
# list that will hold the previous prices for past 1 minute.
# 
# This bot [REQUIRES] a individual to already have SET amount of shares of the current crypto they want to trade.
# 
#   Instructions after entering in login information (no particular order):
#
#       1. Fill in ticker (since this bot is specifically for DOGE, should be left alone)
#       2. Fill in average_cost
#       3. Fill in shares_to_buy amount (in dollars $)
#       4. Fill in shares_to_sell amount (in dollars $)
#       5. Fill in num_shares 
#

# Some buying and selling errors will occur if a individual does not have enough shares to sell or enough money to buy.
# If errors occur, simply re-update through redoing instructions above and restart the program.

# Robinhood.login(username="example72", password="AnotherExample8")

class Bot:
    # 10 second interval price history list, for every 1 minute
    seep = []
    mazda = []

    counter_one = 1.0
    counter_two = 1.0

    shares_to_sell = 0.00
    shares_to_sell_dollar = 6

    # ratio of buy to sell 2:6 ≈ 1:3
    shares_to_buy = 0.00
    shares_to_buy_dollar = 2

    # ratio of buy to sell 2:6 ≈ 1:3
    update_shares_buy = 1
    update_shares_sell = 3

    # step (5)
    # number of shares based on (total cost / shares_to_buy)
    # EX: ($100 / 2) = 50
    num_shares = 50

    # step (2)
    # average cost
    average_cost = 0.833000

    # average cost ceiling percentage (ensures there is a large enough disparity between the live price and the required minimal amount that is greater than the live price to obtain profitability when selling)
    # average cost floor percentage(ensures there is a large enough disparity between the live price and the required minimal amount that is lower than the live price to obtain profitability when buying)
    ac_ceiling = 0.02
    ac_floor = 0.015

    # crypto currency ticker available on robinhood
    ticker = "MATIC"

    quote = None

    def run(self):
        robinhood.authentication.login(
            environ['RH_USERNAME'], 
            environ['RH_PASSWORD'], 
            TOTP("Sauce").now()
        )

        self.quote = robinhood.crypto.get_crypto_quote(self.ticker, info="mark_price")

        print(self.ticker + ": $" + str(self.quote))

        self.seeps()
        self.buy()
        self.sell()

        # Keeps track of counter
        print("c1:" + str(self.counter_one))
        print("c2:" + str(self.counter_two))
        self.counter_one += 1
        self.counter_two += 1

        return {
            "average_cost": self.average_cost,
            "num_shares": self.num_shares,
            "shares_to_buy_dollar": self.shares_to_buy_dollar,
            "shares_to_sell_dollar": self.shares_to_sell_dollar,
            "counter_one": self.counter_one,
            "counter_two": self.counter_two,
            "seep": self.seep,
        }
        
    # Functions to buy and sell crypto currency   
    def buy(self):
        self.quote = robinhood.orders.order_buy_crypto_by_quantity(self.ticker, self.amountD)
        print(self.quote)

    def sell(self):
        self.quote = robinhood.orders.order_sell_crypto_by_quantity(self.ticker,self.amountD)
        print(self.quote)

    def seeps(self):
        self.seep.append(self.quote)

        seepLen = len(self.seep)

        if seepLen > 6:
            # if there are 5 or more elements in the list, rearrange positions
            self.mazda = self.self.seep[1:7]
            self.seep = self.self.seep[-1:]

            self.seep = self.mazda + self.seep
            print("Cleared and repositioned")

        if seepLen == 1:
            #0sec
            print("appended self.seep[0]")
            print(self.seep)
        elif seepLen == 2:
            #seep.append(self.quote) #10sec
            print("appended self.seep[1]")
            print(self.seep)
        elif seepLen == 3:
            #seep.append(self.quote) #20sec
            print("appended self.seep[2]")
            print(self.seep)
        elif seepLen == 4:
            #seep.append(self.quote) #30sec
            print("appended self.seep[3]")
            print(self.seep)
        elif seepLen == 5:
            #seep.append(self.quote) #40sec
            print("appended self.seep[4]")
            print(self.seep)
        elif seepLen == 6:
            #seep.append(self.quote) #50sec
            print("appended self.seep[5]")
            print(self.seep)
        elif seepLen == 7:
            #seep.append(self.quote) #60sec/1min
            print("appended self.seep[6]")
            print(self.seep)
    def buy(self):
        if self.counter_one == 7: 
            if self.calculate_seep_one(self.seep[0], 1.006):
                # instruction step (3) fill in amount in dollars in place of float(20)
                shares_to_buy = math.floor(float(self.shares_to_buy_dollar) / float(self.quote)-1)
                self.buy(self.ticker, shares_to_buy)
                print("bought:", self.quote)
                tempval = average_cost*num_shares
                average_cost = tempval
                average_cost += float(self.quote)
                num_shares += self.update_shares_buy
                average_cost /= float(num_shares)
                print("avg cost:" + str(average_cost))
        elif self.counter_one == 6: 
            if self.calculate_seep_one(self.seep[0], 1.005):
                # instruction step (3) fill in amount in dollars in place of float(20)
                shares_to_buy = math.floor(float(self.shares_to_buy_dollar) / float(self.quote)-1)
                self.buy(self.ticker, shares_to_buy)
                print("bought:", self.quote)
                tempval = average_cost*num_shares
                average_cost = tempval
                average_cost += float(self.quote)
                num_shares += self.update_shares_buy
                average_cost /= float(num_shares)
                print("avg cost:" + str(average_cost))
                
        elif self.counter_one == 5:
            if self.calculate_seep_one(self.seep[0], 1.0045):
                # instruction step (3) fill in amount in dollars in place of float(20)
                shares_to_buy = math.floor(float(self.shares_to_buy_dollar) / float(self.quote)-1)
                self.buy(self.ticker, shares_to_buy)
                print("bought:", self.quote)
                tempval = average_cost*num_shares
                average_cost = tempval
                average_cost += float(self.quote)
                num_shares += self.update_shares_buy
                average_cost /= float(num_shares)
                print("avg cost:" + str(average_cost))
                
        elif self.counter_one == 4:
            if self.calculate_seep_one(self.seep[0], 1.004):
                # instruction step (3) fill in amount in dollars in place of float(20)
                shares_to_buy = math.floor(float(self.shares_to_buy_dollar) / float(self.quote)-1)
                self.buy(self.ticker, shares_to_buy)
                print("bought:", self.quote)
                tempval = average_cost*num_shares
                average_cost = tempval
                average_cost += float(self.quote)
                num_shares += self.update_shares_buy
                average_cost /= float(num_shares)
                print("avg cost:" + str(average_cost))
                
        elif self.counter_one == 3:
            if self.calculate_seep_one(self.seep[0], 1.0035):
                # instruction step (3) fill in amount in dollars in place of float(20)
                shares_to_buy = math.floor(float(self.shares_to_buy_dollar) / float(self.quote)-1)
                self.buy(self.ticker, shares_to_buy)
                print("bought:", self.quote)
                tempval = average_cost*num_shares
                average_cost = tempval
                average_cost += float(self.quote)
                num_shares += self.update_shares_buy
                average_cost /= float(num_shares)
                print("avg cost:" + str(average_cost))
                
        elif self.counter_one == 2:
            if self.calculate_seep_one(self.seep[0], 1.003):
                # instruction step (3) fill in amount in dollars in place of float(20)
                shares_to_buy = math.floor(float(self.shares_to_buy_dollar) / float(self.quote)-1)
                self.buy(self.ticker, shares_to_buy)
                print("bought:", self.quote)
                tempval = average_cost*num_shares
                average_cost = tempval
                average_cost += float(self.quote)
                num_shares += self.update_shares_buy
                average_cost /= float(num_shares)
                print("avg cost:" + str(average_cost))
        elif self.counter_one >= 7:
            if self.calculate_seep_two(self.seep[0], 1.004):
                # instruction step (3) fill in amount in dollars in place of float(20)
                shares_to_buy = math.floor(float(self.shares_to_buy_dollar) / float(self.quote)-1)
                self.buy(self.ticker, shares_to_buy)
                print("bought:", self.quote)
                tempval = average_cost*num_shares
                average_cost = tempval
                average_cost += float(self.quote)
                num_shares += self.update_shares_buy
                average_cost /= float(num_shares)
                print("avg cost:" + str(average_cost))
            elif self.calculate_seep_two(self.seep[1], 1.005):
                # instruction step (3) fill in amount in dollars in place of float(20)
                shares_to_buy = math.floor(float(self.shares_to_buy_dollar) / float(self.quote)-1)
                self.buy(self.ticker, shares_to_buy)
                print("bought:", self.quote)
                tempval = average_cost*num_shares
                average_cost = tempval
                average_cost += float(self.quote)
                num_shares += self.update_shares_buy
                average_cost /= float(num_shares)
                print("avg cost:" + str(average_cost))
            elif self.calculate_seep_two(self.seep[2], 1.006):
                # instruction step (3) fill in amount in dollars in place of float(20)
                shares_to_buy = math.floor(float(self.shares_to_buy_dollar) / float(self.quote)-1)
                self.buy(self.ticker, shares_to_buy)
                print("bought:", self.quote)
                tempval = average_cost*num_shares
                average_cost = tempval
                average_cost += float(self.quote)
                num_shares +=self.update_shares_buy
                average_cost /= float(num_shares)
                print("avg cost:" + str(average_cost))
                
            elif self.calculate_seep_two(self.seep[3], 1.007):
                # instruction step (3) fill in amount in dollars in place of float(20)
                shares_to_buy = math.floor(float(self.shares_to_buy_dollar) / float(self.quote)-1)
                self.buy(self.ticker, shares_to_buy)
                print("bought:", self.quote)
                tempval = average_cost*num_shares
                average_cost = tempval
                average_cost += float(self.quote)
                num_shares += self.update_shares_buy
                average_cost /= float(num_shares)
                print("avg cost:" + str(average_cost))
            elif self.calculate_seep_two(self.seep[4], 1.008):
                # instruction step (3) fill in amount in dollars in place of float(20)
                shares_to_buy = math.floor(float(self.shares_to_buy_dollar) / float(self.quote)-1)
                self.buy(self.ticker, shares_to_buy)
                print("bought:", self.quote)
                tempval = average_cost*num_shares
                average_cost = tempval
                average_cost += float(self.quote)
                num_shares += self.update_shares_buy
                average_cost /= float(num_shares)
                print("avg cost:" + str(average_cost))
            elif self.calculate_seep_two(self.seep[5], 1.01):
                # instruction step (3) fill in amount in dollars in place of float(20)
                shares_to_buy = math.floor(float(self.shares_to_buy_dollar) / float(self.quote)-1)
                self.buy(self.ticker, shares_to_buy)
                print("bought:", self.quote)
                tempval = average_cost*num_shares
                average_cost = tempval
                average_cost += float(self.quote)
                num_shares += self.update_shares_buy
                average_cost /= float(num_shares)
                print("avg cost:" + str(average_cost))
            elif self.calculate_seep_two(self.seep[6], 1.013):
                # instruction step (3) fill in amount in dollars in place of float(20)
                shares_to_buy = math.floor(float(self.shares_to_buy_dollar) / float(self.quote)-1)
                self.buy(self.ticker, shares_to_buy)
                print("bought:", self.quote)
                tempval = average_cost*num_shares
                average_cost = tempval
                average_cost += float(self.quote)
                num_shares += self.update_shares_buy
                average_cost /= float(num_shares)
                print("avg cost:" + str(average_cost))
    def sell(self):
        if self.counter_two < 7:
            if self.counter_two == 7:
                if float(self.seep[0])*1.01 < float(self.quote) and float(self.quote) > float(self.average_cost+float(self.average_cost*float(self.ac_ceiling))):

                    # instruction step (4) fill in amount in dollars in place of float(100)
                    shares_to_sell = math.floor(float(self.shares_to_sell_dollar) / float(self.quote)+1)
                    self.sell(self.ticker, shares_to_sell)
                    print("sold:", self.quote)
                    print("avg cost:", self.average_cost)
                    num_shares -= self.update_shares_sell

            elif self.counter_two == 6:
                if float(self.seep[0])*1.0075 < float(self.quote) and float(self.quote) > float(self.average_cost+float(self.average_cost*float(self.ac_ceiling))):

                    # instruction step (4) fill in amount in dollars in place of float(100)
                    shares_to_sell = math.floor(float(self.shares_to_sell_dollar) / float(self.quote)+1)
                    self.sell(self.ticker, shares_to_sell)
                    print("sold:", self.quote)
                    print("avg cost:", self.average_cost)
                    num_shares -= self.update_shares_sell
                    
            elif self.counter_two == 5:
                if float(self.seep[0])*1.0065 < float(self.quote) and float(self.quote) > float(self.average_cost+float(self.average_cost*float(self.ac_ceiling))):

                    # instruction step (4) fill in amount in dollars in place of float(100)
                    shares_to_sell = math.floor(float(self.shares_to_sell_dollar) / float(self.quote)+1)
                    self.sell(self.ticker, shares_to_sell)
                    print("sold:", self.quote)
                    print("avg cost:", self.average_cost)
                    num_shares -= self.update_shares_sell
                    
            elif self.counter_two == 4:
                if float(self.seep[0])*1.0055 < float(self.quote) and float(self.quote) > float(self.average_cost+float(self.average_cost*float(self.ac_ceiling))):

                    # instruction step (4) fill in amount in dollars in place of float(100)
                    shares_to_sell = math.floor(float(self.shares_to_sell_dollar) / float(self.quote)+1)
                    self.sell(self.ticker, shares_to_sell)
                    print("sold:", self.quote)
                    print("avg cost:", self.average_cost)
                    num_shares -= 2.0
                    
            elif self.counter_two == 3:
                if float(self.seep[0])*1.0045 < float(self.quote) and float(self.quote) > float(self.average_cost+float(self.average_cost*float(self.ac_ceiling))):

                    # instruction step (4) fill in amount in dollars in place of float(100)
                    shares_to_sell = math.floor(float(self.shares_to_sell_dollar) / float(self.quote)+1)
                    self.sell(self.ticker, shares_to_sell)
                    print("sold:", self.quote)
                    print("avg cost:", self.average_cost)
                    num_shares -= self.update_shares_sell
                    
            elif self.counter_two == 2:
                if float(self.seep[0])*1.0035 < float(self.quote) and float(self.quote) > float(self.average_cost+float(self.average_cost*float(self.ac_ceiling))):

                    # instruction step (4) fill in amount in dollars in place of float(100)
                    shares_to_sell = math.floor(float(self.shares_to_sell_dollar) / float(self.quote)+1)
                    self.sell(self.ticker, shares_to_sell)
                    print("sold:", self.quote)
                    print("avg cost:", self.average_cost)
                    num_shares -= self.update_shares_sell

        if self.counter_two >= 7:

            if float(self.quote)*0.997 > float(self.seep[0]) and float(self.quote) > float(self.average_cost+float(self.average_cost*float(self.ac_ceiling))):

                # instruction step (4) fill in amount in dollars in place of float(100)
                shares_to_sell = math.floor(float(self.shares_to_sell_dollar) / float(self.quote)+1)
                self.sell(self.ticker, shares_to_sell)
                print("sold:", self.quote)
                print("avg cost:", self.average_cost)
                num_shares -= self.update_shares_sell
            
            elif float(self.quote)*0.996 > float(self.seep[1]) and float(self.quote) > float(self.average_cost+float(self.average_cost*float(self.ac_ceiling))):

                # instruction step (4) fill in amount in dollars in place of float(100)
                shares_to_sell = math.floor(float(self.shares_to_sell_dollar) / float(self.quote)+1)
                self.sell(self.ticker, shares_to_sell)
                print("sold:", self.quote)
                print("avg cost:", self.average_cost)
                num_shares -= self.update_shares_sell
                
            elif float(self.quote)*0.995 > float(self.seep[2]) and float(self.quote) > float(self.average_cost+float(self.average_cost*float(self.ac_ceiling))):

                # instruction step (4) fill in amount in dollars in place of float(100)
                shares_to_sell = math.floor(float(self.shares_to_sell_dollar) / float(self.quote)+1)
                self.sell(self.ticker, shares_to_sell)
                print("sold:", self.quote)
                print("avg cost:", self.average_cost)
                num_shares -= self.update_shares_sell
                
            elif float(self.quote)*0.993 > float(self.seep[3]) and float(self.quote) > float(self.average_cost+float(self.average_cost*float(self.ac_ceiling))):

                # instruction step (4) fill in amount in dollars in place of float(100)
                shares_to_sell = math.floor(float(self.shares_to_sell_dollar) / float(self.quote)+1)
                self.sell(self.ticker, shares_to_sell)
                print("sold:", self.quote)
                print("avg cost:", self.average_cost)
                num_shares -= self.update_shares_sell
                
            elif float(self.quote)*0.992 > float(self.seep[4]) and float(self.quote) > float(self.average_cost+float(self.average_cost*float(self.ac_ceiling))):

                # instruction step (4) fill in amount in dollars in place of float(100)
                shares_to_sell = math.floor(float(self.shares_to_sell_dollar) / float(self.quote)+1)
                self.sell(self.ticker, shares_to_sell)
                print("sold:", self.quote)
                print("avg cost:", self.average_cost)
                num_shares -= self.update_shares_sell
                
            elif float(self.quote)*0.991 > float(self.seep[5]) and float(self.quote) > float(self.average_cost+float(self.average_cost*float(self.ac_ceiling))):

                # instruction step (4) fill in amount in dollars in place of float(100)
                shares_to_sell = math.floor(float(self.shares_to_sell_dollar) / float(self.quote)+1)
                self.sell(self.ticker, shares_to_sell)
                print("sold:", self.quote)
                print("avg cost:", self.average_cost)
                num_shares -= self.update_shares_sell
                
            elif float(self.quote)*0.988 > float(self.seep[6]) and float(self.quote) > float(self.average_cost+float(self.average_cost*float(self.ac_ceiling))):

                # instruction step (4) fill in amount in dollars in place of float(100)
                shares_to_sell = math.floor(float(self.shares_to_sell_dollar) / float(self.quote)+1)
                self.sell(self.ticker, shares_to_sell)
                print("sold:", self.quote)
                print("avg cost:", self.average_cost)
                num_shares -= self.update_shares_sell
    def calculate_seep_one(self, seep, amount: float):
        return float(seep) * amount > float(self.quote) and float(self.quote) < float(self.average_cost - float(self.average_cost * float(self.ac_floor)))
    def calculate_seep_two(self, seep, amount: float):
        return float(self.quote)* amount < float(seep) and float(self.quote) < float(self.average_cost - float(self.average_cost * float(self.ac_floor)))