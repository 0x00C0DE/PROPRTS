import robin_stocks
import math
import pyotp
import sched
import time
import sys

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
#       3. Fill in Shares2Buy amount (in dollars $)
#       4. Fill in Shares2Sell amount (in dollars $)
#       5. Fill in num_shares 
#

# Some buying and selling errors will occur if a individual does not have enough shares to sell or enough money to buy.
# If errors occur, simply re-update through redoing instructions above and restart the program.


# Robinhood.login(username="example72", password="AnotherExample8")
totp = pyotp.TOTP("Sauce").now()
login = robin_stocks.login("email_here@service.com", "password_here")

# Scheduler created to run every 10 seconds
s = sched.scheduler(time.time, time.sleep)

# 10 second interval price history list, for every 1 minute
SE3P = []
Mazda = []


counter1 = 1.0
counter2 = 1.0

Shares2Sell = 0.00
shares2sellDollar = 6

# ratio of buy to sell 2:6 ≈ 1:3
updateSharesSell = 3


Shares2Buy = 0.00
shares2buyDollar = 2

# ratio of buy to sell 2:6 ≈ 1:3
updateSharesBuy = 1

# step (5)
# number of shares based on (total cost / Shares2Buy)
# EX: ($100 / 2) = 50
num_shares = 50
# step (2)
# average cost
average_cost = 0.833000

# average cost ceiling percentage (ensures there is a large enough disparity between the live price and the required minimal amount that is greater than the live price to obtain profitability when selling)
# average cost floor percentage(ensures there is a large enough disparity between the live price and the required minimal amount that is lower than the live price to obtain profitability when buying)
ac_ceiling = 0.02
ac_floor = 0.015

