from __future__ import print_function, division
import flask
import ee
ee.Initialize()

app = flask.Flask(__name__)

@app.route("/")
def hello():
    return '<iframe src="//giphy.com/embed/j3iGKfXRKlLqw" width="480" height="258" frameBorder="0" class="giphy-embed" allowFullScreen></iframe><p><a href="http://giphy.com/gifs/dog-slap-slapping-j3iGKfXRKlLqw">via GIPHY</a></p>'

@app.route('/foo/api/', methods=['POST'])
def my_function():
    if not flask.request.json or not 'lat' in flask.request.json:
        flask.abort(400)
    task = {
            'lat': flask.request.json.get('lat'),
            'lon':flask.request.json.get('lon'),
            'z':flask.request.json.get('z'),
            }
    ee_stats = return_ee_stats(task['lat'], task['lon'], task['z'])
    print("Got {0}".format(ee_stats))
    return flask.jsonify({'task': ee_stats}), 201


def return_ee_stats(lon, lat, z):
    #z_dic = {0: 156412,}

    data_2008 = 'users/malariaatlasproject/accessibilityMap/jrc_accesibility2008'
    data_2017 = 'users/malariaatlasproject/accessibilityMap/jrc_accessibility2017'
    distance = z * 1000. # z_dict[z]

    d_point = {}
    d_point['lon'] = lon
    d_point['lat'] = lat
    d_point['opt_proj'] = 'EPSG:4326'
    d_point['opt_geodesic'] = False

    point_of_interest = ee.Geometry.Point(**d_point).buffer(distance)
    print("Area of buffered point = {} m^2".format(point_of_interest.area().getInfo()))
    # image_id = "WORLDCLIM/V1/MONTHLY/01"  # Image data (note I set tavg band below when image is called)
    d = {}
    d['bestEffort'] = True
    d['geometry'] = point_of_interest
    d['reducer'] = ee.Reducer.count().combine(ee.Reducer.sum(), outputPrefix='', sharedInputs=True
                                              ).combine(ee.Reducer.mean(), outputPrefix='', sharedInputs=True).combine(
                                                ee.Reducer.sampleStdDev(), outputPrefix='', sharedInputs=True).combine(ee.Reducer.min(),
                                                outputPrefix='',sharedInputs=True).combine(ee.Reducer.max(), outputPrefix='', sharedInputs=True)
    return ee.Image(data_2017).select('b1').reduceRegion(**d).getInfo()



if __name__ == "__main__":
    app.run()
# $ curl -i -H "Content-Type: application/json" -X POST -d '{"lat":28.5, "lon":16.3, "z":3}' http://localhost:5000/foo/api/