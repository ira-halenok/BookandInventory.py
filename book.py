import uuid as uuid_module

class InventoryItem:
    def __init__(self,name,uuid=None):
        self.name = name
        if uuid is None:
            self.uuid = uuid_module.uuid4()
        else:
            self.uuid = uuid_module.UUID(uuid)

    def __str__(self):
        return self.name

    def __repr__(self):
        return "InventoryItem({},{})".format(self.uuid,self.name)

class Book(InventoryItem):
    def __init__(self,title,author='',uuid=None):
        if uuid is None:
            super().__init__(title)
        else:
            super().__init__(title,uuid=uuid)
        
        self.title = title
        self.author = author

    def __str__(self):
        if self.author == '':
            return self.title
        else:
            return '{} by {}'.format(self.title,self.author)

    def __eq__(self, other):
        return (self.title, self.author) == (other.title, other.author)