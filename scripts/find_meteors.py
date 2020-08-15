import requests
import math


def calc_dist(lat1, lon1, lat2, lon2):
    """Calculates distance between two points on a sphere given their
    longitudes and latitudes, using the haversine formula.

    Parameters
    ----------
    lat1 : float
        Latitude for first location
    lon1 : float
        Longitude for first location
    lat2 : float
        Latitude for second location
    lon2 : float
        Longitude for second location

    Returns
    -------
    float
        The great-circle distance between two points on a sphere given their
        longitudes and latitudes.
    """
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    h = math.sin((lat2 - lat1) / 2) ** 2 + \
        math.cos(lat1) * \
        math.cos(lat2) * \
        math.sin((lon2 - lon1) / 2) ** 2

    return 6372.8 * 2 * math.asin(math.sqrt(h))


def get_dist(meteor):
    return meteor.get('distance', math.inf)


if __name__ == '__main__':
    # You can change my_loc to your own location or any other location
    # I used 'https://www.findlatitudeandlongitude.com/' to grab my coordinates
    my_loc = (39.081237, -77.151401)

    meteor_resp = requests.get('https://data.nasa.gov/resource/y77d-th95.json')
    meteor_data = meteor_resp.json()

    for meteor in meteor_data:
        if not ('reclat' in meteor and 'reclong' in meteor):
            continue
        meteor['distance'] = calc_dist(float(meteor['reclat']),
                                       float(meteor['reclong']), my_loc[0],
                                       my_loc[1])

    meteor_data.sort(key=get_dist)

    print(meteor_data[0:10])
