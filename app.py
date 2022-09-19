from flask import Flask, redirect, url_for, request, render_template, jsonify
import urllib.request
import subprocess
import json
import datetime as date



app = Flask(__name__)
app.secret_key = 'ThisisSuperFlagBySecurityDojo'

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

#Injection Vulnerability
@app.route('/welcome/<name>')
def success(name):
    return 'welcome %s' % name

#Injection Vulnerability
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user = request.form['name']
        return redirect(url_for('success', name=user))
    else:
        user = request.args.get('name')
        return redirect(url_for('success', name=user))


#SSRF Vulnerability
@app.route('/redirect')
def web():
    try:
        site=request.args.get('url')
        response = urllib.request.urlopen(site)
        output=json.dumps(response.read().decode('utf-8'))
        return jsonify({"output": output}), 200
    except:
        return ("Error Ocurred")

#Command Execution
@app.route('/date')
def command():
    try:
        cmd = request.args.get('exec')
        count = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        stdout, stderr = count.communicate()
        #print(stdout.decode())
        return jsonify({"output": stdout.decode()}), 200

    except:
        return ("Error Ocurred")



