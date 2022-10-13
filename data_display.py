import csv
import sys
# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def display_csv_data(file_path):

    with open(file_path, 'r') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            print(dict(row))
            
def display_txt_data(file_path) :

    try:
    
        #trying to open a file in read mode
        fo = open(file_path,"rt")
        print("File opened")
    except FileNotFoundError:
        print("File does not exist, app closing")
        sys.exit()
    
    print ("Reading file content in a string...")
    s = fo.read()
    # show the contents from string s

    print(s)
    
    print ("Reading file content...")
    # close the text file
    fo.close()
    print("File does not exist")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    display_txt_data('people1.txt')
    display_csv_data('people.csv')


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
