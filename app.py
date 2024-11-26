from flask import Flask, render_template, request

app = Flask(__name__)
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/results', methods=['GET', 'POST'])
def results():
    if request.method == 'POST':
        search = request.form['search']
        return render_template('results.html', search=search)
    else:
        return "HTTP error"