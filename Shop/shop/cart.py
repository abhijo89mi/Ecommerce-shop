'''
A shopping cart system for Ecommerce in Django.
'''

class Cart(object):
    class Item(object):
        def __init__(self, itemid, product, quantity=1):
            self.itemid = itemid
            self.product = product
            self.quantity = quantity
    
    def __init__(self):
        self.items = list()
        self.unique_item_id = 0

    def _get_next_item_id(self):
        self.unique_item_id += 1
        return self.unique_item_id
    next_item_id = property(_get_next_item_id)

    def add_item(self, product, quantity=1):
        item = Item(self.next_item_id, product, quantity)
        self.items.push(item)

    def is_empty(self):
        return self.items == []

    def empty(self):
        self.items = list()

    def remove_item(self, itemid):
        self.items = filter(lambda x: x.itemid != itemid, self.items)
        
    def __iter__(self):
        return self.forward()

    def forward(self):
        current_index = 0
        while (current_index < len(self.items)):
            item = self.items[current_index]
            current_index += 1
            yield item
