# Roadless forests project

[![license](https://img.shields.io/github/license/mashape/apistatus.svg)]()

A Microservice using Flask to identify statistics around a buffered point. Input data are time (in mins), from
[travel time to major cities](http://forobs.jrc.ec.europa.eu/products/gam/).



### Docker: starting the Microservice
To run the Flask microservice
1. Ensure Docker is installed.
1. Ensuring the .env file is present containing the EE_PRIVATE_KEY and EE_USER environment variables,
1. `$chmod +x start.sh`
1. `$./start.sh`

At this point, the microservice should be active on localhost:8000.


### Using the Microservice

 POST request and response:

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

### Extended Notes


Python 2.7 app built using Flask, and python-earth-engine-api.

1. Install the requirements via pip

```
pip install -r requirements.txt
```

2. start the app

```bash
$python main.py
```

2. Send a POST request with lat, lon, and z information: e.g. to /api/click-point-data/

```
$ curl -i -H "Content-Type: application/json" -X POST -d '{"lat":28.5, "lon":16.3, "z":3}' http://localhost:5000/api/click-point-data/
````

Example response...

```
curl -i -H "Content-Type: application/json" -X POST -d '{"lat":28.5, "lon":16.3, "z":3}' http://localhost:5000/api/click-point-data/
HTTP/1.0 201 CREATED
Content-Type: application/json
Content-Length: 181
Server: Werkzeug/0.11.15 Python/2.7.12
Date: Fri, 03 Feb 2017 13:31:14 GMT

{
  "task": {
    "tavg_count": 32,
    "tavg_max": 207.0,
    "tavg_mean": 206.75,
    "tavg_min": 206.0,
    "tavg_stdDev": 0.43994134506405985,
    "tavg_sum": 6616.0
  }
}
```
