from flask import Flask
from flask import render_template
import socket
import random
import os
import argparse
import time
import requests

# my custom module
import data_create
import data_display

#CSV_TO_USE=r"C:\Users\Dell\\Downloads\\simple_final_docker_ok\\chess.csv"
CSV_TO_USE=r"/tmp/chess.csv"
REST_API_GET='http://api.open-notify.org/astros.json'

color_codes = {
    "red": "#e74c3c",
    "green": "#16a085",
    "blue": "#2980b9",
    "blue2": "#30336b",
    "pink": "#be2edd",
    "darkblue": "#130f40"
}
SUPPORTED_COLORS = ",".join(color_codes.keys())

# Get color from Environment variable
COLOR_FROM_ENV = os.environ.get('APP_COLOR')
# Generate a random color
COLOR = random.choice(["red", "green", "blue", "blue2", "darkblue", "pink"])

def util_rest_get():
    
    print(f"Calling REST API {REST_API_GET}")
    response = requests.get(REST_API_GET)
    print(response)
    print(response.json())

def util_rest_get_query():

    print(f"Calling REST API {REST_API_GET}")
    query = {'lat':'45', 'lon':'180'}
    response = requests.get(REST_API_GET, params=query)
    print(response.json())
    
#############################################
if __name__ == "__main__":

    # Check for Command Line Parameters for color
    parser = argparse.ArgumentParser()
    parser.add_argument('--color', required=False)
    args = parser.parse_args()

    print("Color from random.choice =" + COLOR)
    time.sleep(3) # Sleep for 3 seconds
    util_rest_get_query()
    
    if args.color:
        print("Color from command line argument =" + args.color)

        if COLOR == args.color and COLOR_FROM_ENV == args.color :
            print (f"Bravo ! All color matched, you will get something extra..")
            time.sleep(30) # Sleep for 30 seconds
            data_create.csv_data_create(CSV_TO_USE)
            data_display.display_csv_data(CSV_TO_USE)
            util_rest_get()
        else:
            
            print("A color was set through environment variable -" + COLOR_FROM_ENV + ". However, color from command line argument takes precendence with color - " + args.color) 
    elif COLOR_FROM_ENV:
        print("No Command line argument. Color from environment variable = " + COLOR_FROM_ENV)
        COLOR = COLOR_FROM_ENV
    else:
        print("No command line argument or environment variable. Picking a Random Color = " + COLOR)
        util_rest_get_query()
        
    # Check if input color is a supported one
    if COLOR not in color_codes:
        print("Color not supported. Received '" + COLOR + "' expected one of " + SUPPORTED_COLORS)
        exit(1)

#############################################

# - docker build -t simple:v1 .
# - docker run simple:v1 --color red
# - docker run simple:v1 --color BLACK

# If Normal case, without docker, then set ENV variable APP_COLOR

  # 1 ) Windows : set APP_COLOR=blue
  # 2 ) Linux   : export APP_COLORb=blue
  
  #  python simple.py / Or
  #  python simple.py --color red