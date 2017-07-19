""" ECONOMY  MODULE """

#    IN A NUTSHELL: The idea is to have a self-contained economic system, which the game can interact with.
#
#    PURPOSE: Facilitate all economic transactions between entities in the game, through an interconnected economic system, including:
#        - initiating all economic objects, handling all economic variables
#        - buying and selling inputs, products, factors of production and upgrades
#        - producing products
#        - calculating quantity demanded for products through a detailed demand function
#
#    HOW IT WORKS: When completed, the economy could be initialized through one function - economy.initialize(). This function would take all the necessary
#        parameters to initialize all goods and firms, which in turn initialize markets, inventories, accounts, etc. Currently creating a Product object will 
#       in turn create a market for said product. Creating a firm will in turn create an inventory and account for said firm. The idea being to reduce the
#       amount of objects that have to be manually created every time you want to add on object to the game. 
#
#       I try to write my classes and functions to be as intuitive as possible for when we write the game logic. For example, you could create a button that 
#       buys butter. You would have that button call "firm.buy(good, quantity)", e.g. plumbus_inc.buy(shleem, 3). The buy function then increases the quantity
#       in that firm's inventory of the good, and decreases the cost from their account. I will try to create the rest of the system in a similar fashion,
#       so that tying together the game and the economy can be as simple as using a module.


def initialize():
    """ Will initialize the economy including all objects (products, firms, etc.)"""
    global economy
    economy = Economy()

class Economy(object):
    """ An economy object, used to store system wide variables/functions like the products, resources, markets present in the economy """
    def __init__(self):
        self.products = []
        self.resources = []
        self.fops = []
        self.markets = []

class Market(object):
    """ A market is specific to a product, created by creating a product. Used for variables/functions relevant to individual products and firms which
        produce them """
    def __init__(self, product):
        economy.markets.append(self)
        self.product = product
        self.firms = [] # Created firms are appended to this
        self.size = 100 # Number of customers, should be based off size of town
    
    def addFirm(self, firm):
        self.firms.append(firm)
     
class Firm(object):
    """ A firm  produces a specific product. Contains all the variables/functions related to buying, selling, producing on a firm level """
    def __init__(self, name, product):
        self.name = name
        self.product = product
        self.market = product.market
        self.market.addFirm(self)
        self.account = Account() # Creates an Account object to store cash. Rather redundant now but if loans, assets become involved it will be useful.
        self.inventory = Inventory(self.product) # Creates an Inventory object to store quantities of all items (including FoPs and their level)
    
    def buy(self, item, quantity):
        self.inventory.contents[item][0] += quantity
        self.account.debit(item.price * quantity)
        
    def sell(self, item, quantity):
        """ For selling non-produced, fixed demand items (resources, FoPs) """
        self.inventory.contents[item][0] -= quantity
        self.account.credit(item.price * quantity)
    
    def produce(self, quantity):
        self.inventory.contents[self.product][0] += quantity
        for resource in self.product.recipe:
            self.inventory.contents[resource][0] -= self.product.recipe[resource] * quantity
            
    def sellProduct(self):
        """ For selling produced, variable demand items (products) """
        quantity = self.product.quantity_demanded
        self.sell(self.product, quantity)
        
    def determineDemand(self):
        """ Calculates quantity demanded for a product based on market factors """
        # Determinants
        number_of_firms = len(self.product.market.firms)
        quality = self.inventory.getLevel(self.product)
        market_size = self.product.market.size
        slope = 2
        
        demand = (market_size - (self.product.price * slope) + quality * (market_size/10))/number_of_firms
        self.product.quantity_demanded = int(demand)

class Inventory(object):
    """ Object for storing quantities and levels of items of firms """
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
    """ Object for storing cash of firm, could be expanded to include loans, assets """
    def __init__(self):
        self.contents = 0
    
    def credit(self, amount):
        self.contents += amount
        
    def debit(self, amount):
        self.contents -= amount

class Item(object):
    """ Any object with a price (can be bought/sold), including resources, products, FoPs """
    def __init__(self, name, base_price):
        self.name = name
        self.price = base_price
        
class Resource(Item):
    """ Item used in the production of a product """
    def __init__(self, name, base_price):
        Item.__init__(self, name, base_price)
        economy.resources.append(self)
        
class Product(Item):
    """ Item produced by firms using resources and FoPs """
    def __init__(self, name, base_price, recipe):
        Item.__init__(self, name, base_price)
        economy.products.append(self)
        self.market = Market(self)
        self.recipe = recipe
        self.quantity_demanded = 0 # Quantity demanded per day
        
class FoP(Item):
    """ Item used in production of a product, is not used up in production, can be upgraded """
    def __init__(self, name, base_price):
        Item.__init__(self, name, base_price)
        economy.fops.append(self)
        self.level = 0
    
    def upgrade(self):
        self.level += 1


