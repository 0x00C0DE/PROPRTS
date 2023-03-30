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

    def run(self):
        robinhood.authentication.login(
            environ.get("RH_USERNAME"), 
            environ.get("RH_PASSWORD"), 
            TOTP("Sauce").now()
        )

        r = robinhood.crypto.get_crypto_quote(self.ticker, info="mark_price")
        #r = robin_stocks.robinhood.get_latest_price(ticker)
        print(self.ticker + ": $" + str(r))

        seep.append(r)

        if len(seep) > 6:
            # if there are 5 or more elements in the list, rearrange positions
            mazda = seep[1:7]
            seep = seep[-1:]

            seep = mazda + seep
            print("Cleared and repositioned")

        if len(seep) == 1:
            #0sec
            print("appended seep[0]")
            print(seep)
        elif len(seep) == 2:
            #seep.append(r) #10sec
            print("appended seep[1]")
            print(seep)
        elif len(seep) == 3:
            #seep.append(r) #20sec
            print("appended seep[2]")
            print(seep)
        elif len(seep) == 4:
            #seep.append(r) #30sec
            print("appended seep[3]")
            print(seep)
        elif len(seep) == 5:
            #seep.append(r) #40sec
            print("appended seep[4]")
            print(seep)
        elif len(seep) == 6:
            #seep.append(r) #50sec
            print("appended seep[5]")
            print(seep)
        elif len(seep) == 7:
            #seep.append(r) #60sec/1min
            print("appended seep[6]")
            print(seep)

        # BUY
        if counter_one < 7:
            if counter_one == 7: 
                if float(seep[0])*1.006 > float(r) and float(r) < float(average_cost-float(average_cost*float(self.ac_floor))):

                    # instruction step (3) fill in amount in dollars in place of float(20)
                    shares_to_buy = math.floor(float(self.shares_to_buy_dollar) / float(r)-1)
                    self.buy(self.ticker, shares_to_buy)
                    print("bought:", r)
                    tempval = average_cost*num_shares
                    average_cost = tempval
                    average_cost += float(r)
                    num_shares += self.update_shares_buy
                    average_cost /= float(num_shares)
                    print("avg cost:" + str(average_cost))
            elif counter_one == 6: 
                if float(seep[0])*1.005 > float(r) and float(r) < float(average_cost-float(average_cost*float(self.ac_floor))):

                    # instruction step (3) fill in amount in dollars in place of float(20)
                    shares_to_buy = math.floor(float(self.shares_to_buy_dollar) / float(r)-1)
                    self.buy(self.ticker, shares_to_buy)
                    print("bought:", r)
                    tempval = average_cost*num_shares
                    average_cost = tempval
                    average_cost += float(r)
                    num_shares += self.update_shares_buy
                    average_cost /= float(num_shares)
                    print("avg cost:" + str(average_cost))
                    
            elif counter_one == 5:
                if float(seep[0])*1.0045 > float(r) and float(r) < float(average_cost-float(average_cost*float(self.ac_floor))):
                    
                    # instruction step (3) fill in amount in dollars in place of float(20)
                    shares_to_buy = math.floor(float(self.shares_to_buy_dollar) / float(r)-1)
                    self.buy(self.ticker, shares_to_buy)
                    print("bought:", r)
                    tempval = average_cost*num_shares
                    average_cost = tempval
                    average_cost += float(r)
                    num_shares += self.update_shares_buy
                    average_cost /= float(num_shares)
                    print("avg cost:" + str(average_cost))
                    
            elif counter_one == 4:
                if float(seep[0])*1.004 > float(r) and float(r) < float(average_cost-float(average_cost*float(self.ac_floor))):

                    # instruction step (3) fill in amount in dollars in place of float(20)
                    shares_to_buy = math.floor(float(self.shares_to_buy_dollar) / float(r)-1)
                    self.buy(self.ticker, shares_to_buy)
                    print("bought:", r)
                    tempval = average_cost*num_shares
                    average_cost = tempval
                    average_cost += float(r)
                    num_shares += self.update_shares_buy
                    average_cost /= float(num_shares)
                    print("avg cost:" + str(average_cost))
                    
            elif counter_one == 3:
                if float(seep[0])*1.0035 > float(r) and float(r) < float(average_cost-float(average_cost*float(self.ac_floor))):

                    # instruction step (3) fill in amount in dollars in place of float(20)
                    shares_to_buy = math.floor(float(self.shares_to_buy_dollar) / float(r)-1)
                    self.buy(self.ticker, shares_to_buy)
                    print("bought:", r)
                    tempval = average_cost*num_shares
                    average_cost = tempval
                    average_cost += float(r)
                    num_shares += self.update_shares_buy
                    average_cost /= float(num_shares)
                    print("avg cost:" + str(average_cost))
                    
            elif counter_one == 2:
                if float(seep[0])*1.003 > float(r) and float(r) < float(average_cost-float(average_cost*float(self.ac_floor))):

                    # instruction step (3) fill in amount in dollars in place of float(20)
                    shares_to_buy = math.floor(float(self.shares_to_buy_dollar) / float(r)-1)
                    self.buy(self.ticker, shares_to_buy)
                    print("bought:", r)
                    tempval = average_cost*num_shares
                    average_cost = tempval
                    average_cost += float(r)
                    num_shares += self.update_shares_buy
                    average_cost /= float(num_shares)
                    print("avg cost:" + str(average_cost))

        #BUY
        if counter_one >= 7:

            if float(r)*1.004 < float(seep[0]) and float(r) < float(average_cost-float(average_cost*float(self.ac_floor))):

                # instruction step (3) fill in amount in dollars in place of float(20)
                shares_to_buy = math.floor(float(self.shares_to_buy_dollar) / float(r)-1)
                self.buy(self.ticker, shares_to_buy)
                print("bought:", r)
                tempval = average_cost*num_shares
                average_cost = tempval
                average_cost += float(r)
                num_shares += self.update_shares_buy
                average_cost /= float(num_shares)
                print("avg cost:" + str(average_cost))
                
            elif float(r)*1.005 < float(seep[1]) and float(r) < float(average_cost-float(average_cost*float(self.ac_floor))):

                # instruction step (3) fill in amount in dollars in place of float(20)
                shares_to_buy = math.floor(float(self.shares_to_buy_dollar) / float(r)-1)
                self.buy(self.ticker, shares_to_buy)
                print("bought:", r)
                tempval = average_cost*num_shares
                average_cost = tempval
                average_cost += float(r)
                num_shares += self.update_shares_buy
                average_cost /= float(num_shares)
                print("avg cost:" + str(average_cost))
                
            elif float(r)*1.006 < float(seep[2]) and float(r) < float(average_cost-float(average_cost*float(self.ac_floor))):

                # instruction step (3) fill in amount in dollars in place of float(20)
                shares_to_buy = math.floor(float(self.shares_to_buy_dollar) / float(r)-1)
                self.buy(self.ticker, shares_to_buy)
                print("bought:", r)
                tempval = average_cost*num_shares
                average_cost = tempval
                average_cost += float(r)
                num_shares +=self.update_shares_buy
                average_cost /= float(num_shares)
                print("avg cost:" + str(average_cost))
                
            elif float(r)*1.007 < float(seep[3]) and float(r) < float(average_cost-float(average_cost*float(self.ac_floor))):

                # instruction step (3) fill in amount in dollars in place of float(20)
                shares_to_buy = math.floor(float(self.shares_to_buy_dollar) / float(r)-1)
                self.buy(self.ticker, shares_to_buy)
                print("bought:", r)
                tempval = average_cost*num_shares
                average_cost = tempval
                average_cost += float(r)
                num_shares += self.update_shares_buy
                average_cost /= float(num_shares)
                print("avg cost:" + str(average_cost))
                
            elif float(r)*1.008 < float(seep[4]) and float(r) < float(average_cost-float(average_cost*float(self.ac_floor))):

                # instruction step (3) fill in amount in dollars in place of float(20)
                shares_to_buy = math.floor(float(self.shares_to_buy_dollar) / float(r)-1)
                self.buy(self.ticker, shares_to_buy)
                print("bought:", r)
                tempval = average_cost*num_shares
                average_cost = tempval
                average_cost += float(r)
                num_shares += self.update_shares_buy
                average_cost /= float(num_shares)
                print("avg cost:" + str(average_cost))
                
            elif float(r)*1.01 < float(seep[5]) and float(r) < float(average_cost-float(average_cost*float(self.ac_floor))):

                # instruction step (3) fill in amount in dollars in place of float(20)
                shares_to_buy = math.floor(float(self.shares_to_buy_dollar) / float(r)-1)
                self.buy(self.ticker, shares_to_buy)
                print("bought:", r)
                tempval = average_cost*num_shares
                average_cost = tempval
                average_cost += float(r)
                num_shares += self.update_shares_buy
                average_cost /= float(num_shares)
                print("avg cost:" + str(average_cost))

            elif float(r)*1.013 < float(seep[6]) and float(r) < float(average_cost-float(average_cost*float(self.ac_floor))):

                # instruction step (3) fill in amount in dollars in place of float(20)
                shares_to_buy = math.floor(float(self.shares_to_buy_dollar) / float(r)-1)
                self.buy(self.ticker, shares_to_buy)
                print("bought:", r)
                tempval = average_cost*num_shares
                average_cost = tempval
                average_cost += float(r)
                num_shares += self.update_shares_buy
                average_cost /= float(num_shares)
                print("avg cost:" + str(average_cost))
                
        #SELL
        if counter_two < 7:

            if counter_two == 7:
                if float(seep[0])*1.01 < float(r) and float(r) > float(average_cost+float(average_cost*float(self.ac_ceiling))):

                    # instruction step (4) fill in amount in dollars in place of float(100)
                    shares_to_sell = math.floor(float(self.shares_to_sell_dollar) / float(r)+1)
                    self.sell(self.ticker, shares_to_sell)
                    print("sold:", r)
                    print("avg cost:", average_cost)
                    num_shares -= self.update_shares_sell

            elif counter_two == 6:
                if float(seep[0])*1.0075 < float(r) and float(r) > float(average_cost+float(average_cost*float(self.ac_ceiling))):

                    # instruction step (4) fill in amount in dollars in place of float(100)
                    shares_to_sell = math.floor(float(self.shares_to_sell_dollar) / float(r)+1)
                    self.sell(self.ticker, shares_to_sell)
                    print("sold:", r)
                    print("avg cost:", average_cost)
                    num_shares -= self.update_shares_sell
                    
            elif counter_two == 5:
                if float(seep[0])*1.0065 < float(r) and float(r) > float(average_cost+float(average_cost*float(self.ac_ceiling))):

                    # instruction step (4) fill in amount in dollars in place of float(100)
                    shares_to_sell = math.floor(float(self.shares_to_sell_dollar) / float(r)+1)
                    self.sell(self.ticker, shares_to_sell)
                    print("sold:", r)
                    print("avg cost:", average_cost)
                    num_shares -= self.update_shares_sell
                    
            elif counter_two == 4:
                if float(seep[0])*1.0055 < float(r) and float(r) > float(average_cost+float(average_cost*float(self.ac_ceiling))):

                    # instruction step (4) fill in amount in dollars in place of float(100)
                    shares_to_sell = math.floor(float(self.shares_to_sell_dollar) / float(r)+1)
                    self.sell(self.ticker, shares_to_sell)
                    print("sold:", r)
                    print("avg cost:", average_cost)
                    num_shares -= 2.0
                    
            elif counter_two == 3:
                if float(seep[0])*1.0045 < float(r) and float(r) > float(average_cost+float(average_cost*float(self.ac_ceiling))):

                    # instruction step (4) fill in amount in dollars in place of float(100)
                    shares_to_sell = math.floor(float(self.shares_to_sell_dollar) / float(r)+1)
                    self.sell(self.ticker, shares_to_sell)
                    print("sold:", r)
                    print("avg cost:", average_cost)
                    num_shares -= self.update_shares_sell
                    
            elif counter_two == 2:
                if float(seep[0])*1.0035 < float(r) and float(r) > float(average_cost+float(average_cost*float(self.ac_ceiling))):

                    # instruction step (4) fill in amount in dollars in place of float(100)
                    shares_to_sell = math.floor(float(self.shares_to_sell_dollar) / float(r)+1)
                    self.sell(self.ticker, shares_to_sell)
                    print("sold:", r)
                    print("avg cost:", average_cost)
                    num_shares -= self.update_shares_sell

        #SELL
        if counter_two >= 7:

            if float(r)*0.997 > float(seep[0]) and float(r) > float(average_cost+float(average_cost*float(self.ac_ceiling))):

                # instruction step (4) fill in amount in dollars in place of float(100)
                shares_to_sell = math.floor(float(self.shares_to_sell_dollar) / float(r)+1)
                self.sell(self.ticker, shares_to_sell)
                print("sold:", r)
                print("avg cost:", average_cost)
                num_shares -= self.update_shares_sell
            
            elif float(r)*0.996 > float(seep[1]) and float(r) > float(average_cost+float(average_cost*float(self.ac_ceiling))):

                # instruction step (4) fill in amount in dollars in place of float(100)
                shares_to_sell = math.floor(float(self.shares_to_sell_dollar) / float(r)+1)
                self.sell(self.ticker, shares_to_sell)
                print("sold:", r)
                print("avg cost:", average_cost)
                num_shares -= self.update_shares_sell
                
            elif float(r)*0.995 > float(seep[2]) and float(r) > float(average_cost+float(average_cost*float(self.ac_ceiling))):

                # instruction step (4) fill in amount in dollars in place of float(100)
                shares_to_sell = math.floor(float(self.shares_to_sell_dollar) / float(r)+1)
                self.sell(self.ticker, shares_to_sell)
                print("sold:", r)
                print("avg cost:", average_cost)
                num_shares -= self.update_shares_sell
                
            elif float(r)*0.993 > float(seep[3]) and float(r) > float(average_cost+float(average_cost*float(self.ac_ceiling))):

                # instruction step (4) fill in amount in dollars in place of float(100)
                shares_to_sell = math.floor(float(self.shares_to_sell_dollar) / float(r)+1)
                self.sell(self.ticker, shares_to_sell)
                print("sold:", r)
                print("avg cost:", average_cost)
                num_shares -= self.update_shares_sell
                
            elif float(r)*0.992 > float(seep[4]) and float(r) > float(average_cost+float(average_cost*float(self.ac_ceiling))):

                # instruction step (4) fill in amount in dollars in place of float(100)
                shares_to_sell = math.floor(float(self.shares_to_sell_dollar) / float(r)+1)
                self.sell(self.ticker, shares_to_sell)
                print("sold:", r)
                print("avg cost:", average_cost)
                num_shares -= self.update_shares_sell
                
            elif float(r)*0.991 > float(seep[5]) and float(r) > float(average_cost+float(average_cost*float(self.ac_ceiling))):

                # instruction step (4) fill in amount in dollars in place of float(100)
                shares_to_sell = math.floor(float(self.shares_to_sell_dollar) / float(r)+1)
                self.sell(self.ticker, shares_to_sell)
                print("sold:", r)
                print("avg cost:", average_cost)
                num_shares -= self.update_shares_sell
                
            elif float(r)*0.988 > float(seep[6]) and float(r) > float(average_cost+float(average_cost*float(self.ac_ceiling))):

                # instruction step (4) fill in amount in dollars in place of float(100)
                shares_to_sell = math.floor(float(self.shares_to_sell_dollar) / float(r)+1)
                self.sell(self.ticker, shares_to_sell)
                print("sold:", r)
                print("avg cost:", average_cost)
                num_shares -= self.update_shares_sell

        # Keeps track of counter
        print("c1:" + str(counter_one))
        print("c2:" + str(counter_two))
        counter_one += 1
        counter_two += 1

        return {
            "average_cost": average_cost,
            "num_shares": num_shares,
            "shares_to_buy_dollar": self.shares_to_buy_dollar,
            "shares_to_sell_dollar": self.shares_to_sell_dollar,
            "counter_one": counter_one,
            "counter_two": counter_two,
            "seep": seep,
        }
        
    # Functions to buy and sell crypto currency   
    def buy(ticker, amountD):
        r = robinhood.orders.order_buy_crypto_by_quantity(ticker, amountD)
        print(r)

    def sell(ticker, amountD):
        r = robinhood.orders.order_sell_crypto_by_quantity(ticker, amountD)
        print(r)