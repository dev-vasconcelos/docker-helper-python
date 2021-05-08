import flask
import os
from flask import request

app = flask.Flask(__name__)
app.config["DEBUG"]

@app.route('/hellothere', methods=["GET"])
def helloThere():
    return "General Kennoby"

@app.route('/', methods=["GET"])
def list():
    some = "somequeijo"
    return os.popen('docker ps').read()

@app.route('/listall', methods=["GET"])
def listall():
    return os.popen('docker ps -a').read()

@app.route('/check', methods=["GET"])
def checkContainer():
    checkName = request.args.get('name', default = "000", type = str)
    
    returnStr = os.popen('docker ps -a').read()
    if ( checkName in returnStr ):
        return "True"
    else:
        return "False"

@app.route('/create', methods=["GET"])
def createContainer():
    
    containerName = request.args.get('name', default = "defaultName", type = str)
    osName = request.args.get('os', default = "ubuntu", type = str)

    command = "docker run -td "

    if str(containerName) != "defaultName":
        command += " --name " + str(containerName)
    
    command += " " + str(osName)
    
    # os.system(command)
    return os.popen(command).read()

@app.route('/removeContainer', methods=["GET"])
def removeContainer():
    containerName = request.args.get('name', default = "000", type = str)
    
    if str(containerName) != "000":
        command = "docker rm -f " + containerName
    else:
        return "no container name sent, wish to delete all? go to /deleteAllContainers"
    
    return os.popen(command).read()

@app.route('/removeAllContainers', methods=["GET"])
def removeAllContainers():
    command = "docker rm -f $(docker ps -q)"

    return os.popen(command).read()

@app.route('/getImage')
def getImage():
    imageName = request.args.get('name', default = " ", type = str)

    if(imageName):
        command = "docker pull " + imageName
    else:
        return "Imagem veio nula"

    return os.popen(command).read()

@app.route('/execContainer')
def exeContainer():
    commandContainer = request.args.get('command', default = "ls", type = str)
    name = request.args.get('name', default = "000", type = str)
    
    if ( str(name) != "000"):
        command = 'docker exec ' + str(name)

    command += ' "' + str(commandContainer) + '"'
    print(command)
    return os.popen(command).read()

app.run(debug=True)
