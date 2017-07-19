""" Testing file """

# Used to test the objects and functions of economy.py

import pygame, random, math, os
from economy import *

initialize()

dinglebop = Resource("Dinglebop", 2)
shleem = Resource("Shleem", 0.5)
fleeb = Resource("Fleeb", 3)

plumbus = Product("Plumbus", 6.5, {dinglebop: 1, shleem: 5, fleeb: 1})

plumbus_inc = Firm("Plumbus Inc.", plumbus)
plumbus_and_accessories = Firm("Plumbus and Plumbus Accessories", plumbus)
plumbuses_galore = Firm("Plumbuses Galore", plumbus)


# Testing
for firm in plumbus.market.firms:
    print(firm.name)
    

print(plumbus_inc.inventory.getQuantity(shleem))

plumbus_inc.buy(shleem, 3)

print(plumbus_inc.account.contents)

print(plumbus_inc.inventory.getQuantity(shleem))

plumbus_inc.sell(shleem, 2)
print(plumbus_inc.account.contents)


print(plumbus_inc.inventory.getQuantity(shleem))

print(plumbus_inc.inventory.getQuantity(plumbus))

plumbus_inc.produce(20)

print(plumbus_inc.inventory.getQuantity(plumbus))

plumbus_inc.sell(plumbus, 3)

print(plumbus_inc.account.contents)

print(plumbus_inc.inventory.getQuantity(plumbus))

plumbus_inc.sellProduct()
print(plumbus_inc.inventory.getQuantity(plumbus))
print(plumbus_inc.account.contents)


plumbus_inc.sellProduct()
print(plumbus_inc.inventory.getQuantity(plumbus))
print(plumbus_inc.account.contents)

plumbus_inc.determineDemand()

plumbus_inc.sellProduct()
print(plumbus_inc.inventory.getQuantity(plumbus))
print(plumbus_inc.account.contents)