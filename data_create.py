import csv
# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def csv_data_create(outfile_path):
    # Use a breakpoint in the code line below to debug your script.
    
    with open(outfile_path, 'w', newline='') as file:
    
        fieldnames = ['player_name', 'fide_rating']
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()
        
        writer.writerow({'player_name': 'Magnus Carlsen', 'fide_rating': 2870})
        writer.writerow({'player_name': 'Fabiano Caruana', 'fide_rating': 2822})
        writer.writerow({'player_name': 'Ding Liren', 'fide_rating': 2801})

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    csv_data_create('./players.csv')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
