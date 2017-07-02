import pygame, random, math, os
from market import *

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
    

print(plumbus_inc.inventory.quantity(shleem))

plumbus_inc.buy(shleem, 3)

print(plumbus_inc.account.contents)

print(plumbus_inc.inventory.quantity(shleem))

plumbus_inc.sell(shleem, 2)
print(plumbus_inc.account.contents)


print(plumbus_inc.inventory.quantity(shleem))

print(plumbus_inc.inventory.quantity(plumbus))

plumbus_inc.produce(2)

print(plumbus_inc.inventory.quantity(plumbus))

plumbus_inc.sell(plumbus, 3)

print(plumbus_inc.account.contents)

