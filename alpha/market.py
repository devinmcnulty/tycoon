""" Economic classes, objects, functions """
###   Todo   ###

###   ---    ###


class Market(object):
    
    def __init__(self, product):
        self.product = [product]
        self.resources = []
        self.fops = []
        self.items = [self.product, self.resources, self.fops]
        self.firms = []
    
    def addFirm(self, firm):
        self.firms.append(firm)
        
class Firm(object):
    
    def __init__(self, name, product):
        self.name = name
        self.product = product
        self.market = product.market
        self.market.addFirm(self)
        self.inventory = Inventory(self.product)
        self.account = Account()
    
    def buy(self, item, quantity):
        self.inventory.contents[item] += quantity
        self.account.debit(item.price * quantity)
        
    def sell(self, item, quantity):
        self.inventory.contents[item] -= quantity
        self.account.credit(item.price * quantity)
    
    def produce(self, quantity):
        self.inventory.contents[self.product] += quantity
        for resource in self.product.recipe:
            self.inventory.contents[resource] -= self.product.recipe[resource] * quantity

class Inventory(object):
    
    def __init__(self, product):
        self.product = product
        self.contents = {product : 0}
        for item_type in product.market.items:
            for item in item_type:
                self.contents[item] = 0
        
    
    def quantity(self, item):
        # Returns quantity of item in inventory
        return self.contents[item]

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
        

class Product(Item):
    
    def __init__(self, name, base_price, recipe):
        Item.__init__(self, name, base_price)
        self.market = Market(self)
        self.recipe = recipe
        
class FoP(Item):
    
    def __init__(self, name, base_price):
        Item.__init__(self, name, base_price)
        self.level = 0
    
    def upgrade(self):
        self.level += 1


