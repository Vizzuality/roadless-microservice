# Roadless forests project

[![license](https://img.shields.io/github/license/mashape/apistatus.svg)]()

A Microservice using Flask to identify statistics around a buffered point. Input data are time (in mins), from
[travel time to major cities](http://forobs.jrc.ec.europa.eu/products/gam/).



### Starting the Microservice
To run the Flask microservice:
1. Pull this repo, and `cd` to the folder.
1. Ensure Docker is installed.
1. Ensure the .env file is present contains the EE_PRIVATE_KEY and EE_USER environment variables.
1. Ensure the `start.sh` script can be executed (`chmod +x start.sh`).
1. Execute the start script with a flag indicating if this is a development or production environment, or a test: e.g.
   - `./start.sh test`
   - `./start.sh develop`
   - `./start.sh depoly`
  
At this point, the microservice should be accessible on localhost:8000.

Note: If a development server is started, the app is ultimatley executed with a `python main.py` command,
running the Flask app in development mode. However, if a deoply server is started, the app is executed with
[Gunicorn](http://gunicorn.org/#docs), using the settings in `gunicorn.py`.

Tests run using py.test.

### Using the Microservice

The app accepts POST requests, expecting values for `lat`, `lon` (both floats, of decimal degrees), and `z` (an integer
from 1-12). It gives a json-like response:

```bash
$ curl -i -H "Content-Type: application/json" -X POST -d '{"lat":28.5, "lon":16.3, "z":3}' http://localhost:5000/api/click-point-data/
{
  "task": {
    "b1_count": 32,
    "b1_max": 3606.0,
    "b1_mean": 3550.03125,
    "b1_min": 3500.0,
    "b1_stdDev": 30.397882327556964,
    "b1_sum": 113601.0
  }
}
```

### Halting the microservice
If the process is unresponsive to closing with `ctl + c`, obtain the docker ID and use `docker stop <ID>` to end the process. E.g:

```bash
$docker ps
CONTAINER ID        IMAGE               COMMAND             CREATED              STATUS              PORTS                    NAMES
3ad44399b2be        flask_app           "./entrypoint.sh"   About a minute ago   Up About a minute   0.0.0.0:8000->5000/tcp   kind_elion
$docker stop 3ad44399b2be
```