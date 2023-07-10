from PIL import Image
import requests
import mercantile
import os

url_template = "https://a.tile.openstreetmap.org/{}/{}/{}.png"
dirname = 'images'
if not dirname in os.listdir():
    os.mkdir(dirname)
y_max = 45.590074
y_min = 37.172258
x_max = 73.218926
x_min =  55.998219


lon = x_min
lat = y_max

for zoom in range(20):

    x_ind_min, y_ind_min, zoom = mercantile.tile(x_min, y_max, zoom)
    x_ind_max, y_ind_max, zoom = mercantile.tile(x_max, y_min, zoom)


    zoom = str(zoom)
    zoom_dir = os.path.join(dirname, zoom)
    if not zoom in os.listdir(dirname):
        os.mkdir(zoom_dir)
   


    x_length = x_ind_max - x_ind_min + 1
    y_length = y_ind_max - y_ind_min + 1

    images = {}
    for x in range(x_ind_min, x_ind_max + 1):
        x_dir = os.path.join(zoom_dir, str(x))
        if not str(x) in os.listdir(zoom_dir):
            os.mkdir(x_dir)
        x_images = []
        for y in range(y_ind_min, y_ind_max + 1):
            file_name = f"{y}.png"
            file_path = os.path.join(x_dir, file_name)
            if file_name in os.listdir(x_dir):
                _image = Image.open(file_path)
                x_images.append(_image)
                continue
            url = url_template.format(zoom, x, y)
            print(url)
            headers={'User-Agent': 'M'}
            r= requests.get(url.strip(), headers=headers, timeout=10)
            with open(file_path, 'wb') as f:
                f.write(r.content)
            _image = Image.open(file_path)
            x_images.append(_image)
        images[x] = x_images





    new_image = Image.new('RGB',(x_length*_image.size[0], y_length*_image.size[1]), (250,250,250))
    x_co = 0
    for _x in images.keys():
        y_co = 0
        for im in images[_x]:
            new_image.paste(im,(im.size[0] * x_co, im.size[1] * y_co))
            y_co += 1
        x_co += 1

    # new_image.paste(image2,(image1_size[0],0))
    new_image.save(os.path.join(zoom_dir, 'merged.png'),"PNG")


    print(f"{zoom}-Zoom: Done! ")
