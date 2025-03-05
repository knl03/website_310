import urllib.request, urllib.parse, urllib.error, json
import pprint
import datetime




# Behavior: function to get streamflow data from USGS survey site
# Parameter: takes in a site code for the survey site. aiming to find some way to give user the site code based on inputted coordinates
# Returns: return the stream data averages for the previous day.

def get_usgs_data(site_code = 12201700, delta = 1):
    baseurl = "https://waterservices.usgs.gov/nwis/dv/"
    #print(str(datetime.date.today() - datetime.timedelta(1)))
    parameters = {
        'format': 'json',
        'sites': site_code,
        'startDT': str(datetime.date.today() - datetime.timedelta(delta)),
        'endDT': str(datetime.date.today() - datetime.timedelta(delta)),
        'siteStatus': 'all',
    }
    paramstr = urllib.parse.urlencode(parameters)

    request = baseurl + "?" + paramstr
    #print(request)
    try:
        with urllib.request.urlopen(request) as response:
            data = json.loads(response.read().decode("utf-8"))


    except urllib.error.URLError as e:
        #print(f"Failed to retrieve data: {e.reason}")
        return None
    if len(data['value']['timeSeries']) == 0:
        data = get_usgs_data(site_code, delta + 1)
    return data
#print(get_usgs_data(12213100))


#Behavior: formats the data from the usgs data call into a list that can later be processed into html
#Returns: returns the list of all relevant data from the API call
#Parameters: the data returned by the usgs api call function

def print_usgs_data(data):


    if len(data['value']['timeSeries']) == 0:
        return None
    printList = []
    printList.append("Available data for " + data['value']['timeSeries'][0]['sourceInfo']['siteName'] + " on " + str(datetime.date.today() - datetime.timedelta(1)))
    printList.append('latitude: ' + str(data['value']['timeSeries'][0]['sourceInfo']['geoLocation']['geogLocation']['latitude']))
    printList.append('longitude: ' + str(data['value']['timeSeries'][0]['sourceInfo']['geoLocation']['geogLocation']['longitude']))
    for value in data['value']['timeSeries']:
        printList.append(value['variable']['variableDescription'])
        printList.append(value['values'][0]['value'][0]['value'])
        printList.append(value['variable']['options']['option'][0]['value'])
    return printList


#Behavior: Completes a request to the noaa forecast API based on coordinates and collects forecasts for the next 3 days.
#           Skips over nightly forecasts, only records daytime forecasts.
#Return: returns a dictionary containing the day and the corresponding forecast
#Parameters: latitude and longitude of location user wants forecast for
def get_noaa_data(lat=48.70216667, lng=-122.4824722):

    request = "https://api.weather.gov/points/" + str(lat) + "," + str(lng)

    try:
        with urllib.request.urlopen(request) as response:
            data = json.loads(response.read().decode("utf-8"))
            url = data['properties']['forecast']
            print(url)


    except urllib.error.URLError as e:
        print(f"Failed to retrieve data: {e.reason}")
        return None

    today = datetime.datetime.now()
    try:
        with urllib.request.urlopen(url) as response:
            data2 = json.loads(response.read().decode("utf-8"))
            index = 0
            forecast = {}

            for data in data2['properties']['periods']:

                if "Night" not in data['name'] and "Tonight" not in data['name'] and index < 3:
                    forecast[data['name']] = data['detailedForecast']
                    index += 1

            return forecast


    except urllib.error.URLError as e:
        print(f"Failed to retrieve data: {e.reason}")
        return None



#Behavior: this function queries the WDFW fish records to find all species that have been reported inside the queried zone. It also
#           finds all the streams where each fish can be found.
#Return: returns a dictionary with keys of all fish species and then values of all locations where each has been recorded.
#Parameter: takes two coordinates to create a zone to search within, provides data for all water bodies within that zone.
def get_species(lat1 = 48.815367, lng1= -122.607774, lat2 = 48.778015, lng2 = -122.548735):
    parameters = {
        'where': '1=1',
        'outFields': '*',
        'geometry': f'{lng1},{lat1},{lng2},{lat2}',
        'geometryType': 'esriGeometryEnvelope',
        'inSR': '4326',
        'spatialRel': 'esriSpatialRelIntersects',
        'outSR': '4326',
        'f': 'json'

    }
    baseurl = 'https://geodataservices.wdfw.wa.gov/arcgis/rest/services/MapServices/SWIFD/MapServer/0/query'

    request = baseurl + '?' + urllib.parse.urlencode(parameters)

    try:
        with urllib.request.urlopen(request) as response:
            data = json.loads(response.read().decode("utf-8"))

            species = {}

            for item in data['features']:

                if item['attributes']['SPECIES'] not in species:
                    if 'Unnamed stream' in item['attributes']['LLID_STRM_NAME']:
                        species[item['attributes']['SPECIES']] = []
                    else:
                        species[item['attributes']['SPECIES']] = [item['attributes']['LLID_STRM_NAME']]
                else:
                    if item['attributes']['LLID_STRM_NAME'] not in species[item['attributes']['SPECIES']] and 'Unnamed stream' not in item['attributes']['LLID_STRM_NAME']:
                        species[item['attributes']['SPECIES']].append(item['attributes']['LLID_STRM_NAME'])

            return species

    except urllib.error.URLError as e:
        print(f"Failed to retrieve data: {e.reason}")
        return None

#get_species()
