import robin_stocks
import pyotp
import datetime
import sys
import os

class dataWriter:
    totp = pyotp.TOTP("Sauce").now()
    login = robin_stocks.login("email_here@test.com", "password_here")
    y = []
    x = []
    cryptoPrice = 0
    # crypto currency ticker available on robinhood
    ticker = "MATIC"

    def wCryptoData(self):
        cryptoSymbol = robin_stocks.crypto.get_crypto_quote(self.ticker, info="mark_price")
        self.cryptoPrice = float(cryptoSymbol)
        print(self.ticker + ": $" + str(cryptoSymbol))
    
        dt = datetime.datetime.now()
        ts = datetime.datetime.timestamp(dt)
        self.x.append(ts)
        self.y.append(self.cryptoPrice)

        filename = sys.argv[2]

        # Read all lines from the file
        with open(filename, 'r') as f:
            lines = f.readlines()
            print("read lines: ", lines)

        # If number of lines exceeds 96, remove the oldest lines
        if len(lines) > 96:
            lines = lines[-96:]
            print("removed lines: ", lines)

        # Open file in write mode and write modified lines
        with open(filename, 'w') as f:
            f.writelines(lines)
            print("write lines: ", lines)

        # Append new data to file if it doesn't already have 96 entries
        if len(lines) < 97:
            with open(filename, 'a') as f:
                coordinate = list(zip(self.x, self.y))
                final_coord = ''.join(str(z) for z in coordinate)
                f.write(final_coord)
                f.write("\n")
                print("append lines: ", final_coord)


if len(sys.argv) == 1:
    print("[ERROR]")
    print("not enough args.lol")
else:
    cwd = os.getcwd()
    files = [i for i in os.listdir(cwd) if i.endswith(".txt")]
    if len(files) == 1:
        test = dataWriter()
        test.wCryptoData()
        #print(files)
    else:
        print("There are no data files to load [ERROR]")

