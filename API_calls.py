import urllib.request, urllib.parse, urllib.error, json
import pprint



# Behavior: function to get streamflow data from USGS survey site
# Parameter: takes in a site code for the survey site. aiming to find some way to give user the site code based on inputted coordinates
# Returns: return the streamflow average for the previous day.
# **Need to have code update to detect current day and set date to previous in order to get most recent daily average**


def get_usgs_data(site_code = 12201700):
    baseurl = "https://waterservices.usgs.gov/nwis/dv/"
    paramters = {
        'format': 'json',
        'sites': site_code,
        'startDT': '2024-11-24',
        'endDT': '2024-11-24',
        'siteStatus': 'all',
    }
    paramstr = urllib.parse.urlencode(paramters)

    request = baseurl + "?" + paramstr
    print(request)
    try:
        with urllib.request.urlopen(request) as response:
            data = json.loads(response.read().decode("utf-8"))
            return data
    except urllib.error.URLError as e:
        print(f"Failed to retrieve data: {e.reason}")
        return None

# Prints all water data provided in the return
def print_usgs_data(data):
    if data is None:
        return "No data available"
    print(data['value']['timeSeries'][0]['sourceInfo']['siteName'])
    print(
        'latitude: ' + str(data['value']['timeSeries'][0]['sourceInfo']['geoLocation']['geogLocation']['latitude']))
    print('longitude: ' + str(
        data['value']['timeSeries'][0]['sourceInfo']['geoLocation']['geogLocation']['longitude']))

    for value in data['value']['timeSeries']:
        print(value['variable']['variableDescription'])
        print(value['values'][0]['value'][0]['value'])

    #return(json.loads(urllib.request.urlopen(request).read().decode("utf-8")))
data = get_usgs_data()
print_usgs_data(data)
#pprint.pprint(data)
#12134500 skykomish river

def get_usgs_siteCode(lat=48.70216667, lng=-122.4824722):
    baseurl = "https://dashboard.waterdata.usgs.gov/api/geocoder/1.0.1/search"
    paramters = {

        'lat': lat,
        'lon': lng,
        'format': 'json',


    }
    paramstr = urllib.parse.urlencode(paramters)

    request = baseurl + "?" + paramstr
    print(request)
    try:
        with urllib.request.urlopen(request) as response:
            data = json.loads(response.read().decode("utf-8"))
            site_id = data['results'][0]['site_id']
            site_name = data['results'][0]['site_name']
            return site_id, site_name
    except urllib.error.URLError as e:
        print(f"Failed to retrieve data: {e.reason}")
        return None


print(get_usgs_siteCode())

def get_noaa_data(lat=48.70216667, lng=-122.4824722):



    request = "https://api.weather.gov/points/" + str(lat) + "," + str(lng)
    print(request)
    try:
        with urllib.request.urlopen(request) as response:
            data = json.loads(response.read().decode("utf-8"))
            pprint.pprint(data)
            #site_id = data['results'][0]['site_id']
            #site_name = data['results'][0]['site_name']
            #return site_id, site_name
    except urllib.error.URLError as e:
        print(f"Failed to retrieve data: {e.reason}")
        return None

get_noaa_data()

# Using the geodataservices.wdfw.wa.gov/arcgis/rest/services/MapServices/SWIFD/MapServer/0/query API to get WA state fish records
def get_species():
    return None

