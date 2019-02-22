from flask import Flask, request, send_file, redirect
from gmplot import gmplot
import time
import os

app = Flask(__name__)

@app.route('/', methods = ['GET'])
def home():
    return send_file('./templates/home.html')

@app.route("/lopy", methods = ['GET'])
def lopy():
    query = request.query_string
    coord_list = [tuple(map(float, x.split(","))) for x in [pair.split('=')[1] for pair in query.split('&')]]
    file = open("locations.txt", 'a')
    coord_str = map(str, coord_list)
    no = []
    for x in coord_str:
        n = "{}\n".format(x)
        print(n)
        no.append(n)
    print(no)
    file.writelines(no)
    file.close()
    return "received"

@app.route('/locations', methods = ['GET'])
def locations():
    URL = "/map/sheeps?"
    file = open("locations.txt", 'r')
    lines = file.readlines()
    coords = ""
    for line in lines:
        s = line[1:]
        n = s[:-2]
        l = n.replace(" ", "")
        ss = "coord={}".format(l)
        if len(coords) == 0:
            coords = ss
        else:
            coords = "{}&{}".format(coords, ss)
    new_url = "{}{}".format(URL, coords)
    return redirect(new_url)

@app.route('/map/polygon', methods = ['GET'])
def polygon():
    my_dir = "./templates"
    for fname in os.listdir(my_dir):
        if fname.startswith("polygon"):
            os.remove(os.path.join(my_dir, fname))

    query = request.query_string
    coord_list = [tuple(map(float, x.split(","))) for x in [pair.split('=')[1] for pair in query.split('&')]]

    coord_first = coord_list[0]
    c1 = coord_first[0]
    c2 = coord_first[1]

    gmap = gmplot.GoogleMapPlotter(c1, c2, 20)

    coord_lats = [x[0] for x in coord_list]
    coord_lats.append(c1)
    coord_lons = [x[1] for x in coord_list]
    print(coord_lats)
    coord_lats.append(c2)

    gmap.plot(coord_lats, coord_lons, 'cornflowerblue', edge_width=10)
    filename = "./templates/polygon{}.html".format(int(time.time()))
    g = gmap.draw(filename)
    print(os.path.isfile(filename))
    while not os.path.isfile(filename):
        pass
    return send_file(filename)

@app.route('/map/sheeps', methods = ['GET'])
def sheeps():
    my_dir = "./templates"
    for fname in os.listdir(my_dir):
        if fname.startswith("sheeps"):
            os.remove(os.path.join(my_dir, fname))

    query = request.query_string
    sheeps_list = [tuple(map(float, x.split(","))) for x in [pair.split('=')[1] for pair in query.split('&')]]
    start_sheep = sheeps_list[0]
    c1 = start_sheep[0]
    c2 = start_sheep[1]
    gmap = gmplot.GoogleMapPlotter(c1, c2, 20)

    scatter_lats = [x[0] for x in sheeps_list]
    scatter_lons = [x[1] for x in sheeps_list]
    gmap.scatter(scatter_lats, scatter_lons, '#3B0B39', size=1000, marker=False)

    filename = "./templates/sheeps{}.html".format(int(time.time()))
    gmap.draw(filename)
    return send_file(filename)

#When run from command line, start the server
if __name__ == '__main__':
    my_dir = "./"
    for fname in os.listdir(my_dir):
        if fname.startswith("locations.txt"):
            os.remove(os.path.join(my_dir, fname))
    app.run(host ='0.0.0.0', port = 3333, debug = True)
