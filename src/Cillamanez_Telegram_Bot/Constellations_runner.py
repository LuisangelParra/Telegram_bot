from PIL import Image
from Constellations import plot_stars


img_size = 1000
dict1,dict2,dict3 = plot_stars.read_coords(plot_stars.stars)

def constellations(option, constellation_name = None):
  if option == 1:
    img = Image.new('RGB', (img_size, img_size), color='black')
    plot_stars.plot_by_magnitude(img,img_size,dict1,dict2)
    img.save('generated_images\constellations.jpg')
  elif option == 2:
    img = Image.new('RGB', (img_size, img_size), color='black')
    plot_stars.plot_by_magnitude(img,img_size,dict1,dict2)
    conste = plot_stars.read_constellations(plot_stars.Constellations_path[constellation_name])
    plot_stars.plot_constellations(img, dict1, conste, dict3, 'green', img_size)
    img.save('generated_images\constellations.jpg')
  elif option == 3:
    img = Image.new('RGB', (img_size, img_size), color='black')
    plot_stars.plot_by_magnitude(img,img_size,dict1,dict2)
    for constellation in plot_stars.Constellations_path:
      conste = plot_stars.read_constellations(plot_stars.Constellations_path[constellation])
      plot_stars.plot_constellations(img, dict1, conste, dict3, 'green', img_size)
      img.save('generated_images\constellations.jpg')


