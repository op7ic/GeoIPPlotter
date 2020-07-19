# GeoIPPlotter

GeoIP plotting script written in Python to help security teams draw visualized reports from IP addresses. This script is based on already existing excellent [PyGeoIPMap](https://github.com/pieqq/PyGeoIpMap) project with some additions towards extended plotting capabilities.

This script currently supports the following plot types:
- [Scatter plot](https://matplotlib.org/3.2.2/api/_as_gen/matplotlib.pyplot.scatter.html)
- [Bubble map](https://matplotlib.org/3.2.2/api/_as_gen/matplotlib.pyplot.plot.html#matplotlib.pyplot.plot)
- [Connection map](https://en.wikipedia.org/wiki/Great_circle)

## Prerequisites 

Install the following prerequsites:

* [numpy](http://www.numpy.org/)
* [matplotlib](http://matplotlib.org/)
* [Basemap](http://matplotlib.org/basemap/)

The following command line should take care of prerequisites on Debian/Ubuntu:

```
apt-get install libgeos-dev && pip3 install -r requirements.txt
```

## Usage

```
usage: geoipplotter.py [-h] [-i INPUT] [-o OUTPUT] [-db DB] [-e EXTENTS]
                       [-t TYPE] [-d DESTINATION]

Visualize IP addresses on the map

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        Input file. One IP per line
  -o OUTPUT, --output OUTPUT
                        Path to save the file (e.g. /tmp/output.png)
  -db DB, --db DB       Full path to MaxMind GeoLite2-City.mmdb database file
                        (download from
                        https://dev.maxmind.com/geoip/geoip2/geolite2/)
  -e EXTENTS, --extents EXTENTS
                        Extents for the plot (west/east/south/north). Default
                        to globe.
  -t TYPE, --type TYPE  Plot type scatter, bubble, connectionmap
  -d DESTINATION, --destination DESTINATION
                        When connectionmap line plot is used, add latitude and
                        longitude as destination (i.e. -d 51.50/0.12)
```

## Common Extends
To zoom towards specific continent use ```-e``` parameter with approximate location flags:

Europe - ``` -12/45/30/65 ```
Middle East - ``` 10/80/-10/60 ```
Africa + Middle East - ``` -20/90/-60/40 ```
Africa - ``` -20/55/-60/40 ```
South America - ``` -100/-30/-60/40 ```
North America - ```  -200/-40/1/90 ```
Americas (North + South) - ``` -200/-20/-60/90 ```

If argument parsing throws an error around input because it doesn't like extra ```-``` use double quotes to pass appropriate parameter i.e. ```-e " -100/-30/-60/40"```

## Example Use

To generate scatter plot:
```bash
python3 geoipplotter.py -t scatter --db /tmp/GeoLite2-City.mmdb -i sourceip.txt -o scatter.png
```
To generate bubble plot:
```bash
python3 geoipplotter.py -t bubble --db /tmp/GeoLite2-City.mmdb -i sourceip.txt -o bubble.png
```
To generate connectionmap against specific LON/LAT (useful for showing that **we** are under attack):
```bash
python3 geoipplotter.py -t connectionmap --db /tmp/GeoLite2-City.mmdb -i sourceip.txt -o connectionmap.png -d 51.50/0.12
```

## Example output

![Alt text](samples/scatter.png?raw=true "Scatter plot of IPs")
![Alt text](samples/bubble.png?raw=true "Bubble plot of IPs")
![Alt text](samples/connectionmap.png?raw=true "Connection map plot of IPs")