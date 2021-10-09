# -*- coding: utf-8 -*-
"""
Created on Tue Oct 16 13:05:30 2018

@author: Chris
"""


import xml.etree.ElementTree as ETree
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

class Inventory:
    def __init__(self):
        self.inventory_items = []

    def add_item(self,item):
        if isinstance(item, InventoryItem):
            self.inventory_items.append(item)
        else:
            raise TypeError

    def remove_item(self,item_uuid):
        for item in self.inventory_items:
            if item.uuid == item_uuid:
                self.inventory_items.remove(item)

    def get_xml_tree(self):
        # create etree
        root = ETree.Element('Inventory')
        for item in self.inventory_items:
            item_xml = ETree.Element('InventoryItem')
            # save the item type in the xml tree
            item_type = ETree.SubElement(item_xml,'type')
            item_type.text = str(item.__class__.__name__)
            # go through all attributes in the item dictionary
            for attribute, value in item.__dict__.items():
                item_attribute = ETree.SubElement(item_xml,attribute)
                item_attribute.text = str(value)
            root.append(item_xml)
        tree = ETree.ElementTree(root)

        return tree

    def save_item(self, filename):
        tree = self.get_xml_string()
        tree.write(filename,'UTF-8')

    @staticmethod
    def load_from_xml(filename):
        inventory_tree = ETree.parse(filename)
        root = inventory_tree.getroot()
        inventory = Inventory()
        for inventory_item in root:
            # check that our item type is Book
            # not necessary now, but it would be if we had more than one
            # InventoryItem type to load
            if inventory_item.find('type').text == 'Book':
                title = inventory_item.find('title').text
                author = inventory_item.find('author').text
                uuid = inventory_item.find('uuid').text
                b = Book(title, uuid=uuid)
                if author is not None: # possible for author to be empty
                    b.author = author
                inventory.add_item(b)
            else:
                raise Exception('Provided file consists of invalid data.')

        return inventory

    def __str__(self):
        return '\n'.join(str(item)for item in self.inventory_items)
