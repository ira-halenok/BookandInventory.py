#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  4 11:39:31 2018

@author: chris
"""


import unittest

from inventory import Inventory as library 

#created my test class after importing my book_inventory.py


class BookInventoryTester(unittest.TestCase):
# I struggled to get this to work.  
    def test_set_up(self):
        pass
    def test_add_item(self):
        new_book = 'good book'
        if library == []:# I used the empty list set '[]', 'True' and ' False' 
            #the tests using all 3 of these bools said ok. not sure why but this 
            #works with the if statement
            library.add_item(self,new_book)
            self.assertIn(new_book,library)
        
    
        
if __name__ == '__main__':
    unittest.main()
    print(library)
        
