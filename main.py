from __future__ import print_function, division
import flask
import flask_restful
import sys
import os
import ee

app = flask.Flask(__name__)
api = flask_restful.Api(app)

print("Starting Flask Microservice. Running on ", sys.platform)
if sys.platform == 'darwin':
    # If using a local mac, assume you can initilise using the below...
    ee.Initialize()
else:
    # Else, assume you have an EE_private_key environment variable with authorisation,
    service_account = os.environ['EE_USER']
    print(service_account)
    credentials = ee.ServiceAccountCredentials(service_account, './privatekey.pem')
    ee.Initialize(credentials, 'https://earthengine.googleapis.com')

class ClickPointData(flask_restful.Resource):
    def __init__(self):
        self.params = ['lat', 'lon', 'z']
        # Hacky way of ensuring the area of polygon does not become too small to function as a reducer
        self.z_dic = [156412, 78206, 3910, 19551, 9776, 4888, 7000, 7000, 7000, 7000, 7000, 7000, 7000]
        self.imageIDs = ['users/malariaatlasproject/accessibilityMap/jrc_accesibility2008',
                       'users/malariaatlasproject/accessibilityMap/jrc_accessibility2017']
        self.band = 'b1'
        return

    def post(self):
        location = flask.request.get_json(force=True)
        self.check_request_params(location)
        ee_stats = self.return_ee_stats(location)
        print("Got {0}".format(ee_stats))
        return ee_stats

    def check_request_params(self, request):
        """route for returning click point data"""
        if request.has_key(self.params[0]) and request.has_key(self.params[1]) and request.has_key(self.params[2]):
            print('Valid parameters passed')
        else:
            flask_restful.abort(404, message="Request {} must contain lat, lon, and z.".format(request))
        return

    def eePoint(self, location):
        """Return an Earth Engine Point, Buffered by a distance set by the z-level"""
        distance = self.z_dic[location['z']]
        d_point = {'lon': location['lon'], 'lat': location['lat'], 'opt_proj': 'EPSG:4326', 'opt_geodesic': False}
        return ee.Geometry.Point(**d_point).buffer(distance)

    def return_ee_stats(self, location):
        """
        Request aggregated data from two EE images, and place into a single dictionary (response_dict).
        We also control the sig figs of the returned data via a string and format command here.
        """
        response_dict = {}
        d = {'bestEffort': True, 'geometry': self.eePoint(location), 'reducer': ee.Reducer.mean()}
        for image in self.imageIDs:
            image_key = image.split('/')[-1][-4:]
            print("Requesting EE data for {0}".format(image_key))
            # print("Set buffer distance of ", self.z_dic[location['z']])
            try:
                response = ee.Image(image).select(self.band).reduceRegion(**d).getInfo()
                if response['b1']:
                    response_dict[image_key + '_mean'] = '{0:6.2f}'.format(response['b1'])
                else:
                    response_dict[image_key + '_mean'] = 'null'
            except ee.EEException:
                print("Hit EEException with request")
                response_dict[image_key + '_mean'] = 'null'
        return response_dict


# set up routes
api.add_resource(ClickPointData, '/api/click-point-data/')

if __name__ == "__main__":
    if sys.platform == 'darwin':
        app.run(host='0.0.0.0', debug=os.getenv('DEBUG') == 'True')
    else:
        app.run(host='0.0.0.0', debug=os.getenv('DEBUG') == 'False')
