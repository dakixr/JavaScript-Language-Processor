import sys

from tkinter import filedialog
from tkinter import *

first_time = True

def init():

    global file_in, first_time

    if not first_time:
        input("Pulsar cualquier tecla para procesar otro archivo...")
    else:
        first_time = False

    root = Tk()
    root.withdraw()
    file_in = filedialog.askopenfile()

    if not file_in:
        sys.exit()


def get_file():

    global source_code, file_in

    #file_in = open(sys.argv[1], "r")

    source_code = ""

    for line in file_in:
        source_code += line

