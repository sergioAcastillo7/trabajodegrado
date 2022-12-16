from collections import OrderedDict
from flask import Flask, render_template, url_for, redirect
from datetime import datetime
import os

app = Flask(__name__)

IMG_FOLDER = os.path.join('static','images')

app.config['UPLOAD_FOLDER'] = IMG_FOLDER

@app.route('/')
def index():
    logoUP = os.path.join(app.config['UPLOAD_FOLDER'], 'escudo_62_anios.png')
    logoIngE = os.path.join(app.config['UPLOAD_FOLDER'], 'logo_act.jpeg')
    return render_template('index.html', logoUP=logoUP, logoIngE=logoIngE)


@app.route('/temperatura-humedad')
def temperatura():
    now = datetime.now()
    fecha_str = now.strftime('%d.%m.%Y')
    path = "" + fecha_str + ".txt"
    with open("data.txt", "r") as tf:
        line_temperatures = tf.read().split('\n')
    # line_humidity = [0, 10, 12, 13, 14, 15, 16, 17, 18, 19, 20, 18, 16, 18, 14, 15, 16, 17, 18, 19, 20]
    labels = range(len(line_temperatures))

    return render_template('temperature.html', title='Datos del Sensor de Temperatura y Humedad', labels=labels,
                           values1=line_temperatures, values2=line_temperatures)


@app.route('/lluvia')
def lluvia():
    now = datetime.now()
    fecha_str = now.strftime('%d.%m.%Y')
    path = "" + fecha_str + ".txt"
    with open("data.txt", "r") as tf:
        line_lluvia = tf.read().split('\n')

    labels = range(len(line_lluvia))

    return render_template('lluvia.html', title='Datos del Sensor de Lluvia', labels=labels,
                           values=line_lluvia)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9999)
