import uuid
from datetime import datetime
import os

def get_uuid():
    return uuid.uuid4()

def get_current_time():
    """
    This function returns current date and time
    :return:
    """
    return datetime.now()
    
def add(x, y):
    """add numbers"""
    return x + y

def subtract(x, y):
    """subtract numbers"""
    return x - y

def divide(x, y):
    """divide numbers"""
    return x / y

def multiply(x, y):
    """multiply numbers"""
    return x * y
    
if __name__ == "__main__":
    print (get_uuid())
    print(get_current_time())
    print (add(5,7))

