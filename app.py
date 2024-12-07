from flask import Flask, render_template, request

from API_calls import get_usgs_data, print_usgs_data, get_noaa_data, get_species

app = Flask(__name__)

#Search page querying user for parameters needed to make API calls
@app.route('/')
def home():
    return render_template('home.html')

#Search results page that implements all 3 API calls
@app.route('/results', methods=['GET', 'POST'])
def results():

    if request.method == 'POST':

        siteCode = int(request.form['siteCode'])
        if get_usgs_data(siteCode) is None:
            error()
        siteDataRaw = get_usgs_data(siteCode)
        siteData = print_usgs_data(siteDataRaw)
        print(siteData)
        siteLocation = siteData.pop(1),siteData.pop(1)
        siteData.insert(1, 'Statistic')
        siteData.insert(1, 'Value')
        coords = request.form.getlist('coords[]')
        if get_noaa_data(coords[0], coords[1]) is None or get_species(coords[0], coords[1], coords[2], coords[3]) is None:
            error()
        weather= get_noaa_data(coords[0], coords[1])
        fish = get_species(coords[0], coords[1], coords[2], coords[3])
        return render_template('results.html', siteCode=siteCode, siteData=siteData, weather=weather,
                                fish=fish, siteLocation=siteLocation)
    else:
        return "HTTP error"

@app.route('/error')
def error():
    return render_template('error.html')