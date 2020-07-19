#!/usr/bin/env python
# coding: utf-8
# Based on: http://introtopython.org/visualization_earthquakes.html
# Based on: https://github.com/pieqq/PyGeoIpMap

import argparse
import contextlib
import sys
import matplotlib
import numpy as np
# Anti-Grain Geometry (AGG) backend so PyGeoIpMap can be used 'headless'
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import geoip2.database
from collections import defaultdict


#lon/lat dictionary for some plot types
long_lat = dict()
test_long_lat = defaultdict(list)

def get_ip(ip_file):
    """
    Returns a list of IP addresses from a file containing one IP per line.
    """
    with contextlib.closing(ip_file):
        return [line.strip() for line in ip_file]

def geoip_lat_lon(gi, ip_list=[], lats=[], lons=[]):
    """
    This function uses the MaxMind library and databases to geolocate IP addresses
    Returns two lists (latitude and longitude).
    """
    print("Processing {} IPs...".format(len(ip_list)))
    for ip in ip_list:
        try:
            r = gi.city(ip)
        except Exception:
            print("Unable to locate or process IP: %s" % ip)
            continue
        if r is None or r.location.latitude is None or r.location.longitude is None:
            print("Unable to find lat/long for IP: %s" % ip)
            continue
        # put numbers to list
        lats.append(r.location.latitude)
        lons.append(r.location.longitude)

        # append to dictionary - to be used for later and where plot type needs it (it will only hold unique values)
        long_lat[ip] = {'lats':r.location.latitude,'lons':r.location.longitude,'count' : 1}
        # this is for experimental Heatmap function
        test_long_lat[ip].append({'lats':r.location.latitude,'lons':r.location.longitude})
    
    return lats, lons


def generate_map(output, lats=[], lons=[], plottype=None, wesn=None,plotdest=None):
    """
    Using Basemap and the matplotlib toolkit, this function generates a map and
    puts a red dot at the location of every IP addresses found in the list.
    The map is then saved in the file specified in `output`. Depending on output 
    type different picture is presented.
    """
    if (plottype == "connection" and plotdest == None):
        print("[+] No destination specified. Please specify -d/--destination parameter with longitude and latitude as input (i.e. -d 53/12)")
        sys.exit(1)

    print("Generating map and saving it to {}".format(output))
    if wesn:
        wesn = [float(i) for i in wesn.split('/')]
        m = Basemap(projection='cyl', resolution='l',
                llcrnrlon=wesn[0], llcrnrlat=wesn[2],
                urcrnrlon=wesn[1], urcrnrlat=wesn[3])
    else:
        m = Basemap(projection='cyl', resolution='l')
    #m.bluemarble()
    m.drawstates(linewidth=0.1, color="black")
    # plot type
    m.drawlsmask()
    # draw country map
    m.drawcountries(linewidth=0.1, color="black")
    # draw coastlines
    m.drawcoastlines(linewidth=0.1, color="black")

    # If plot type is scatter, draw markers as per https://matplotlib.org/3.2.2/api/_as_gen/matplotlib.pyplot.scatter.html
    if (plottype == "scatter"):
        x, y = m(lons, lats)
        m.scatter(x, y, s=1, color='#CA002A', marker='o', alpha=0.5)
        # save to file
        plt.savefig(output, dpi=1200, bbox_inches='tight')

    # If plot is bubble, draw normal plot with 'bubble-like' structures https://matplotlib.org/3.2.2/api/_as_gen/matplotlib.pyplot.plot.html#matplotlib.pyplot.plot
    if (plottype == "bubble"):
        for key, value in long_lat.items():
            m.plot(value['lons'],value['lats'], linestyle='none', marker="o", markersize=4, alpha=0.6, c="orange", markeredgecolor="black", markeredgewidth=0.1)
        # save to file
        plt.savefig(output, dpi=1200, bbox_inches='tight')

    # If plot type is connectionmap, draw plot which joins connection source latitude and longitude with destination latitude and longitude
    if (plottype == "connectionmap" and plotdest != None):
        dst = [float(i) for i in plotdest.split('/')]
        # based on our dictionary with connections, draw the lines 
        for key, value in long_lat.items():
            m.drawgreatcircle(value['lons'],value['lats'],dst[0],dst[1], linewidth=0.1, color='#CA002A')
        # save to file
        plt.savefig(output, dpi=1200, bbox_inches='tight')


def main():
    arguments = argparse.ArgumentParser(description='Visualize IP addresses on the map')
    arguments.add_argument('-i', '--input', dest="input", type=argparse.FileType('r'), help='Input file. One IP per line',default=sys.stdin)
    arguments.add_argument('-o', '--output', default='output.png', help='Path to save the file (e.g. /tmp/output.png)')
    arguments.add_argument('-db', '--db', default=None, help='Full path to MaxMind GeoLite2-City.mmdb database file (download from https://dev.maxmind.com/geoip/geoip2/geolite2/)')
    arguments.add_argument('-e','--extents', default=None, help='Extents for the plot (west/east/south/north). Default to globe.')
    arguments.add_argument("-t","--type", default="scatter", help="Plot type scatter, bubble, connectionmap")
    arguments.add_argument("-d","--destination", default=None, help="When connectionmap line plot is used, add latitude and longitude as destination (i.e. -d 51.50/0.12)")
    args = arguments.parse_args()

    # Get output to file
    output = args.output

    # Get list of IPs out of file
    ip_list = get_ip(args.input)
    # Parse MaxMind db file
    gi = geoip2.database.Reader(args.db)
    # Get latitude and longitude as lists
    lats, lons = geoip_lat_lon(gi, ip_list)
    # Call final function to start drawing on the map
    generate_map(output, lats, lons, plottype=args.type, wesn=args.extents,plotdest=args.destination)


if __name__ == '__main__':
    main()
