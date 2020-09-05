# coding: utf-8

import os
import platform
import datetime
import socket
import requests
import glob
from flask import Flask, render_template, redirect, send_from_directory

def get_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8",80))
        ip = s.getsockname()[0]
        return ip
    except:
        return None


def time_to_date(time):
    date_time = datetime.datetime.fromtimestamp(time)
    date = date_time.strftime('%d/%m/%Y %H:%M:%S')
    return date
  
    
def file_time(path):
    time = None
    if platform.system() == 'Windows':
        time =  os.path.getctime(path)
    else:
        stat = os.stat(path)
        try:
            time =  stat.st_birthtime
        except AttributeError:
            time =  stat.st_mtime
    return time

    
ip = get_ip()
while ip is None:
    ip = get_ip()
    

app = Flask(__name__)
app.jinja_env.auto_reload = True
app.config['TEMPLATES_AUTO_RELOAD'] = True


@app.route('/')
def index():
    return render_template('index.html', ip=ip)
    
@app.route('/videos/')
def videos():
    files = glob.glob('motion/*.mkv')
    files = sorted(files, key = lambda file: file_time(file), reverse=True)
    videos = [{'date': time_to_date(file_time(file)), 'file': os.path.basename(file)} for file in files]
    return render_template('videos.html', videos=videos)

@app.route('/videos/<name>')
def send_video(name):
    return send_from_directory('motion', name)

@app.route('/videos/delete/<name>')
def delete_video(name):
    os.remove(os.path.join('motion', name))
    return redirect('/videos/')

@app.route('/motion/status')
def motion_status():
    r = requests.get('http://' + ip + ':8081/0/detection/status')
    return r.content
    
@app.route('/motion/start')
def motion_start():
    r = requests.get('http://' + ip + ':8081/0/detection/start')
    return r.content
    
@app.route('/motion/pause')
def motion_pause():
    r = requests.get('http://' + ip + ':8081/0/detection/pause')
    return r.content
    

app.run(host='0.0.0.0', port=80, debug=False)
    
