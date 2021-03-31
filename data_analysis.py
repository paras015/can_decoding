from flask import Flask, render_template, request, redirect, url_for, send_file
import cantools
import pandas as pd
import os
import binascii
import datetime
import plotly
import plotly.graph_objs as go
import numpy as np
import json
import plotly.express as px
import time
# import dash
# import dash_core_components as dcc
# import dash_html_components as html

app = Flask(__name__)
ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLD = os.path.dirname('C:/Users/paras/Desktop/Paras/Orion/Tronics/Flask Website/History')
UPLOAD_FOLDER = os.path.join(ROOT_PATH, UPLOAD_FOLD)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
# dash_app = dash.Dash(__name__, external_stylesheets=external_stylesheets, url_base_pathname='/pathname/', server=app)
#
# df = pd.DataFrame({
#     "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
#     "Amount": [4, 1, 2, 2, 4, 5],
#     "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
# })
#
# fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")
#
# dash_app.layout = html.Div(children=[
#     dcc.Graph(
#         id='example-graph',
#         figure=fig
#     )
# ])


@app.route("/graph")
def graph():
    return redirect('/pathname')


class Variables:
    csv_filename = ''
    dbc_filename = ''
    frames = ''
    names = ''
    dt = ''


va = Variables()


class Calculations:
    def __init__(self, csv, dbc):
        self.csv_file = csv
        self.dbc_file = dbc

    def decoding(self):
        start_time = time.time()
        if len(self.dbc_file) == 1:
            db = cantools.database.load_file(os.path.join(ROOT_PATH, va.dt, self.dbc_file[0].filename), database_format='dbc')
        else:
            for i in range(len(self.dbc_file)):
                if i == 0:
                    db = cantools.database.load_file(os.path.join(ROOT_PATH, va.dt, self.dbc_file[i].filename),
                                                     database_format='dbc')
                else:
                    db.add_dbc_file(os.path.join(ROOT_PATH, va.dt, self.dbc_file[i].filename))

        names = range(0, 14)
        if len(self.csv_file) == 1:
            df = pd.read_csv(os.path.join(ROOT_PATH, va.dt, self.csv_file[0].filename), delim_whitespace=True, skiprows=3,
                             skipfooter=1,
                             names=names, engine='python')
        else:
            for i in range(len(self.csv_file)):
                if i == 0:
                    df = pd.read_csv(os.path.join(ROOT_PATH, va.dt, self.csv_file[i].filename), delim_whitespace=True, skiprows=3,
                                     skipfooter=1,
                                     names=names, engine='python')
                else:
                    df1 = df = pd.read_csv(os.path.join(ROOT_PATH, va.dt, self.csv_file[i].filename), delim_whitespace=True, skiprows=3,
                                     skipfooter=1,
                                     names=names, engine='python')
                    df = pd.concat([df, df1], ignore_index=True)

        df.rename(columns={0: 'Time', 2: 'Id'}, inplace=True)
        print(df.shape)
        message_frames = {}

        def int_to_hex(num):
            x = hex(num)
            x = x.replace('0x', '')
            if len(x) == 1:
                x = ('0' + x)
            return x

        for index in range(6, df.shape[1]):
            df.iloc[:, index] = df.iloc[:, index].map(lambda x: int_to_hex(x))
        a = 1
        for i in range(6, df.shape[1], 2):
            df['Cell' + str(a)] = df.iloc[:, i + 1].astype(str) + "" + df.iloc[:, i].astype(str)
            a += 1
        df['Data'] = df['Cell1'] + df['Cell2'] + df['Cell3'] + df['Cell4']
        df = df.drop(['Cell1', 'Cell2', 'Cell3', 'Cell4'], axis=1)
        df['Data'] = df['Data'].map(lambda x: bytearray.fromhex(x))
        df['Data'].apply(lambda x: x.reverse())

        for row in range(df.shape[0]):
            name = db.get_message_by_frame_id(df['Id'][row]).name
            if not name in message_frames:
                message_frames[name] = pd.DataFrame()
            decoded = db.decode_message(df['Id'][row], df['Data'][row])
            decoded['Time'] = df['Time'][row]
            message_frames[name] = message_frames[name].append(decoded, ignore_index=True)
        print("--- %s seconds ---" % (time.time() - start_time))
        print('Done')
        va.frames = message_frames
        va.names = list(message_frames.keys())


@app.route('/analysis')
@app.route('/')
def analysis():
    return render_template('analysis.html')


@app.route('/upload_file', methods=['GET', 'POST'])
def upload_file():
    dt = str(datetime.datetime.now()).replace(":", "_")
    directory = os.path.join('History', dt)
    va.dt = directory
    os.mkdir(directory)
    csv_file = request.files.getlist('CSV file')
    if csv_file:
        for csv in csv_file:
            csv.save(os.path.join(directory, csv.filename))
            print(csv.filename)
    dbc_file = request.files.getlist('DBC file')
    if dbc_file:
        for dbc in dbc_file:
            dbc.save(os.path.join(directory, dbc.filename))
            print(dbc.filename)

    cal = Calculations(csv_file, dbc_file)
    cal.decoding()

    return redirect(url_for('handle_data'))


@app.route('/handle_data', methods=['GET', 'POST'])
def handle_data():
    # select = request.form.get('message', False)
    select1 = request.form.getlist('multiSelect')
    data = []
    if not select1:
        select1.append(va.names[0])
    for i in range(0, len(select1)):
        labels = va.frames[select1[i]]['Time'].values.tolist()
        data1 = va.frames[select1[i]].iloc[:, 0].values.tolist()
        data2 = va.frames[select1[i]].iloc[:, 1].values.tolist()
        data3 = va.frames[select1[i]].iloc[:, 2].values.tolist()
        data4 = va.frames[select1[i]].iloc[:, 3].values.tolist()
        linenames = va.frames[select1[i]].columns.values.tolist()
        datalist = [labels, data1, data2, data3, data4, linenames]
        data.append(datalist)
    return render_template('analysis.html', data=data,
                           names=va.names, select=select1)


@app.route('/export_decoded')
def background_process_test():
    dt = str(datetime.datetime.now()).replace(":", "_")
    file_name = "Decoded - " + dt + ".xlsx"
    file_name = os.path.join('Decoded', file_name)
    writer = pd.ExcelWriter(file_name, engine='xlsxwriter')
    for name in va.names:
        va.frames[name].to_excel(writer, sheet_name=name, startrow=0, startcol=0)
    writer.save()
    print("Exported")
    return "nothing"


@app.route('/history')
def history():
    return render_template('history.html')


if __name__ == '__main__':
    app.debug = True
    port = int(os.environ.get('PORT', 33507))
    app.run(port=port, debug=True)
    app.run(debug=True)
