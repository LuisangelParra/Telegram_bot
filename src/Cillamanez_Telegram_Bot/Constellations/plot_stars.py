from PIL import ImageDraw
from decouple import config
from .Tools.file_manager import read_file
from .Tools.list_manager import corregir_lista
from .Tools.coords import coords_to_pixel

#Variables de entorno
STARS_PATH = config('STARS_PATH')
stars = read_file(STARS_PATH, False)

Constellations_path = {
  "Osa Menor": "./src/Data/OsaMenor.txt",
  "Osa Mayor": "./src/Data/OsaMayor.txt",
  "Hydra": "./src/Data/Hydra.txt",
  "Geminis": "./src/Data/Geminis.txt",
  "Cygnet": "./src/Data/Cygnet.txt",
  "Cazo": "./src/Data/Cazo.txt",
  "Casiopea": "./src/Data/Casiopea.txt",
  "Boyero": "./src/Data/Boyero.txt"
}

def read_coords(points):
    """
    Given a filename of a text file containing two star names per line,
    reads the file into a dictionary, adds the lines between the stars
    to a picture of the star map, and returns the resulting picture.
    """
    stars=[]
    dict1 = {}
    dict2 = {}
    dict3 = {}
    Henry_Draper = []
    for point in points:
      dict1[point[3]] = (point[0],point[1])
      dict2[point[3]] = float(point[4])
      names = []
      if len(point)>6:
        Henry_Draper.append([point[3]])
        for element in point[6:]:
          names.append(element)
        stars.append(names)

    stars_names=[]
    
    for star in stars:
      stars_names.append(tuple(corregir_lista(star)))

    for i in range(len(stars_names)):
      dict3[stars_names[i]] = Henry_Draper[i]
    
    return dict1, dict2, dict3

def plot_plain_stars(picture, int, dict):
  draw = ImageDraw.Draw(picture)
  for star in dict:
    coords = dict[star]
    x, y = coords_to_pixel(coords[0], coords[1], 1000)
    draw.rectangle((x, y, x+2, y+2), fill='white')
  
  return picture

def plot_by_magnitude(picture, int, dict_coords, dict_magnitudes):
  draw = ImageDraw.Draw(picture)
  for star in dict_coords:
    coords = dict_coords[star]
    x, y = coords_to_pixel(coords[0], coords[1], 1000)
    star_size = round(10.0 / (dict_magnitudes[star] + 2))
    draw.rectangle((x, y, x+star_size, y+star_size), fill='white')

  return picture

def read_constellations(filename):
    # Step 1: Read the data from the input file.
    with open(filename, 'r') as f:
        data = f.read()
    
    # Step 2: Parse the data to extract star names and their connections.
    stars = set()
    connections = []
    for line in data.splitlines():
        line_stars = line.split(',')
        stars.update(line_stars)
        connections.append(line_stars)
    
    # Step 3: Create a dictionary to store the star names and their connections.
    constellations = {star: [] for star in stars}
    
    # Step 4: For each star name in the dictionary, find all stars connected to it and add them to the corresponding list in the dictionary.
    for star in constellations.keys():
        for conn in connections:
            if star in conn:
                constellations[star].append(conn[1] if conn[0] == star else conn[0])
    
    # Step 5: Return the resulting dictionary.
    return constellations

def find_code_by_name(name, dic_name_code):
  for star in dic_name_code:
    if name in star:
      return dic_name_code[star]

def plot_constellations(Picture, dict_coords, dict_lines, dict_names, Color, size):
  draw = ImageDraw.Draw(Picture)
  for star in dict_lines:
    star_code = find_code_by_name(star, dict_names)
    cords_star = dict_coords[star_code[0]]

    cords_stars_conected = []
    stars_conected = dict_lines[star]
    stars_conected_code = []
    stars_conected_coords = []
    for star in stars_conected:
      star_conected_code = find_code_by_name(star, dict_names)
      stars_conected_code.append(star_conected_code)

    for code in stars_conected_code:
      stars_conected_coords.append(dict_coords[code[0]])

    x, y = coords_to_pixel(cords_star[0], cords_star[1], size)
    for coords in stars_conected_coords:
      x2, y2 = coords_to_pixel(coords[0], coords[1], 1000)
      draw.line((x,y,x2,y2), fill='green',width=3)

  return Picture

