import robin_stocks
import pyotp
import datetime

totp = pyotp.TOTP("Sauce").now()
login = robin_stocks.login("email_here@test.com", "password_here")

y = []
x = []

cryptoPrice = 0

# crypto currency ticker available on robinhood
ticker = "MATIC"

cryptoSymbol = robin_stocks.crypto.get_crypto_quote(ticker, info="mark_price")
cryptoPrice = float(cryptoSymbol)
print(ticker + ": $" + str(cryptoSymbol))


dt = datetime.now()
ts = datetime.timestamp(dt)
x.append(ts)
y.append(cryptoPrice)

filename = "PROPRTS-1-data.txt"

# Read all lines from the file
with open(filename, 'r') as f:
    lines = f.readlines()
    #print("read lines: ", lines)

# If number of lines exceeds 96, remove the oldest lines
if len(lines) > 96:
    lines = lines[-96:]
    #print("removed lines: ", lines)

# Open file in write mode and write modified lines
with open(filename, 'w') as f:
    f.writelines(lines)
    #print("write lines: ", lines)

# Append new data to file if it doesn't already have 96 entries
if len(lines) < 97:
    with open(filename, 'a') as f:
        coordinate = list(zip(x, y))
        final_coord = ''.join(str(z) for z in coordinate)
        f.write(final_coord)
        f.write("\n")
        #print("append lines: ", final_coord)
