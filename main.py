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
# z = int(input("z: "))
# print(mercantile.tile(x_min, y_max, z))
# print(mercantile.tile(x_max, y_min, z))
# input(';;')
zoom = 15


x_ind_min, y_ind_min, zoom = mercantile.tile(x_min, y_max, zoom)
x_ind_max, y_ind_max, zoom = mercantile.tile(x_max, y_min, zoom)


zoom = str(zoom)
zoom_dir = os.path.join(dirname, zoom)
if not zoom in os.listdir(dirname):
    os.mkdir(zoom_dir)
xs = os.listdir(zoom_dir)
if xs:
    x_ind_min = max([int(x_) for x_ in xs ])
x_length = x_ind_max - x_ind_min + 1
y_length = y_ind_max - y_ind_min + 1
print("Running...")
for x in range(x_ind_min, x_ind_max + 1):
    x_dir = os.path.join(zoom_dir, str(x))
    if not str(x) in os.listdir(zoom_dir):
        os.mkdir(x_dir)
    ys = os.listdir(x_dir)
    if ys:
        y_ind_min = max([int(y_.replace('.png', '')) for y_ in ys])
        print(y_ind_min)
    for y in range(y_ind_min, y_ind_max + 1):
        url = url_template.format(zoom, x, y)
        file_name = f"{y}.png"
        file_path = os.path.join(x_dir, file_name)
        headers={'User-Agent': 'M'}
        r= requests.get(url.strip(), headers=headers, timeout=10)
        while r.status_code != 200:
            r = requests.get(url.strip(), headers=headers, timeout=10)
            print("Reconnecting...", end="\r")
            if r.status_code == 200: 
                 print("\n\n\nConnected!")
        with open(file_path, 'wb') as f:
            f.write(r.content)
    print(f"X: {x}: Done!")
print(f"{zoom}-Zoom: Done! ")
