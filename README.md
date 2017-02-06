# Roadless forests project
## Function to identify stats around a point

MIT License

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


Docker info:

buld the image in the local folder via:

```
docker build -t <desired name> .
```

Run the container:

```
docker run -d -p docker_port_number:desired_host_port <desired name>
```
