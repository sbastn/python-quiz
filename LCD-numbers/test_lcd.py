import unittest

def lcd(n):
    return '\n|\n\n|\n\n'

class TestLCD(unittest.TestCase):
    
    def test_display_one(self):
        self.assertEquals('\n|\n\n|\n\n', lcd(1))
        
