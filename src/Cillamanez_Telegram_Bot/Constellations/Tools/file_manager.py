# This file contains functions for reading files.
def read_file(filename, commas):
    """
    Reads a file, creates a tuple for each line, and puts each tuple in a list.
    Returns the list of tuples.
    """
    # Open the file for reading
    with open(filename, 'r') as file:
        # Read all lines from the file and strip whitespace
        lines = [line.strip() for line in file.readlines()]
        # Create a list of tuples from the lines
        if commas == True:
          tuples = [tuple(line.split(",")) for line in lines]
        else:
          tuples = [tuple(line.split()) for line in lines]
        # Return the list of tuples
        return tuples
    
# Path: src\Tools\file_manager.py
    

