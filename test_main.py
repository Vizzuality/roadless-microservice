from flask_testing import TestCase
import requests
import urllib2
from main import app
#
# Curerntly, started working on tests - not functional yet

class MyTest(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        return app

class TestViews(MyTest):

    # def test_post(self):
    #     r = requests.post('http://localhost:5001/api/click-point-data/', data={'lat':10, 'lon':10, 'z':3}).json()
    #     print(r)
    #     return

    # def test_get(self):
    #     response = self.client.get("/api/click-point-data/", data={'lat':10, 'lon':10, 'z':3})
    #     print("RESPONSE WAS: ", response)
    #     return

    # def test_flask_application_is_up_and_running(self):
    #     response = urllib2.urlopen(self.get_server_url())
    #     self.assertEqual(response.code, 200)