def run(sc):

    # crypto currency ticker available on robinhood
    ticker = "MATIC"

    global SE3P 
    global Mazda

    global ac_ceiling
    global ac_floor
    global updateSharesSell
    global updateSharesBuy
    
    global Shares2Sell
    global Shares2Buy
    global counter1
    global counter2
    global average_cost
    global num_shares
    
    r = robin_stocks.crypto.get_crypto_quote(ticker, info="mark_price")
    #r = robin_stocks.robinhood.get_latest_price(ticker)
    print(ticker + ": $" + str(r))

    SE3P.append(r)

    if len(SE3P) > 6:

        # if there are 5 or more elements in the list, rearrange positions
        Mazda = SE3P[1:7]
        SE3P = SE3P[-1:]

        SE3P = Mazda + SE3P
        print("Cleared and repositioned")

    if len(SE3P) == 1:
        #0sec
        print("appended SE3P[0]")
        print(SE3P)
    elif len(SE3P) == 2:
        #SE3P.append(r) #10sec
        print("appended SE3P[1]")
        print(SE3P)
    elif len(SE3P) == 3:
        #SE3P.append(r) #20sec
        print("appended SE3P[2]")
        print(SE3P)
    elif len(SE3P) == 4:
        #SE3P.append(r) #30sec
        print("appended SE3P[3]")
        print(SE3P)
    elif len(SE3P) == 5:
        #SE3P.append(r) #40sec
        print("appended SE3P[4]")
        print(SE3P)
    elif len(SE3P) == 6:
        #SE3P.append(r) #50sec
        print("appended SE3P[5]")
        print(SE3P)
    elif len(SE3P) == 7:
        #SE3P.append(r) #60sec/1min
        print("appended SE3P[6]")
        print(SE3P)

    # BUY
    if counter1 < 7:

       if counter1 == 7: 
        if float(SE3P[0])*1.006 > float(r) and float(r) < float(average_cost-float(average_cost*float(ac_floor))):

                # instruction step (3) fill in amount in dollars in place of float(20)
                Shares2Buy = math.floor(float(shares2buyDollar) / float(r)-1)
                crypto_BUY(ticker, Shares2Buy)
                print("bought:", r)
                tempval = average_cost*num_shares
                average_cost = tempval
                average_cost += float(r)
                num_shares += updateSharesBuy
                average_cost /= float(num_shares)
                print("avg cost:" + str(average_cost))
        elif counter1 == 6: 
            if float(SE3P[0])*1.005 > float(r) and float(r) < float(average_cost-float(average_cost*float(ac_floor))):

                # instruction step (3) fill in amount in dollars in place of float(20)
                Shares2Buy = math.floor(float(shares2buyDollar) / float(r)-1)
                crypto_BUY(ticker, Shares2Buy)
                print("bought:", r)
                tempval = average_cost*num_shares
                average_cost = tempval
                average_cost += float(r)
                num_shares += updateSharesBuy
                average_cost /= float(num_shares)
                print("avg cost:" + str(average_cost))
                
        elif counter1 == 5:
            if float(SE3P[0])*1.0045 > float(r) and float(r) < float(average_cost-float(average_cost*float(ac_floor))):
                
                # instruction step (3) fill in amount in dollars in place of float(20)
                Shares2Buy = math.floor(float(shares2buyDollar) / float(r)-1)
                crypto_BUY(ticker, Shares2Buy)
                print("bought:", r)
                tempval = average_cost*num_shares
                average_cost = tempval
                average_cost += float(r)
                num_shares += updateSharesBuy
                average_cost /= float(num_shares)
                print("avg cost:" + str(average_cost))
                
        elif counter1 == 4:
            if float(SE3P[0])*1.004 > float(r) and float(r) < float(average_cost-float(average_cost*float(ac_floor))):

                # instruction step (3) fill in amount in dollars in place of float(20)
                Shares2Buy = math.floor(float(shares2buyDollar) / float(r)-1)
                crypto_BUY(ticker, Shares2Buy)
                print("bought:", r)
                tempval = average_cost*num_shares
                average_cost = tempval
                average_cost += float(r)
                num_shares += updateSharesBuy
                average_cost /= float(num_shares)
                print("avg cost:" + str(average_cost))
                
        elif counter1 == 3:
            if float(SE3P[0])*1.0035 > float(r) and float(r) < float(average_cost-float(average_cost*float(ac_floor))):

                # instruction step (3) fill in amount in dollars in place of float(20)
                Shares2Buy = math.floor(float(shares2buyDollar) / float(r)-1)
                crypto_BUY(ticker, Shares2Buy)
                print("bought:", r)
                tempval = average_cost*num_shares
                average_cost = tempval
                average_cost += float(r)
                num_shares += updateSharesBuy
                average_cost /= float(num_shares)
                print("avg cost:" + str(average_cost))
                
        elif counter1 == 2:
            if float(SE3P[0])*1.003 > float(r) and float(r) < float(average_cost-float(average_cost*float(ac_floor))):

                # instruction step (3) fill in amount in dollars in place of float(20)
                Shares2Buy = math.floor(float(shares2buyDollar) / float(r)-1)
                crypto_BUY(ticker, Shares2Buy)
                print("bought:", r)
                tempval = average_cost*num_shares
                average_cost = tempval
                average_cost += float(r)
                num_shares += updateSharesBuy
                average_cost /= float(num_shares)
                print("avg cost:" + str(average_cost))

    #BUY
    if counter1 >= 7:

        if float(r)*1.004 < float(SE3P[0]) and float(r) < float(average_cost-float(average_cost*float(ac_floor))):

            # instruction step (3) fill in amount in dollars in place of float(20)
            Shares2Buy = math.floor(float(shares2buyDollar) / float(r)-1)
            crypto_BUY(ticker, Shares2Buy)
            print("bought:", r)
            tempval = average_cost*num_shares
            average_cost = tempval
            average_cost += float(r)
            num_shares += updateSharesBuy
            average_cost /= float(num_shares)
            print("avg cost:" + str(average_cost))
            
        elif float(r)*1.005 < float(SE3P[1]) and float(r) < float(average_cost-float(average_cost*float(ac_floor))):

            # instruction step (3) fill in amount in dollars in place of float(20)
            Shares2Buy = math.floor(float(shares2buyDollar) / float(r)-1)
            crypto_BUY(ticker, Shares2Buy)
            print("bought:", r)
            tempval = average_cost*num_shares
            average_cost = tempval
            average_cost += float(r)
            num_shares += updateSharesBuy
            average_cost /= float(num_shares)
            print("avg cost:" + str(average_cost))
            
        elif float(r)*1.006 < float(SE3P[2]) and float(r) < float(average_cost-float(average_cost*float(ac_floor))):

            # instruction step (3) fill in amount in dollars in place of float(20)
            Shares2Buy = math.floor(float(shares2buyDollar) / float(r)-1)
            crypto_BUY(ticker, Shares2Buy)
            print("bought:", r)
            tempval = average_cost*num_shares
            average_cost = tempval
            average_cost += float(r)
            num_shares += updateSharesBuy
            average_cost /= float(num_shares)
            print("avg cost:" + str(average_cost))
            
        elif float(r)*1.007 < float(SE3P[3]) and float(r) < float(average_cost-float(average_cost*float(ac_floor))):

            # instruction step (3) fill in amount in dollars in place of float(20)
            Shares2Buy = math.floor(float(shares2buyDollar) / float(r)-1)
            crypto_BUY(ticker, Shares2Buy)
            print("bought:", r)
            tempval = average_cost*num_shares
            average_cost = tempval
            average_cost += float(r)
            num_shares += updateSharesBuy
            average_cost /= float(num_shares)
            print("avg cost:" + str(average_cost))
            
        elif float(r)*1.008 < float(SE3P[4]) and float(r) < float(average_cost-float(average_cost*float(ac_floor))):

            # instruction step (3) fill in amount in dollars in place of float(20)
            Shares2Buy = math.floor(float(shares2buyDollar) / float(r)-1)
            crypto_BUY(ticker, Shares2Buy)
            print("bought:", r)
            tempval = average_cost*num_shares
            average_cost = tempval
            average_cost += float(r)
            num_shares += updateSharesBuy
            average_cost /= float(num_shares)
            print("avg cost:" + str(average_cost))
            
        elif float(r)*1.01 < float(SE3P[5]) and float(r) < float(average_cost-float(average_cost*float(ac_floor))):

            # instruction step (3) fill in amount in dollars in place of float(20)
            Shares2Buy = math.floor(float(shares2buyDollar) / float(r)-1)
            crypto_BUY(ticker, Shares2Buy)
            print("bought:", r)
            tempval = average_cost*num_shares
            average_cost = tempval
            average_cost += float(r)
            num_shares += updateSharesBuy
            average_cost /= float(num_shares)
            print("avg cost:" + str(average_cost))

        elif float(r)*1.013 < float(SE3P[6]) and float(r) < float(average_cost-float(average_cost*float(ac_floor))):

            # instruction step (3) fill in amount in dollars in place of float(20)
            Shares2Buy = math.floor(float(shares2buyDollar) / float(r)-1)
            crypto_BUY(ticker, Shares2Buy)
            print("bought:", r)
            tempval = average_cost*num_shares
            average_cost = tempval
            average_cost += float(r)
            num_shares += updateSharesBuy
            average_cost /= float(num_shares)
            print("avg cost:" + str(average_cost))
            
    #SELL
    if counter2 < 7:

        if counter2 == 7:
            if float(SE3P[0])*1.01 < float(r) and float(r) > float(average_cost+float(average_cost*float(ac_ceiling))):

                # instruction step (4) fill in amount in dollars in place of float(100)
                Shares2Sell = math.floor(float(shares2sellDollar) / float(r)+1)
                crypto_SELL(ticker, Shares2Sell)
                print("sold:", r)
                print("avg cost:", average_cost)
                num_shares -= updateSharesSell

        elif counter2 == 6:
            if float(SE3P[0])*1.0075 < float(r) and float(r) > float(average_cost+float(average_cost*float(ac_ceiling))):

                # instruction step (4) fill in amount in dollars in place of float(100)
                Shares2Sell = math.floor(float(shares2sellDollar) / float(r)+1)
                crypto_SELL(ticker, Shares2Sell)
                print("sold:", r)
                print("avg cost:", average_cost)
                num_shares -= updateSharesSell
                
        elif counter2 == 5:
            if float(SE3P[0])*1.0065 < float(r) and float(r) > float(average_cost+float(average_cost*float(ac_ceiling))):

                # instruction step (4) fill in amount in dollars in place of float(100)
                Shares2Sell = math.floor(float(shares2sellDollar) / float(r)+1)
                crypto_SELL(ticker, Shares2Sell)
                print("sold:", r)
                print("avg cost:", average_cost)
                num_shares -= updateSharesSell
                
        elif counter2 == 4:
            if float(SE3P[0])*1.0055 < float(r) and float(r) > float(average_cost+float(average_cost*float(ac_ceiling))):

                # instruction step (4) fill in amount in dollars in place of float(100)
                Shares2Sell = math.floor(float(shares2sellDollar) / float(r)+1)
                crypto_SELL(ticker, Shares2Sell)
                print("sold:", r)
                print("avg cost:", average_cost)
                num_shares -= 2.0
                
        elif counter2 == 3:
            if float(SE3P[0])*1.0045 < float(r) and float(r) > float(average_cost+float(average_cost*float(ac_ceiling))):

                # instruction step (4) fill in amount in dollars in place of float(100)
                Shares2Sell = math.floor(float(shares2sellDollar) / float(r)+1)
                crypto_SELL(ticker, Shares2Sell)
                print("sold:", r)
                print("avg cost:", average_cost)
                num_shares -= updateSharesSell
                
        elif counter2 == 2:
            if float(SE3P[0])*1.0035 < float(r) and float(r) > float(average_cost+float(average_cost*float(ac_ceiling))):

                # instruction step (4) fill in amount in dollars in place of float(100)
                Shares2Sell = math.floor(float(shares2sellDollar) / float(r)+1)
                crypto_SELL(ticker, Shares2Sell)
                print("sold:", r)
                print("avg cost:", average_cost)
                num_shares -= updateSharesSell

    #SELL
    if counter2 >= 7:

        if float(r)*0.997 > float(SE3P[0]) and float(r) > float(average_cost+float(average_cost*float(ac_ceiling))):

            # instruction step (4) fill in amount in dollars in place of float(100)
            Shares2Sell = math.floor(float(shares2sellDollar) / float(r)+1)
            crypto_SELL(ticker, Shares2Sell)
            print("sold:", r)
            print("avg cost:", average_cost)
            num_shares -= updateSharesSell
        
        elif float(r)*0.996 > float(SE3P[1]) and float(r) > float(average_cost+float(average_cost*float(ac_ceiling))):

            # instruction step (4) fill in amount in dollars in place of float(100)
            Shares2Sell = math.floor(float(shares2sellDollar) / float(r)+1)
            crypto_SELL(ticker, Shares2Sell)
            print("sold:", r)
            print("avg cost:", average_cost)
            num_shares -= updateSharesSell
            
        elif float(r)*0.995 > float(SE3P[2]) and float(r) > float(average_cost+float(average_cost*float(ac_ceiling))):

            # instruction step (4) fill in amount in dollars in place of float(100)
            Shares2Sell = math.floor(float(shares2sellDollar) / float(r)+1)
            crypto_SELL(ticker, Shares2Sell)
            print("sold:", r)
            print("avg cost:", average_cost)
            num_shares -= updateSharesSell
            
        elif float(r)*0.993 > float(SE3P[3]) and float(r) > float(average_cost+float(average_cost*float(ac_ceiling))):

            # instruction step (4) fill in amount in dollars in place of float(100)
            Shares2Sell = math.floor(float(shares2sellDollar) / float(r)+1)
            crypto_SELL(ticker, Shares2Sell)
            print("sold:", r)
            print("avg cost:", average_cost)
            num_shares -= updateSharesSell
            
        elif float(r)*0.992 > float(SE3P[4]) and float(r) > float(average_cost+float(average_cost*float(ac_ceiling))):

            # instruction step (4) fill in amount in dollars in place of float(100)
            Shares2Sell = math.floor(float(shares2sellDollar) / float(r)+1)
            crypto_SELL(ticker, Shares2Sell)
            print("sold:", r)
            print("avg cost:", average_cost)
            num_shares -= updateSharesSell
            
        elif float(r)*0.991 > float(SE3P[5]) and float(r) > float(average_cost+float(average_cost*float(ac_ceiling))):

            # instruction step (4) fill in amount in dollars in place of float(100)
            Shares2Sell = math.floor(float(shares2sellDollar) / float(r)+1)
            crypto_SELL(ticker, Shares2Sell)
            print("sold:", r)
            print("avg cost:", average_cost)
            num_shares -= updateSharesSell
            
        elif float(r)*0.988 > float(SE3P[6]) and float(r) > float(average_cost+float(average_cost*float(ac_ceiling))):

            # instruction step (4) fill in amount in dollars in place of float(100)
            Shares2Sell = math.floor(float(shares2sellDollar) / float(r)+1)
            crypto_SELL(ticker, Shares2Sell)
            print("sold:", r)
            print("avg cost:", average_cost)
            num_shares -= updateSharesSell

    # Keeps track of counter
    print("c1:" + str(counter1))
    print("c2:" + str(counter2))
    counter1 += 1
    counter2 += 1
    
    # calls scheduler every 10 seconds
    s.enter(10, 1, run, (sc,))

# Functions to buy and sell crypto currency   
def crypto_BUY(ticker, amountD):
    r = robin_stocks.orders.order_buy_crypto_by_quantity(ticker, amountD)
    print(r)

def crypto_SELL(ticker, amountD):
    r = robin_stocks.orders.order_sell_crypto_by_quantity(ticker, amountD)
    print(r)

s.enter(1, 1, run, (s,))
s.run()
