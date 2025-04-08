import sys
sys.path.append( '.' )
import unittest
from setuptool_test.utils.utils import *

class MyTest(unittest.TestCase):

    # 'unittest' module requires that we start the name of test methods with the word test, 
    # otherwise, our test won't run as expected.
    def test_add(self):
    
        self.assertEqual(add(1, 2), 3)
        self.assertEqual(add(-1, 1), 0)
    def test_subtract(self):    
        self.assertEqual(subtract(3, 1), 2)
    def test_multiply(self):    
        self.assertEqual(multiply(9, 9), 81)
        
    def test_divide(self):
        self.assertEqual(divide(10, 2), 5)
        self.assertEqual(divide(0, 1), 0) # ZeroDivisionError handling
        with self.assertRaises(ZeroDivisionError):
            divide(10, 0)        
       
if __name__ == "__main__":
    unittest.main()    
    
## Running step:
# - Goto python_setuptool_test/
# - python3 -m unittest tests/tests.py        
    

