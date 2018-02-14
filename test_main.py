from __future__ import print_function, division
from main import ClickPointData
import pytest
import ee
import os
from dotenv.main import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

if os.environ['EE_CREDENTIAL_STORE'] == 'local':
    local_system = True
    # If using a local mac, assume you can initialise using the below...
    ee.Initialize()
else:
    # Else, assume you have an EE_private_key environment variable with authorisation,
    service_account = os.environ['EE_USER']
    print(service_account)
    credentials = ee.ServiceAccountCredentials(service_account, os.path.join(os.path.dirname(__file__), './privatekey.pem'))
    ee.Initialize(credentials, 'https://earthengine.googleapis.com')

# Going to test the functionality of the app directly via the return_ee_stats method


def test_basic_response_zoomed():
    expected = {'2017_mean': '  3.98', '2008_mean': '  6.02'}
    d = {'lon': -16.3, 'lat': 28.5, 'z': 12}
    r = ClickPointData().return_ee_stats(d)
    assert isinstance(r, dict), "Return was not of dictionary type"
    assert r == expected, "Returned dictionary {r} incorrect".format(r=r)
    return


def test_basic_response_distant():
    expected = {'2017_mean': ' 71.08', '2008_mean': '106.74'}
    d = {'lon': -16.3, 'lat': 28.5, 'z': 0}
    r = ClickPointData().return_ee_stats(d)
    assert r == expected, "Returned dictionary {r} incorrect".format(r=r)
    return


def test_point_distant():
    """Check a buffered area was within 10% of the expected size for distant zoom level"""
    target_size = 75936587859
    d = {'lon': -16.3, 'lat': 28.5, 'z': 0}
    p = ClickPointData().eePoint(d).area().getInfo()
    assert p == pytest.approx(target_size, rel=0.1)
    return


def test_point_zoomed():
    """Check a buffered area was within 10% of the expected size for closest zoom level"""
    target_size = 152098957.601
    d = {'lon': -16.3, 'lat': 28.5, 'z': 12}
    p = ClickPointData().eePoint(d).area().getInfo()
    assert p == pytest.approx(target_size, rel=0.1)
    return