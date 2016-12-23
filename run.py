import os
import os.path as osp
from flask import Flask
from flask import render_template as render
from flask import send_from_directory as sfd
from collections import OrderedDict

app = Flask(__name__, static_url_path='')

data_path = './data'
data = {}
years = {}


@app.route('/')
def main_routine():
    year_title = get_year_and_titles()
    return render('index.html', year_title=year_title)


@app.route('/statics/<path:path>')
def send_static(path):
    return sfd('statics', path)


@app.route('/<string: title>')
def get_content(title):
    pass



def get_year_and_titles():
    global years
    if len(years) == 0:
        load_data(data_path)
    return years


def load_data(path):
    global years
    global data
    # load the data from disk
    files = os.listdir(path)
    count = 0
    for f in files:
        if len(f) < 3:
            continue
        year = f[-12:-8]
        if year not in years:
            years[year] = []
        # get title and save to years
        title = f[:-12]
        years[year].append(title.decode('utf-8'))

        # get the data and save to data
        if title in data:
            title += str(count)
            count += 1
        # read data
        file_name = osp.join(path, f)
        with open(file_name, 'r') as fid:
            content = fid.read()
            data[title] = content.decode('utf-8')
            fid.close()
        years = OrderedDict(sorted(years.items(),
                                   reverse=True))

