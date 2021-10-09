import unittest
import uuid
from book_inventory import *
from unittest import mock
import xml.etree.ElementTree as ETree

TEST_UUIDS = ["8fddf6ab-a535-4d3e-bb14-7afaf3c0f01a",
              "fe7d920c-8db0-4f0e-9e42-0c1d4b7471e0",
              "d579007a-8051-49b3-bf9a-7f9c5a6e6067",
              "1eea75b8-8b64-45cc-a3a8-8e1129554e1c"]

BOOK_TITLES = ["Harry Potter and the Order of the Phoenix", "The Ickabog", "The Christmas Pig"]
AUTHORS = ["J. K. Rowling"]

uuid_pool = iter(TEST_UUIDS)

def generate_uuid():
    return next(uuid_pool)

class Test_Inventory (unittest.TestCase):
    def test_inventory_item_str(self):
        invent_item_name = "Inventory Item Test"
        invent_item = InventoryItem("Inventory Item Test")
        self.assertEqual(invent_item_name, str(invent_item))

    def test_inventory_item_str(self):
        invent_item_name = "Inventory Item Test"
        invent_item = InventoryItem(invent_item_name, TEST_UUIDS[3])
        self.assertEqual(f"InventoryItem({TEST_UUIDS[3]},{invent_item.name})", repr(invent_item))

    @mock.patch('uuid.uuid4', generate_uuid)
    def test_book_uuid_empty(self):
        patched_uuid = TEST_UUIDS[0]
        new_book = Book(BOOK_TITLES[1], AUTHORS[0])
        self.assertEqual(patched_uuid, new_book.uuid)

    def test_book_uuid_not_empty(self):
        created_uuid = TEST_UUIDS[1]
        new_book = Book(BOOK_TITLES[0], AUTHORS[0], uuid=created_uuid)
        self.assertEqual(uuid.UUID(created_uuid), new_book.uuid)

    def test_book_str_empty_author(self):
        new_book = Book(BOOK_TITLES[0], "")
        self.assertEqual(str(new_book), BOOK_TITLES[0])

    def test_book_str_filled_author(self):
        new_book = Book(BOOK_TITLES[0], AUTHORS[0])
        self.assertEqual(str(new_book), "Harry Potter and the Order of the Phoenix by J. K. Rowling")

    def test_inventory_add_valid_item_true(self):
        inventory = Inventory()
        new_book = Book(BOOK_TITLES[0], AUTHORS[0])
        inventory.add_item(new_book)
        self.assertEqual(len(inventory.inventory_items), 1)
    
    def test_inventory_add_invalid_item(self):
        inventory = Inventory()
        with self.assertRaises(TypeError):
            inventory.add_item(BOOK_TITLES[0])

    def test_inventory_save_to_file(self):
        books = [
            Book(BOOK_TITLES[1], AUTHORS[0]),
            Book(BOOK_TITLES[0], AUTHORS[0]),
            Book(BOOK_TITLES[2])
        ]
        
        inventory = Inventory()
        for book in books:
            inventory.add_item(book)
        
        expected_tree = ETree.parse('expected_result.xml')

        # act
        actual = inventory.get_xml_tree()
        
        # assert
        self.assertEqual(self.remove_uuid_from_xml(expected_tree), self.remove_uuid_from_xml(actual))

    def test_invalid_inventory_from_file(self):
        with self.assertRaises(Exception) as ex:
            Inventory.load_from_xml("invalid_item.xml")

        self.assertEqual("Provided file consists of invalid data.", str(ex.exception))

    def test_valid_inventory_from_file(self):
        # arrange
        books = [
            Book(BOOK_TITLES[1], AUTHORS[0]),
            Book(BOOK_TITLES[0], AUTHORS[0]),
            Book(BOOK_TITLES[2])
        ]
        
        expected_inventory = Inventory()
        for book in books:
            expected_inventory.add_item(book)

        # act
        loaded_inventory = Inventory.load_from_xml("valid_items.xml")

        # assert
        self.assertEqual(expected_inventory.inventory_items, loaded_inventory.inventory_items)

    def test_remove_item_empty_inventory(self):
        # arrange
        inventory = Inventory()

        # act
        inventory.remove_item(TEST_UUIDS[0])

        # assert
        self.assertEqual(len(inventory.inventory_items), 0)

    @mock.patch('uuid.uuid4', generate_uuid)
    def test_remove_item_filled_inventory(self):
        # arrange
        patched_uuid = TEST_UUIDS[1]
        inventory = Inventory()
        inventory.add_item(Book(BOOK_TITLES[0], AUTHORS[0]))

        # act
        inventory.remove_item(patched_uuid)

        #assert
        self.assertEqual(len(inventory.inventory_items), 0) 

    @mock.patch('uuid.uuid4', generate_uuid)
    def test_remove_non_existing_item_inventory(self):
        # arrange
        inventory = Inventory()
        inventory.add_item(Book(BOOK_TITLES[0], AUTHORS[0]))

        # act
        inventory.remove_item("c0fdb14b-c984-4770-99b0-8b3d98e7aca7")

        # assert
        self.assertEqual(len(inventory.inventory_items), 1)

    def remove_uuid_from_xml(self, xml_tree):
        for elem in xml_tree.iter():
            for row in list(elem):
                if row.tag == 'uuid':
                    elem.remove(row)

if __name__ == '__main__':
	unittest.main()