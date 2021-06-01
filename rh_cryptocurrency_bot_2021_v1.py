import robin_stocks
import math
import pyotp
import sched
import time
import sys

# Program description:
# A Robinhood bot created to automatically monitor and trade crypto currency currently supported by Robinhood.
# Works with all crypto currencies supported by Robinhood except for DOGE.
#
# This bot runs a scheduler every 5 minutes in order to update the prices on a 5 minute interval for a 
# list that will hold the previous prices for 30 minutes.
# 
# This bot [REQUIRES] a individual to already have SET amount of shares of the current crypto they want to trade.
# 
#   Instructions after entering in login information (no particular order):
#
#       1. Fill in ticker
#       2. Fill in average_cost
#       3. Fill in Shares2Buy amount (in dollars $)
#       4. Fill in Shares2Sell amount (in dollars $)
#       5. Fill in num_shares 
#

# Some buying and selling errors will occur if a individual does not have enough shares to sell or enough money to buy.
# If errors occur, simply re-update through redoing instructions above and restart the program.


# Robin_stocks.login("example72", "AnotherExample8")
# where "example72" is the username and "AnotherExample8" is the password
totp = pyotp.TOTP("Sauce").now()
login = robin_stocks.login("", "")

# Scheduler created to run every 5 mins
s = sched.scheduler(time.time, time.sleep)

# 5 min interval price history list, for every 30 minutes
SE3P = []
Mazda = []


counter1 = 1.0
counter2 = 1.0

# note if you change the shares2Sell you must also update the num_shares when selling because it's current set
# to update as (num_shares -= 6.0) below at the bottom in the sell section, when selling since 120/20 = 6.
# step (4)
Shares2Sell = 120

# note if you change the shares2buy you must also update the num_shares accordingly, because
# it's currently set to update as (num_shares += 1) below in the buy section.
# step (3)
Shares2Buy = 20


# step (5)
# number of shares based on (total cost / Shares2Buy)
# EX: ($2940 / $20) = 147
num_shares = 147.00

# step (2)
# average cost
average_cost = 913.00


