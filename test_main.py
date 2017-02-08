from __future__ import print_function, division
from main import ClickPointData
import sys
import ee
import os

if sys.platform == 'darwin':
    local_system = True
    # If using a local mac, assume you can initilise using the below...
    ee.Initialize()
else:
    # Else, assume you have an EE_private_key environment variable with authorisation,
    service_account = os.environ['EE_USER']
    print(service_account)
    credentials = ee.ServiceAccountCredentials(service_account, './privatekey.pem')
    ee.Initialize(credentials, 'https://earthengine.googleapis.com')

# Going to test the functionality of the app directly via the return_ee_stats method

def test_basic_response():
    r = ClickPointData().return_ee_stats({'lon': 10, 'lat': 10, 'z': 1})
    print("Returned ", r)
    assert isinstance(r, dict)
    return