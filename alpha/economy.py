""" Economic classes, objects, functions """
###   Todo   ###

###   ---    ###
def initialize():
    global economy
    economy = Economy()

class Economy(object):
    
    def __init__(self):
        self.products = []
        self.resources = []
        self.fops = []
        self.markets = []

class Market(object):
    
    def __init__(self, product):
        economy.markets.append(self)
        self.product = product
        self.firms = []
        self.size = 100 # Number of customers, should be based off size of town
    
    def addFirm(self, firm):
        self.firms.append(firm)
     
class Firm(object):
    
    def __init__(self, name, product):
        self.name = name
        self.product = product
        self.market = product.market
        self.market.addFirm(self)
        self.account = Account()
        self.inventory = Inventory(self.product)
    
    def buy(self, item, quantity):
        self.inventory.contents[item][0] += quantity
        self.account.debit(item.price * quantity)
        
    def sell(self, item, quantity):
        self.inventory.contents[item][0] -= quantity
        self.account.credit(item.price * quantity)
    
    def produce(self, quantity):
        self.inventory.contents[self.product][0] += quantity
        for resource in self.product.recipe:
            self.inventory.contents[resource][0] -= self.product.recipe[resource] * quantity
            
    def sellProduct(self):
        quantity = self.product.quantity_demanded
        self.sell(self.product, quantity)
        
     # Calculates demand based on market factors
    def determineDemand(self):
        # Determinants
        number_of_firms = len(self.product.market.firms)
        quality = self.inventory.getLevel(self.product)
        market_size = self.product.market.size
        slope = 2
        demand = market_size - (self.product.price * slope) + quality * (market_size/10)
        demand = demand/number_of_firms
        self.product.quantity_demanded = int(demand)

class Inventory(object):
    
    def __init__(self, product):
        self.items = []
        self.contents = {}
        self.items.append(product)
        for resource in economy.resources:
            self.items.append(resource)
        for fop in economy.fops:
            self.items.append(fop)
        for item in self.items:
            self.contents[item] = [0,0] # [quantity, level]
            
    def getQuantity(self, item):
        return self.contents[item][0]
    
    def getLevel(self, item):
        return self.contents[item][1]
        
class Account(object):
    
    def __init__(self):
        self.contents = 0
    
    def credit(self, amount):
        self.contents += amount
        
    def debit(self, amount):
        self.contents -= amount

class Item(object):
    
    def __init__(self, name, base_price):
        self.name = name
        self.price = base_price
        
class Resource(Item):
    
    def __init__(self, name, base_price):
        Item.__init__(self, name, base_price)
        economy.resources.append(self)
        
class Product(Item):
    
    def __init__(self, name, base_price, recipe):
        Item.__init__(self, name, base_price)
        economy.products.append(self)
        self.market = Market(self)
        self.recipe = recipe
        self.quantity_demanded = 0 # Quantity demanded per day
        
class FoP(Item):
    
    def __init__(self, name, base_price):
        Item.__init__(self, name, base_price)
        economy.fops.append(self)
        self.level = 0
    
    def upgrade(self):
        self.level += 1