def run(sc):

    # step (1)
    # crypto currency ticker available on robinhood
    ticker = "BCH"

    global SE3P 
    global Mazda
    
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
        Mazda = SE3P[1:6]
        SE3P = SE3P[-1:]

        SE3P = Mazda + SE3P
        print("Cleared and repositioned")

    if len(SE3P) == 1:
        #0min
        print("appended SE3P[0]")
        print(SE3P)
    elif len(SE3P) == 2:
        #SE3P.append(r) #5min
        print("appended SE3P[1]")
        print(SE3P)
    elif len(SE3P) == 3:
        #SE3P.append(r) #10min
        print("appended SE3P[2]")
        print(SE3P)
    elif len(SE3P) == 4:
        #SE3P.append(r) #15min
        print("appended SE3P[3]")
        print(SE3P)
    elif len(SE3P) == 5:
        #SE3P.append(r) #20min
        print("appended SE3P[4]")
        print(SE3P)
    elif len(SE3P) == 6:
        #SE3P.append(r) #25min
        print("appended SE3P[5]")
        print(SE3P)

    # BUY
    # if it's been less than 30 minutes since the start of the program
    if counter1 < 6:

        # For each 5 minutes, compare the inital price at the start of the program to the current price.
        # Each 5 minutes passed, checks if difference is larger than a manually set percentage, progressively increasing the difference boundary.
        # If the initial starting price when the program started multiplied by a set percentage, is greater than the current price AND
        # the current price is lower than the average cost minus a set percentage, then buy Shares2Buy amount in dollars.
        # If Bought, updates the average_cost and num_shares.
        
        if counter1 == 6: 
            if float(SE3P[0])*1.005 > float(r) and float(r) < float(average_cost-float(average_cost*float(0.015))):
                crypto_BUY(ticker, Shares2Buy)
                print("bought:", r)
                tempval = average_cost*num_shares
                average_cost = tempval
                average_cost += float(r)
                num_shares += 1
                average_cost /= float(num_shares)
                print("avg cost:" + str(average_cost))
        elif counter1 == 5:
            if float(SE3P[0])*1.0045 > float(r) and float(r) < float(average_cost-float(average_cost*float(0.015))):
                crypto_BUY(ticker, Shares2Buy)
                print("bought:", r)
                tempval = average_cost*num_shares
                average_cost = tempval
                average_cost += float(r)
                num_shares += 1
                average_cost /= float(num_shares)
                print("avg cost:" + str(average_cost))
        elif counter1 == 4:
            if float(SE3P[0])*1.004 > float(r) and float(r) < float(average_cost-float(average_cost*float(0.015))):
                crypto_BUY(ticker, Shares2Buy)
                print("bought:", r)
                tempval = average_cost*num_shares
                average_cost = tempval
                average_cost += float(r)
                num_shares += 1
                average_cost /= float(num_shares)
                print("avg cost:" + str(average_cost))
        elif counter1 == 3:
            if float(SE3P[0])*1.0035 > float(r) and float(r) < float(average_cost-float(average_cost*float(0.015))):
                crypto_BUY(ticker, Shares2Buy)
                print("bought:", r)
                tempval = average_cost*num_shares
                average_cost = tempval
                average_cost += float(r)
                num_shares += 1
                average_cost /= float(num_shares)
                print("avg cost:" + str(average_cost))
        elif counter1 == 2:
            if float(SE3P[0])*1.003 > float(r) and float(r) < float(average_cost-float(average_cost*float(0.015))):
                crypto_BUY(ticker, Shares2Buy)
                print("bought:", r)
                tempval = average_cost*num_shares
                average_cost = tempval
                average_cost += float(r)
                num_shares += 1
                average_cost /= float(num_shares)
                print("avg cost:" + str(average_cost))
    #BUY
    # if first price is < than 2nd
    # if it has been 30 minutes or more since the start of the program
    if counter1 >= 6:


        # For each 5 minutes, compare the current price to each index of the list in order starting with [1]-[5] since the current price would be [0].
        # Each 5 minutes passed, checks if difference is larger than a manually set percentage, progressively increasing the difference boundary.
        # If the current price multiplied by a set percentage, is less than one of the indices AND
        # the current price is lower than the average cost minus a set percentage, then buy Shares2Buy amount in dollars.
        # If Bought, updates the average_cost and num_shares.
        
        if float(r)*1.005 < float(SE3P[1]) and float(r) < float(average_cost-float(average_cost*float(0.015))):

            crypto_BUY(ticker, Shares2Buy)
            print("bought:", r)
            tempval = average_cost*num_shares
            average_cost = tempval
            average_cost += float(r)
            num_shares += 1
            average_cost /= float(num_shares)
            print("avg cost:" + str(average_cost))
        if float(r)*1.006 < float(SE3P[2]) and float(r) < float(average_cost-float(average_cost*float(0.015))):
            crypto_BUY(ticker, Shares2Buy)
            print("bought:", r)
            tempval = average_cost*num_shares
            average_cost = tempval
            average_cost += float(r)
            num_shares += 1
            average_cost /= float(num_shares)
            print("avg cost:" + str(average_cost))
        if float(r)*1.007 < float(SE3P[3]) and float(r) < float(average_cost-float(average_cost*float(0.015))):
            crypto_BUY(ticker, Shares2Buy)
            print("bought:", r)
            tempval = average_cost*num_shares
            average_cost = tempval
            average_cost += float(r)
            num_shares += 1
            average_cost /= float(num_shares)
            print("avg cost:" + str(average_cost))
        if float(r)*1.008 < float(SE3P[4]) and float(r) < float(average_cost-float(average_cost*float(0.015))):
            crypto_BUY(ticker, Shares2Buy)
            print("bought:", r)
            tempval = average_cost*num_shares
            average_cost = tempval
            average_cost += float(r)
            num_shares += 1
            average_cost /= float(num_shares)
            print("avg cost:" + str(average_cost))
        if float(r)*1.01 < float(SE3P[5]) and float(r) < float(average_cost-float(average_cost*float(0.015))):
            crypto_BUY(ticker, Shares2Buy)
            print("bought:", r)
            tempval = average_cost*num_shares
            average_cost = tempval
            average_cost += float(r)
            num_shares += 1
            average_cost /= float(num_shares)
            print("avg cost:" + str(average_cost))
    #SELL
    # if it's been less than 30 minutes since the start of the program
    if counter2 < 6:

        # For each 5 minutes, compare the inital price at the start of the program to the current price.
        # Each 5 minutes passed, checks if difference is larger than a manually set percentage, progressively increasing the difference boundary.
        # If the initial starting price when the program started multiplied by a set percentage, is less than the current price AND
        # the current price is greater than the average cost plus a set percentage, then sell Shares2Sell amount in dollars.
        # If Sold, updates the average_cost and num_shares.
        
        if counter2 == 6:
            if float(SE3P[0])*1.0115 < float(r) and float(r) > float(average_cost+float(average_cost*float(0.04))):
                crypto_SELL(ticker, Shares2Sell)
                print("sold:", r)
                print("avg cost:", average_cost)
                num_shares -= 6.0
        elif counter2 == 5:
            if float(SE3P[0])*1.0105 < float(r) and float(r) > float(average_cost+float(average_cost*float(0.04))):
                crypto_SELL(ticker, Shares2Sell)
                print("sold:", r)
                print("avg cost:", average_cost)
                num_shares -= 6.0
        elif counter2 == 4:
            if float(SE3P[0])*1.0095 < float(r) and float(r) > float(average_cost+float(average_cost*float(0.04))):
                crypto_SELL(ticker, Shares2Sell)
                print("sold:", r)
                print("avg cost:", average_cost)
                num_shares -= 6.0
        elif counter2 == 3:
            if float(SE3P[0])*1.0085 < float(r) and float(r) > float(average_cost+float(average_cost*float(0.04))):
                crypto_SELL(ticker, Shares2Sell)
                print("sold:", r)
                print("avg cost:", average_cost)
                num_shares -= 6.0
        elif counter2 == 2:
            if float(SE3P[0])*1.0075 < float(r) and float(r) > float(average_cost+float(average_cost*float(0.04))):
                crypto_SELL(ticker, Shares2Sell)
                print("sold:", r)
                print("avg cost:", average_cost)
                num_shares -= 6.0


    #SELL
    # if it has been 30 minutes or more since the start of the program
    if counter2 >= 6:

        # For each 5 minutes, compare the current price to each index of the list in order starting with [1]-[5] since the current price would be [0].
        # Each 5 minutes passed, checks if difference is larger than a manually set percentage, progressively increasing the difference boundary.
        # If the current price multiplied by a set percentage, is greater than one of the indices AND
        # the current price is greater than the average cost plus a set percentage, then sell Shares2Sell amount in dollars.
        # If Sold, updates the average_cost and num_shares.
        
        if float(r)*0.995 > float(SE3P[1]) and float(r) > float(average_cost+float(average_cost*float(0.04))):
            crypto_SELL(ticker, Shares2Sell)
            print("sold:", r)
            print("avg cost:", average_cost)
            num_shares -= 6.0
        if float(r)*0.993 > float(SE3P[2]) and float(r) > float(average_cost+float(average_cost*float(0.04))):
            crypto_SELL(ticker, Shares2Sell)
            print("sold:", r)
            print("avg cost:", average_cost)
            num_shares -= 6.0
        if float(r)*0.991 > float(SE3P[3]) and float(r) > float(average_cost+float(average_cost*float(0.04))):
            crypto_SELL(ticker, Shares2Sell)
            print("sold:", r)
            print("avg cost:", average_cost)
            num_shares -= 6.0
        if float(r)*0.989 > float(SE3P[4]) and float(r) > float(average_cost+float(average_cost*float(0.04))):
            crypto_SELL(ticker, Shares2Sell)
            print("sold:", r)
            print("avg cost:", average_cost)
            num_shares -= 6.0
        if float(r)*0.987 > float(SE3P[5]) and float(r) > float(average_cost+float(average_cost*float(0.04))):
            crypto_SELL(ticker, Shares2Sell)
            print("sold:", r)
            print("avg cost:", average_cost)
            num_shares -= 6.0

    # Keeps track of counter
    print("c1:" + str(counter1))
    print("c2:" + str(counter2))
    counter1 += 1
    counter2 += 1
    
    # calls scheduler every 5 minutes
    s.enter(300, 1, run, (sc,))

# Functions to buy and sell crypto currency   
def crypto_BUY(ticker, amountD):
    r = robin_stocks.orders.order_buy_crypto_by_price(ticker, amountD)
    print(r)

def crypto_SELL(ticker, amountD):
    r = robin_stocks.orders.order_sell_crypto_by_price(ticker, amountD)
    print(r)

s.enter(1, 1, run, (s,))
s.run()
