from __future__ import print_function, division
from flask import Flask, jsonify, request
from flask_restful import reqparse, abort, Api, Resource
import ee

# auth earth engine and start flask
ee.Initialize()
app = Flask(__name__)
api = Api(app)

# CONSTS
params = ['lat','lon','z']
z_dic = [156412, 78206, 3910, 19551, 9776, 4888, 2444, 1222, 610.984, 305.492, 152.746, 76.373, 38.187]
data_2008 = 'users/malariaatlasproject/accessibilityMap/jrc_accesibility2008'
data_2017 = 'users/malariaatlasproject/accessibilityMap/jrc_accessibility2017'
band = 'b1';


# route for returning click point data
def check_request_params(request):
    if request.has_key(params[0]) and request.has_key(params[1]) and request.has_key(params[2]):
        print('Valid parmas')
    else:
        abort(404, message="Request {} must contain lat, lng, and z.".format(request))


# class to handle click request
class ClickPointData(Resource):
    def post(self):
        location = request.get_json(force=True)
        check_request_params(location)
        ee_stats = return_ee_stats(location)
        print("Got {0}".format(ee_stats))
        return ee_stats


# request focused data from EE from params
def return_ee_stats(location):
    distance = z_dic[location['z']]
    d_point = {}
    d_point['lon'] = location['lon']
    d_point['lat'] = location['lat']
    d_point['opt_proj'] = 'EPSG:4326'
    d_point['opt_geodesic'] = False
    point_of_interest = ee.Geometry.Point(**d_point).buffer(distance)
    print("Area of buffered point = {} m^2".format(point_of_interest.area().getInfo()))
    d = {}
    d['bestEffort'] = True
    d['geometry'] = point_of_interest
    d['reducer'] = ee.Reducer.count() \
    .combine(ee.Reducer.sum(), outputPrefix='', sharedInputs=True) \
    .combine(ee.Reducer.mean(), outputPrefix='', sharedInputs=True) \
    .combine(ee.Reducer.sampleStdDev(), outputPrefix='', sharedInputs=True) \
    .combine(ee.Reducer.min(), outputPrefix='',sharedInputs=True) \
    .combine(ee.Reducer.max(), outputPrefix='', sharedInputs=True)

    return ee.Image(data_2008).select(band).reduceRegion(**d).getInfo()


# set up routes/resources
api.add_resource(ClickPointData, '/api/click-point-data/')


# party time
if __name__ == "__main__":
    app.run(debug=True)
